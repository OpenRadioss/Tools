//Copyright>
//Copyright> Copyright (C) 1986-2026 Altair Engineering Inc.
//Copyright>
//Copyright> Permission is hereby granted, free of charge, to any person obtaining
//Copyright> a copy of this software and associated documentation files (the "Software"),
//Copyright> to deal in the Software without restriction, including without limitation
//Copyright> the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
//Copyright> sell copies of the Software, and to permit persons to whom the Software is
//Copyright> furnished to do so, subject to the following conditions:
//Copyright>
//Copyright> The above copyright notice and this permission notice shall be included in all
//Copyright> copies or substantial portions of the Software.
//Copyright>
//Copyright> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//Copyright> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//Copyright> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//Copyright> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
//Copyright> WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
//Copyright> IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
//Copyright>

//! # OpenRadioss Animation-to-VTK Converter
//!
//! Converts OpenRadioss binary animation files (A-files) to VTK Legacy
//! Unstructured Grid format for visualization in ParaView, VisIt, etc.
//!
//! ## OpenRadioss A-File Format
//!
//! Animation files are big-endian binary files containing a full simulation
//! snapshot: node coordinates, element connectivity (1D/2D/3D/SPH), part
//! definitions, nodal and elemental scalar/vector/tensor fields, erosion
//! status, and optional time-history data.  Each file represents one time
//! step; filenames end with a letter+digits suffix (e.g. `modelA001`).
//!
//! ## VTK Output
//!
//! The converter writes VTK Legacy Unstructured Grid files (`.vtk`).
//! Three output modes are supported:
//! - **ASCII (default):** Human-readable, uses fast Ryu formatting for floats.
//! - **ASCII `--legacy`:** Matches the C++ reference converter's `%.6g`
//!   formatting via a custom pure-Rust implementation.
//! - **Binary (`--binary`):** Big-endian binary VTK for smaller files.
//!
//! ## Architecture
//!
//! 1. **I/O layer** – Big-endian readers (`read_i32`, `read_f32_vec`, …)
//! 2. **Formatting** – Custom integer (`write_u32_fast`) and float (`format_g6`)
//!    formatters that avoid `libc` and minimize allocations.
//! 3. **`VtkWriter`** – Buffered writer abstraction that handles binary/ASCII/
//!    legacy mode selection and batches output through a scratch buffer.
//! 4. **`read_radioss_anim`** – Reads the A-file and drives VTK output.
//! 5. **`main`** – Argument parsing, memory-aware thread pool, file dispatch.
//!
//! ## Usage
//!
//! ```text
//! anim_to_vtk <file1> [file2 ...] [--binary] [--legacy] [--threads N]
//! ```

use std::env;
use std::fs::File;
use std::io::{BufReader, BufWriter, Read, Write};
use std::process;
use std::path::Path;
use std::sync::{mpsc, Arc, Mutex};
use std::thread;

/// Magic number identifying OpenRadioss animation file format version 10.
const FASTMAGI10: i32 = 0x542c;

// =====================================================================
// Big-endian binary I/O
// =====================================================================
// OpenRadioss animation files store all numeric data in big-endian byte
// order.  These functions read scalars and vectors from the input stream,
// converting to native (little-endian on x86) representation.

/// Read a single big-endian `i32` from the input stream.
fn read_i32<R: Read>(reader: &mut R) -> i32 {
    let mut buf = [0u8; 4];
    reader.read_exact(&mut buf).expect("Error in reading file");
    i32::from_be_bytes(buf)
}

/// Read a single big-endian `f32` from the input stream.
fn read_f32<R: Read>(reader: &mut R) -> f32 {
    let mut buf = [0u8; 4];
    reader.read_exact(&mut buf).expect("Error in reading file");
    f32::from_be_bytes(buf)
}

/// Read `count` big-endian `i32` values into a newly allocated `Vec`.
fn read_i32_vec<R: Read>(reader: &mut R, count: usize) -> Vec<i32> {
    let byte_len = count * 4;
    let mut bytes = vec![0u8; byte_len];
    reader.read_exact(&mut bytes).expect("Error in reading file");
    bytes.chunks_exact(4)
        .map(|c| i32::from_be_bytes(c.try_into().unwrap()))
        .collect()
}

/// Read `count` big-endian `f32` values into a newly allocated `Vec`.
///
/// Uses `f32::from_bits(u32::from_be_bytes(…))` for exact bit-level
/// conversion without involving float arithmetic.
fn read_f32_vec<R: Read>(reader: &mut R, count: usize) -> Vec<f32> {
    let byte_len = count * 4;
    let mut bytes = vec![0u8; byte_len];
    reader.read_exact(&mut bytes).expect("Error in reading file");
    bytes.chunks_exact(4)
        .map(|c| f32::from_bits(u32::from_be_bytes(c.try_into().unwrap())))
        .collect()
}

/// Read `count` big-endian `u16` values (used for normals / skew data).
fn read_u16_vec<R: Read>(reader: &mut R, count: usize) -> Vec<u16> {
    let byte_len = count * 2;
    let mut bytes = vec![0u8; byte_len];
    reader.read_exact(&mut bytes).expect("Error in reading file");
    bytes.chunks_exact(2)
        .map(|c| u16::from_be_bytes(c.try_into().unwrap()))
        .collect()
}

/// Read `count` raw bytes (used for deletion flags, one byte per element).
fn read_bytes<R: Read>(reader: &mut R, count: usize) -> Vec<u8> {
    let mut buf = vec![0u8; count];
    reader.read_exact(&mut buf).expect("Error in reading file");
    buf
}

/// Read a fixed-width text field, stripping trailing NUL padding.
///
/// Used for part names, field labels, and other descriptive strings
/// embedded in the animation file.
fn read_text<R: Read>(reader: &mut R, count: usize) -> String {
    let buf = read_bytes(reader, count);
    let s = String::from_utf8_lossy(&buf);
    s.trim_end_matches('\0').to_string()
}

// =====================================================================
// System utilities
// =====================================================================

/// Query available system memory from `/proc/meminfo` (Linux only).
///
/// Returns `None` on non-Linux platforms or if the file cannot be read.
/// Used to limit the number of worker threads so that all files being
/// processed concurrently fit in memory.
fn mem_available_bytes() -> Option<u64> {
    let content = std::fs::read_to_string("/proc/meminfo").ok()?;
    for line in content.lines() {
        if let Some(rest) = line.strip_prefix("MemAvailable:") {
            let mut parts = rest.split_whitespace();
            let kb = parts.next()?.parse::<u64>().ok()?;
            return Some(kb * 1024);
        }
    }
    None
}

/// Compute the maximum number of worker threads based on available CPUs
/// and memory.  Each file is fully loaded into memory during conversion,
/// so the thread count is capped so that `max_file_size × threads` does
/// not exceed 80% of available RAM.
fn compute_max_threads(file_sizes: &[u64]) -> usize {
    if file_sizes.is_empty() {
        return 1;
    }
    let cpu_limit = thread::available_parallelism().map(|n| n.get()).unwrap_or(1);
    let max_file = *file_sizes.iter().max().unwrap_or(&0);
    let mem_available = mem_available_bytes();

    let mem_limit = match (mem_available, max_file) {
        (Some(mem), size) if size > 0 => {
            let usable = (mem as f64 * 0.8) as u64;
            let threads = (usable / size.saturating_mul(2)) as usize;
            if threads == 0 { 1 } else { threads }
        }
        _ => 1,
    };

    let mut max_threads = cpu_limit.min(mem_limit);
    if max_threads == 0 {
        max_threads = 1;
    }
    max_threads.min(file_sizes.len())
}

/// Replace spaces with underscores in field names.
///
/// VTK field names must not contain spaces, so this is applied to all
/// scalar, vector, and tensor labels read from the animation file.
fn replace_underscore(s: &str) -> String {
    s.replace(' ', "_")
}

// =====================================================================
// Fast integer-to-ASCII formatting
// =====================================================================
// These functions convert integers directly into byte buffers without
// allocating strings.  They use a two-digit lookup table (DIGIT_PAIRS)
// to emit two ASCII digits per division, halving the loop iterations
// compared to a naive digit-by-digit approach.

/// Lookup table mapping each value 0..99 to its two-digit ASCII
/// representation ("00", "01", …, "99").
static DIGIT_PAIRS: &[u8; 200] = b"\
0001020304050607080910111213141516171819\
2021222324252627282930313233343536373839\
4041424344454647484950515253545556575859\
6061626364656667686970717273747576777879\
8081828384858687888990919293949596979899";

/// Write an unsigned 32-bit integer as ASCII decimal into `buf`.
///
/// Returns the number of bytes written.  `buf` must be at least 10 bytes.
/// Digits are produced in reverse order using the `DIGIT_PAIRS` table,
/// then copied to the start of `buf`.
#[inline(always)]
fn write_u32_fast(buf: &mut [u8], mut val: u32) -> usize {
    if val == 0 {
        buf[0] = b'0';
        return 1;
    }
    // Write digits from the end using 2-digit lookup
    let mut tmp = [0u8; 10];
    let mut pos = 10usize;
    while val >= 100 {
        let rem = (val % 100) as usize;
        val /= 100;
        pos -= 2;
        tmp[pos] = DIGIT_PAIRS[rem * 2];
        tmp[pos + 1] = DIGIT_PAIRS[rem * 2 + 1];
    }
    if val >= 10 {
        let rem = val as usize;
        pos -= 2;
        tmp[pos] = DIGIT_PAIRS[rem * 2];
        tmp[pos + 1] = DIGIT_PAIRS[rem * 2 + 1];
    } else {
        pos -= 1;
        tmp[pos] = b'0' + val as u8;
    }
    let len = 10 - pos;
    buf[..len].copy_from_slice(&tmp[pos..10]);
    len
}

/// Write a signed 32-bit integer as ASCII decimal into `buf`.
///
/// Returns the number of bytes written.  `buf` must be at least 11 bytes
/// (sign + 10 digits).  Negative values are handled by prepending `'-'`
/// and formatting the absolute value.
#[inline(always)]
fn write_i32_fast(buf: &mut [u8], val: i32) -> usize {
    if val >= 0 {
        write_u32_fast(buf, val as u32)
    } else {
        buf[0] = b'-';
        1 + write_u32_fast(&mut buf[1..], val.unsigned_abs())
    }
}

/// Write an unsigned 64-bit integer as ASCII decimal into `buf`.
///
/// Returns the number of bytes written.  `buf` must be at least 20 bytes.
/// Values that fit in `u32` are delegated to the faster 32-bit path.
#[inline(always)]
fn write_u64_fast(buf: &mut [u8], mut val: u64) -> usize {
    if val == 0 {
        buf[0] = b'0';
        return 1;
    }
    // For values that fit in u32, use the faster path
    if val <= u32::MAX as u64 {
        return write_u32_fast(buf, val as u32);
    }
    let mut tmp = [0u8; 20];
    let mut pos = 20usize;
    while val >= 100 {
        let rem = (val % 100) as usize;
        val /= 100;
        pos -= 2;
        tmp[pos] = DIGIT_PAIRS[rem * 2];
        tmp[pos + 1] = DIGIT_PAIRS[rem * 2 + 1];
    }
    if val >= 10 {
        let rem = val as usize;
        pos -= 2;
        tmp[pos] = DIGIT_PAIRS[rem * 2];
        tmp[pos + 1] = DIGIT_PAIRS[rem * 2 + 1];
    } else {
        pos -= 1;
        tmp[pos] = b'0' + val as u8;
    }
    let len = 20 - pos;
    buf[..len].copy_from_slice(&tmp[pos..20]);
    len
}

// =====================================================================
// Fast pure-Rust `%.6g` float formatting
// =====================================================================
// Implements the C `printf("%.6g", val)` formatting convention without
// calling libc.  This is used in `--legacy` mode to match the output
// of the original C++ reference converter.
//
// The algorithm works in three phases:
//   1. Compute floor(log10(|val|)) using IEEE 754 bit extraction.
//   2. Decide between fixed-point and exponential notation:
//      - Fixed-point if exponent ∈ [-4, 6)
//      - Exponential otherwise
//   3. Scale the value to an integer mantissa with 6 significant digits,
//      strip trailing zeros, and emit using the integer formatter.
//
// Lookup tables for powers of 10 avoid repeated floating-point
// multiplication and division.

/// Precomputed powers of 10 as `f64` for exponents 0…23.
static POW10_F64: [f64; 23] = [
    1e0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9,
    1e10, 1e11, 1e12, 1e13, 1e14, 1e15, 1e16, 1e17, 1e18, 1e19,
    1e20, 1e21, 1e22,
];

/// Precomputed powers of 10 as `u64` for exponents 0…19.
static POW10_U64: [u64; 20] = [
    1, 10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000,
    100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000,
    1_000_000_000_000, 10_000_000_000_000, 100_000_000_000_000,
    1_000_000_000_000_000, 10_000_000_000_000_000,
    100_000_000_000_000_000, 1_000_000_000_000_000_000,
    10_000_000_000_000_000_000,
];

/// Look up 10^e from the precomputed table, falling back to `powi`
/// for exponents outside the table range.
#[inline(always)]
fn pow10_f64(e: i32) -> f64 {
    if e >= 0 && (e as usize) < POW10_F64.len() {
        POW10_F64[e as usize]
    } else if e < 0 && ((-e) as usize) < POW10_F64.len() {
        1.0 / POW10_F64[(-e) as usize]
    } else {
        10.0f64.powi(e)
    }
}

/// Fast `floor(log10(v))` using IEEE 754 bit extraction.
///
/// Extracts the binary exponent from the float's bit representation
/// and approximates `log10` via the ratio `log10(2) ≈ 77/256`.
/// A correction step using the power-of-10 table guarantees an exact
/// result for all finite positive values.
#[inline(always)]
fn fast_log10_floor(v: f64) -> i32 {
    let bits = v.to_bits();
    let biased_exp = ((bits >> 52) & 0x7FF) as i32;
    let binary_exp = biased_exp - 1023;
    // log10(2) ≈ 0.30103; approximate as 77/256 ≈ 0.30078
    let mut approx = (binary_exp * 77) >> 8;
    // Inline the table lookup for the correction to avoid function-call overhead
    let p = if approx >= 0 && (approx as usize) < POW10_F64.len() {
        POW10_F64[approx as usize]
    } else {
        pow10_f64(approx)
    };
    if v < p {
        approx -= 1;
    } else {
        // Check approx+1
        let p1 = if approx + 1 >= 0 && ((approx + 1) as usize) < POW10_F64.len() {
            POW10_F64[(approx + 1) as usize]
        } else {
            pow10_f64(approx + 1)
        };
        if v >= p1 {
            approx += 1;
        }
    }
    approx
}

/// Remove trailing zeros from a decimal digit string represented as an
/// integer.  Returns `(stripped_value, remaining_digit_count)`.
///
/// For example, `strip_trailing_zeros(12300, 5)` returns `(123, 3)`.
/// This is used to suppress trailing zeros in `%.6g` output.
#[inline(always)]
fn strip_trailing_zeros(mut val: u64, digits: u32) -> (u64, u32) {
    let mut d = digits;
    // Remove 2 trailing zeros at a time
    while d >= 2 && val % 100 == 0 {
        val /= 100;
        d -= 2;
    }
    if d >= 1 && val % 10 == 0 {
        val /= 10;
        d -= 1;
    }
    (val, d)
}

/// Format an `f64` value as `%.6g` (6 significant digits, shortest
/// representation), writing directly into `buf`.
///
/// Returns the number of bytes written.  `buf` must be at least 32 bytes.
/// Handles NaN, ±Inf, zero, and negative values.  Delegates to
/// [`format_g6_exp`] when exponential notation is needed.
#[inline]
fn format_g6(buf: &mut [u8], val: f64) -> usize {
    if val.is_nan() {
        buf[..3].copy_from_slice(b"nan");
        return 3;
    }
    let mut pos = 0usize;
    let mut v = val;
    if val.is_sign_negative() && val != 0.0 {
        if val.is_infinite() {
            buf[..4].copy_from_slice(b"-inf");
            return 4;
        }
        buf[0] = b'-';
        pos = 1;
        v = -val;
    } else if val.is_infinite() {
        buf[..3].copy_from_slice(b"inf");
        return 3;
    }

    if v == 0.0 {
        buf[pos] = b'0';
        return pos + 1;
    }

    let exp10 = fast_log10_floor(v);
    const PRECISION: i32 = 6;

    // Fixed-point notation for exponents in [-4, 6), e.g. 0.001234 or 12345.6
    // Exponential notation otherwise, e.g. 1.23e+10 or 1.5e-05
    if exp10 >= -4 && exp10 < PRECISION {
        let frac_digits = (PRECISION - 1 - exp10).max(0) as u32;
        let scale = pow10_f64(frac_digits as i32);
        let rounded = (v * scale + 0.5) as u64;

        // Check if rounding carried into the next order of magnitude,
        // which would push us into exponential notation territory.
        if frac_digits > 0 {
            let total_digits = (frac_digits as i32) + exp10 + 1;
            if total_digits >= 0 && (total_digits as usize) < POW10_U64.len() {
                let pow_check = POW10_U64[total_digits as usize];
                if rounded >= pow_check && exp10 + 1 >= PRECISION {
                    return format_g6_exp(buf, pos, v, exp10);
                }
            }
        }

        let divisor = POW10_U64[frac_digits as usize];
        let int_part = rounded / divisor;
        let frac_part = rounded % divisor;

        let ilen = write_u64_fast(&mut buf[pos..], int_part);
        pos += ilen;

        if frac_digits > 0 {
            let (frac, fdigits) = strip_trailing_zeros(frac_part, frac_digits);
            if fdigits > 0 {
                buf[pos] = b'.';
                pos += 1;
                let frac_start = pos;
                pos += fdigits as usize;
                let mut f = frac;
                let mut i = pos;
                while i >= frac_start + 2 {
                    let r = (f % 100) as usize;
                    f /= 100;
                    i -= 2;
                    buf[i] = DIGIT_PAIRS[r * 2];
                    buf[i + 1] = DIGIT_PAIRS[r * 2 + 1];
                }
                if i > frac_start {
                    buf[frac_start] = b'0' + (f % 10) as u8;
                }
            }
        }
        pos
    } else {
        format_g6_exp(buf, pos, v, exp10)
    }
}

/// Format the exponential-notation branch of `%.6g`.
///
/// Produces output like `1.23e+04`.  The exponent always has at least
/// two digits with an explicit sign, matching C `printf` conventions.
/// `pos` is the current write position in `buf` (after the sign, if any).
#[inline]
fn format_g6_exp(buf: &mut [u8], mut pos: usize, v: f64, exp10: i32) -> usize {
    const PRECISION: i32 = 6;
    let frac_digits = (PRECISION - 1) as u32;
    let scale = pow10_f64(frac_digits as i32);
    let sig = v / pow10_f64(exp10);
    let mut rounded = (sig * scale + 0.5) as u64;
    let mut e = exp10;

    if rounded >= POW10_U64[(frac_digits + 1) as usize] {
        rounded /= 10;
        e += 1;
    }

    let divisor = POW10_U64[frac_digits as usize];
    let int_digit = rounded / divisor;
    let frac_val = rounded % divisor;

    buf[pos] = b'0' + int_digit as u8;
    pos += 1;

    let mut frac = frac_val;
    let mut fdigits = frac_digits;
    let (frac_stripped, fdigits_stripped) = strip_trailing_zeros(frac, fdigits);
    frac = frac_stripped;
    fdigits = fdigits_stripped;
    if fdigits > 0 {
        buf[pos] = b'.';
        pos += 1;
        let frac_start = pos;
        pos += fdigits as usize;
        let mut f = frac;
        let mut i = pos;
        while i >= frac_start + 2 {
            let r = (f % 100) as usize;
            f /= 100;
            i -= 2;
            buf[i] = DIGIT_PAIRS[r * 2];
            buf[i + 1] = DIGIT_PAIRS[r * 2 + 1];
        }
        if i > frac_start {
            buf[frac_start] = b'0' + (f % 10) as u8;
        }
    }

    buf[pos] = b'e';
    pos += 1;
    if e < 0 {
        buf[pos] = b'-';
        pos += 1;
        e = -e;
    } else {
        buf[pos] = b'+';
        pos += 1;
    }
    if e < 10 {
        buf[pos] = b'0';
        buf[pos + 1] = b'0' + e as u8;
        pos += 2;
    } else if e < 100 {
        buf[pos] = b'0' + (e / 10) as u8;
        buf[pos + 1] = b'0' + (e % 10) as u8;
        pos += 2;
    } else {
        let elen = write_u64_fast(&mut buf[pos..], e as u64);
        pos += elen;
    }
    pos
}

// =====================================================================
// VtkWriter – buffered VTK output abstraction
// =====================================================================
// All VTK output goes through this struct, which selects between binary
// (big-endian) and ASCII representations and provides batch-write
// methods that minimise per-value I/O overhead.  A reusable `scratch`
// buffer is used for bulk formatting before flushing to the underlying
// `BufWriter`.

/// Buffered writer for VTK Legacy format output.
///
/// Wraps a `BufWriter` and adds:
/// - Mode selection: binary / ASCII / ASCII-legacy (`%.6g`).
/// - A reusable `scratch` buffer for batching small writes.
struct VtkWriter<W: Write> {
    writer: BufWriter<W>,
    /// If `true`, emit big-endian binary values instead of ASCII.
    binary: bool,
    /// If `true` (and `binary` is `false`), format floats with `%.6g`
    /// for exact compatibility with the C++ reference converter.
    legacy: bool,
    /// Reusable byte buffer for batching formatted output before I/O.
    scratch: Vec<u8>,
}

impl<W: Write> VtkWriter<W> {
    /// Create a new `VtkWriter` wrapping the given output stream.
    fn new(writer: W, binary: bool, legacy: bool) -> Self {
        VtkWriter {
            writer: BufWriter::with_capacity(256 * 1024, writer),
            binary,
            legacy,
            scratch: Vec::with_capacity(128 * 1024),
        }
    }

    /// Write a single float in legacy `%.6g` ASCII format (no newline).
    #[inline(always)]
    fn write_legacy_float_ascii(&mut self, val: f64) {
        let mut buf = [0u8; 32];
        let len = format_g6(&mut buf, val);
        self.writer.write_all(&buf[..len]).unwrap();
    }

    /// Write a single `i32` value followed by a newline (ASCII) or as
    /// 4 big-endian bytes (binary).
    fn write_i32(&mut self, val: i32) {
        if self.binary {
            self.writer.write_all(&val.to_be_bytes()).unwrap();
        } else {
            let mut buf = [0u8; 12]; // 11 for i32 + newline
            let len = write_i32_fast(&mut buf, val);
            buf[len] = b'\n';
            self.writer.write_all(&buf[..len + 1]).unwrap();
        }
    }

    /// Bulk-write a slice of `i32` values, one per line in ASCII mode
    /// or as contiguous big-endian bytes in binary mode.
    ///
    /// Uses the scratch buffer to batch output in 64 KB chunks.
    fn write_i32_slice(&mut self, values: &[i32]) {
        if self.binary {
            const CHUNK_LEN: usize = 16384;
            for chunk in values.chunks(CHUNK_LEN) {
                let out_len = chunk.len() * 4;
                self.scratch.resize(out_len, 0);
                for (i, &val) in chunk.iter().enumerate() {
                    let base = i * 4;
                    let be = val.to_be_bytes();
                    self.scratch[base] = be[0];
                    self.scratch[base + 1] = be[1];
                    self.scratch[base + 2] = be[2];
                    self.scratch[base + 3] = be[3];
                }
                self.writer.write_all(&self.scratch[..out_len]).unwrap();
            }
        } else {
            const BUF_CAP: usize = 65536;
            // Ensure scratch has enough capacity
            if self.scratch.len() < BUF_CAP + 16 {
                self.scratch.resize(BUF_CAP + 16, 0);
            }
            let mut pos = 0usize;
            for &val in values {
                let len = write_i32_fast(&mut self.scratch[pos..], val);
                pos += len;
                self.scratch[pos] = b'\n';
                pos += 1;
                if pos >= BUF_CAP {
                    self.writer.write_all(&self.scratch[..pos]).unwrap();
                    pos = 0;
                }
            }
            if pos > 0 {
                self.writer.write_all(&self.scratch[..pos]).unwrap();
            }
        }
    }

    /// Write a single `f32` value followed by a newline.
    ///
    /// Formatting depends on mode: big-endian bytes (binary), `%.6g`
    /// (legacy ASCII), or Ryu shortest representation (default ASCII).
    #[inline]
    fn write_f32(&mut self, val: f32) {
        if self.binary {
            self.writer.write_all(&val.to_be_bytes()).unwrap();
        } else if self.legacy {
            let mut buf = [0u8; 34];
            let len = format_g6(&mut buf, val as f64);
            buf[len] = b'\n';
            self.writer.write_all(&buf[..len + 1]).unwrap();
        } else {
            let mut ryu_buf = ryu::Buffer::new();
            let s = ryu_buf.format_finite(val);
            self.writer.write_all(s.as_bytes()).unwrap();
            self.writer.write_all(b"\n").unwrap();
        }
    }

    /// Bulk-write a slice of `f32` values, one per line in ASCII mode
    /// or as contiguous big-endian bytes in binary mode.
    ///
    /// More efficient than calling [`write_f32`] in a loop because it
    /// batches output through the scratch buffer.
    fn write_f32_slice(&mut self, values: &[f32]) {
        if self.binary {
            const CHUNK_LEN: usize = 16384;
            for chunk in values.chunks(CHUNK_LEN) {
                let out_len = chunk.len() * 4;
                self.scratch.resize(out_len, 0);
                for (i, &val) in chunk.iter().enumerate() {
                    let base = i * 4;
                    let be = val.to_be_bytes();
                    self.scratch[base] = be[0];
                    self.scratch[base + 1] = be[1];
                    self.scratch[base + 2] = be[2];
                    self.scratch[base + 3] = be[3];
                }
                self.writer.write_all(&self.scratch[..out_len]).unwrap();
            }
        } else if self.legacy {
            const BUF_CAP: usize = 65536;
            if self.scratch.len() < BUF_CAP + 48 {
                self.scratch.resize(BUF_CAP + 48, 0);
            }
            let mut pos = 0usize;
            for &val in values {
                let len = format_g6(&mut self.scratch[pos..], val as f64);
                pos += len;
                self.scratch[pos] = b'\n';
                pos += 1;
                if pos >= BUF_CAP {
                    self.writer.write_all(&self.scratch[..pos]).unwrap();
                    pos = 0;
                }
            }
            if pos > 0 {
                self.writer.write_all(&self.scratch[..pos]).unwrap();
            }
        } else {
            const BUF_CAP: usize = 65536;
            self.scratch.clear();
            let mut ryu_buf = ryu::Buffer::new();
            for &val in values {
                let s = ryu_buf.format_finite(val);
                self.scratch.extend_from_slice(s.as_bytes());
                self.scratch.push(b'\n');
                if self.scratch.len() >= BUF_CAP {
                    self.writer.write_all(&self.scratch).unwrap();
                    self.scratch.clear();
                }
            }
            if !self.scratch.is_empty() {
                self.writer.write_all(&self.scratch).unwrap();
                self.scratch.clear();
            }
        }
    }

    /// Write a single `f64` value followed by a newline.
    fn write_f64(&mut self, val: f64) {
        if self.binary {
            self.writer.write_all(&val.to_be_bytes()).unwrap();
        } else if self.legacy {
            let mut buf = [0u8; 34];
            let len = format_g6(&mut buf, val);
            buf[len] = b'\n';
            self.writer.write_all(&buf[..len + 1]).unwrap();
        } else {
            let mut ryu_buf = ryu::Buffer::new();
            let s = ryu_buf.format_finite(val);
            self.writer.write_all(s.as_bytes()).unwrap();
            self.writer.write_all(b"\n").unwrap();
        }
    }

    /// Write three `f32` values on one line, separated by spaces.
    ///
    /// Used for 3-component data such as node coordinates, vectors,
    /// and tensor rows.
    #[inline]
    fn write_f32_triple(&mut self, a: f32, b: f32, c: f32) {
        if self.binary {
            let mut buf = [0u8; 12];
            buf[0..4].copy_from_slice(&a.to_be_bytes());
            buf[4..8].copy_from_slice(&b.to_be_bytes());
            buf[8..12].copy_from_slice(&c.to_be_bytes());
            self.writer.write_all(&buf).unwrap();
        } else if self.legacy {
            // Max: 3 * ~24 chars + 2 spaces + newline = ~80
            let mut buf = [0u8; 96];
            let mut pos = format_g6(&mut buf, a as f64);
            buf[pos] = b' ';
            pos += 1;
            pos += format_g6(&mut buf[pos..], b as f64);
            buf[pos] = b' ';
            pos += 1;
            pos += format_g6(&mut buf[pos..], c as f64);
            buf[pos] = b'\n';
            pos += 1;
            self.writer.write_all(&buf[..pos]).unwrap();
        } else {
            let mut buf = [0u8; 64];
            let mut ryu_buf = ryu::Buffer::new();
            let s1 = ryu_buf.format_finite(a);
            let mut pos = s1.len();
            buf[..pos].copy_from_slice(s1.as_bytes());
            buf[pos] = b' ';
            pos += 1;
            let s2 = ryu_buf.format_finite(b);
            buf[pos..pos + s2.len()].copy_from_slice(s2.as_bytes());
            pos += s2.len();
            buf[pos] = b' ';
            pos += 1;
            let s3 = ryu_buf.format_finite(c);
            buf[pos..pos + s3.len()].copy_from_slice(s3.as_bytes());
            pos += s3.len();
            buf[pos] = b'\n';
            pos += 1;
            self.writer.write_all(&buf[..pos]).unwrap();
        }
    }

    /// Write `count` zero-valued `f32` entries.
    ///
    /// In binary mode this emits zero bytes (since `0.0f32` is all
    /// zeros in IEEE 754).  Used for padding when an element type has
    /// no data for a particular field.
    fn write_zeros_f32(&mut self, count: usize) {
        if self.binary {
            // 0.0f32 is all zero bytes in both big and little endian
            let byte_len = count * 4;
            self.scratch.clear();
            self.scratch.resize(byte_len, 0);
            self.writer.write_all(&self.scratch).unwrap();
        } else {
            for _ in 0..count {
                self.writer.write_all(b"0\n").unwrap();
            }
        }
    }

    /// Write a 3×3 zero tensor (9 values, three rows of three).
    fn write_zero_tensor(&mut self) {
        if self.binary {
            self.write_zeros_f32(9);
        } else if self.legacy {
            for _ in 0..3 {
                self.write_legacy_float_ascii(0.0);
                self.writer.write_all(b" ").unwrap();
                self.write_legacy_float_ascii(0.0);
                self.writer.write_all(b" ").unwrap();
                self.write_legacy_float_ascii(0.0);
                self.writer.write_all(b"\n").unwrap();
            }
        } else {
            for _ in 0..3 {
                self.writer.write_all(b"0 0 0\n").unwrap();
            }
        }
    }

    /// Write a plain text header line (terminated by newline).
    fn write_header(&mut self, text: &str) {
        self.writer.write_all(text.as_bytes()).unwrap();
        self.writer.write_all(b"\n").unwrap();
    }

    /// Write a header line assembled from multiple string fragments.
    fn write_header_parts(&mut self, parts: &[&str]) {
        self.scratch.clear();
        for part in parts {
            self.scratch.extend_from_slice(part.as_bytes());
        }
        self.writer.write_all(&self.scratch).unwrap();
        self.writer.write_all(b"\n").unwrap();
    }

    /// Write a header line like `"SCALARS name float 1"`.
    fn write_header_name_suffix(&mut self, prefix: &str, name: &str, suffix: &str) {
        self.scratch.clear();
        self.scratch.extend_from_slice(prefix.as_bytes());
        self.scratch.extend_from_slice(name.as_bytes());
        self.scratch.extend_from_slice(suffix.as_bytes());
        self.writer.write_all(&self.scratch).unwrap();
        self.writer.write_all(b"\n").unwrap();
    }

    /// Write a header line with an embedded integer, e.g. `"POINTS 12345 float"`.
    fn write_header_usize(&mut self, prefix: &str, value: usize, suffix: &str) {
        self.scratch.clear();
        self.scratch.extend_from_slice(prefix.as_bytes());
        let mut buf = [0u8; 20];
        let len = write_u64_fast(&mut buf, value as u64);
        self.scratch.extend_from_slice(&buf[..len]);
        self.scratch.extend_from_slice(suffix.as_bytes());
        self.writer.write_all(&self.scratch).unwrap();
        self.writer.write_all(b"\n").unwrap();
        self.scratch.clear();
    }

    /// Write a header line with two embedded integers, e.g. `"CELLS 100 500"`.
    fn write_header_two_usize(
        &mut self,
        prefix: &str,
        value_a: usize,
        middle: &str,
        value_b: usize,
        suffix: &str,
    ) {
        self.scratch.clear();
        self.scratch.extend_from_slice(prefix.as_bytes());
        let mut buf = [0u8; 20];
        let len_a = write_u64_fast(&mut buf, value_a as u64);
        self.scratch.extend_from_slice(&buf[..len_a]);
        self.scratch.extend_from_slice(middle.as_bytes());
        let len_b = write_u64_fast(&mut buf, value_b as u64);
        self.scratch.extend_from_slice(&buf[..len_b]);
        self.scratch.extend_from_slice(suffix.as_bytes());
        self.writer.write_all(&self.scratch).unwrap();
        self.writer.write_all(b"\n").unwrap();
        self.scratch.clear();
    }

    /// Emit a bare newline (section separator in VTK format).
    fn newline(&mut self) {
        self.writer.write_all(b"\n").unwrap();
    }

    /// Flush all buffered data to the underlying writer.
    fn flush(&mut self) {
        self.writer.flush().unwrap();
    }

    /// Write a space-separated line of `i32` values followed by a newline.
    ///
    /// In ASCII mode, the line is formatted into a small stack buffer
    /// and appended to `scratch`; the scratch buffer is flushed when it
    /// exceeds 64 KB.  In binary mode, delegates to [`write_i32_slice`].
    #[inline]
    fn write_i32_line(&mut self, values: &[i32]) {
        if self.binary {
            self.write_i32_slice(values);
        } else {
            // Max 9 values * 11 chars + 8 spaces + newline = ~108
            // Accumulate into scratch buffer, flush when > 64KB
            const FLUSH_THRESHOLD: usize = 65536;
            let mut line_buf = [0u8; 128];
            let mut pos = 0usize;
            for (i, &v) in values.iter().enumerate() {
                if i > 0 {
                    line_buf[pos] = b' ';
                    pos += 1;
                }
                pos += write_i32_fast(&mut line_buf[pos..], v);
            }
            line_buf[pos] = b'\n';
            pos += 1;
            self.scratch.extend_from_slice(&line_buf[..pos]);
            if self.scratch.len() >= FLUSH_THRESHOLD {
                self.writer.write_all(&self.scratch).unwrap();
                self.scratch.clear();
            }
        }
    }

    /// Flush the scratch buffer to the writer.
    ///
    /// Must be called after a series of [`write_i32_line`] /
    /// [`write_raw`] / [`write_repeated_line`] calls to ensure any
    /// remaining buffered data is written out.
    fn flush_scratch(&mut self) {
        if !self.scratch.is_empty() {
            self.writer.write_all(&self.scratch).unwrap();
            self.scratch.clear();
        }
    }

    /// Append raw bytes to the scratch buffer, flushing when it exceeds 64 KB.
    #[inline]
    fn write_raw(&mut self, data: &[u8]) {
        self.scratch.extend_from_slice(data);
        if self.scratch.len() >= 65536 {
            self.writer.write_all(&self.scratch).unwrap();
            self.scratch.clear();
        }
    }

    /// Repeat the same byte pattern `count` times through the scratch buffer.
    ///
    /// Used for writing constant-valued cell types (e.g. `b"3\n"` for all
    /// 1D elements).
    fn write_repeated_line(&mut self, line: &[u8], count: usize) {
        for _ in 0..count {
            self.scratch.extend_from_slice(line);
            if self.scratch.len() >= 65536 {
                self.writer.write_all(&self.scratch).unwrap();
                self.scratch.clear();
            }
        }
    }
}

// =====================================================================
// Element topology helpers
// =====================================================================
// OpenRadioss stores all 2D elements as quads (4 nodes) and all 3D
// elements as hexahedra (8 nodes).  Degenerate elements (where some
// nodes are repeated) represent triangles and tetrahedra respectively.
// These helpers detect and extract the unique nodes.

/// Count the number of distinct node IDs among 4 quad nodes.
///
/// Returns 3 for a degenerate triangle, 4 for a true quad.
fn unique_count_4(nodes: &[i32]) -> usize {
    let a = nodes[0];
    let b = nodes[1];
    let c = nodes[2];
    let d = nodes[3];

    let mut count = 1usize;
    if b != a {
        count += 1;
    }
    if c != a && c != b {
        count += 1;
    }
    if d != a && d != b && d != c {
        count += 1;
    }
    count
}

/// Try to extract exactly 4 unique node IDs from an 8-node hex.
///
/// If the hex is a degenerate tetrahedron (exactly 4 distinct nodes),
/// returns `Some([a, b, c, d])` with the nodes sorted.  Otherwise
/// returns `None` (the element is a true hexahedron).
fn unique_sorted_4_of_8(nodes: &[i32]) -> Option<[i32; 4]> {
    let mut uniq = [0i32; 4];
    let mut count = 0usize;

    for &n in nodes {
        let mut seen = false;
        for i in 0..count {
            if uniq[i] == n {
                seen = true;
                break;
            }
        }
        if !seen {
            if count == 4 {
                return None;
            }
            uniq[count] = n;
            count += 1;
        }
    }

    if count == 4 {
        uniq.sort_unstable();
        Some(uniq)
    } else {
        None
    }
}

// =====================================================================
// Part / element field output helpers
// =====================================================================

/// Resolve the part ID for element `iel`.
///
/// Part boundaries are stored as a sorted list of element indices in
/// `def_part`.  This function advances `part_index` when `iel` crosses
/// a boundary, then parses the corresponding part-name string as an
/// integer (the part ID used in the VTK output).
fn resolve_part_id(
    iel: usize,           // Element index
    part_index: &mut usize, // Current part index (mutated at boundaries)
    def_part: &[i32],     // Element indices where parts begin
    p_text: &[String],    // Part ID strings (to be parsed as integers)
) -> i32 {
    if *part_index < def_part.len() && iel == def_part[*part_index] as usize {
        *part_index += 1;
    }
    if *part_index < p_text.len() {
        atoi_prefix(&p_text[*part_index])
    } else {
        0
    }
}

/// Parse the leading decimal integer from a string, ignoring any
/// trailing non-digit text.  Mimics the C `atoi()` function.
fn atoi_prefix(text: &str) -> i32 {
    let bytes = text.as_bytes();
    let mut idx = 0;
    while idx < bytes.len() && bytes[idx].is_ascii_whitespace() {
        idx += 1;
    }
    let mut sign: i32 = 1;
    if idx < bytes.len() {
        if bytes[idx] == b'-' {
            sign = -1;
            idx += 1;
        } else if bytes[idx] == b'+' {
            idx += 1;
        }
    }
    let mut value: i32 = 0;
    let mut seen_digit = false;
    while idx < bytes.len() && bytes[idx].is_ascii_digit() {
        seen_digit = true;
        value = value.saturating_mul(10)
            .saturating_add((bytes[idx] - b'0') as i32);
        idx += 1;
    }
    if seen_digit { sign.saturating_mul(value) } else { 0 }
}

/// Write per-cell integer values by concatenating multiple slices.
///
/// The slices correspond to element dimensions (1D, 2D, 3D, SPH) and
/// are written in order.
fn write_cell_i32_values<W: Write>(
    writer: &mut VtkWriter<W>,
    slices: &[&[i32]],
) {
    for slice in slices {
        writer.write_i32_slice(slice);
    }
    writer.newline();
}

/// Write a VTK SCALARS field for one element dimension, zero-padding
/// the others.
///
/// - `counts`: number of elements per dimension `[1D, 2D, 3D, SPH]`.
/// - `active_idx`: index of the dimension that has actual data.
/// - `values`: scalar data for the active dimension.
fn write_elemental_scalar<W: Write>(
    writer: &mut VtkWriter<W>,
    name: &str,
    counts: &[usize],       // [nb_1d, nb_2d, nb_3d, nb_sph]
    active_idx: usize,      // which element type has actual values
    values: &[f32],         // actual values for active element type
) {
    writer.write_header_name_suffix("SCALARS ", name, " float 1");
    writer.write_header("LOOKUP_TABLE default");
    
    for (idx, &count) in counts.iter().enumerate() {
        if idx == active_idx {
            // Use bulk write for the entire slice - more efficient
            writer.write_f32_slice(&values[0..count]);
        } else {
            writer.write_zeros_f32(count);
        }
    }
    writer.newline();
}

/// Write a VTK SCALARS field extracted from strided (interleaved) data.
///
/// Used for 1D torseur components where each element stores 9 values
/// (F1–F3, M1–M6) and we want to output one component at a time.
fn write_elemental_scalar_strided<W: Write>(
    writer: &mut VtkWriter<W>,
    name: &str,
    counts: &[usize],       // [nb_1d, nb_2d, nb_3d, nb_sph]
    active_idx: usize,      // which element type has actual values
    data: &[f32],           // source data array
    stride: usize,          // stride between elements (e.g., 9 for torseur)
    offset: usize,          // offset within stride for this component
    count: usize,           // number of elements
) {
    writer.write_header_name_suffix("SCALARS ", name, " float 1");
    writer.write_header("LOOKUP_TABLE default");
    
    for (idx, &elem_count) in counts.iter().enumerate() {
        if idx == active_idx {
            // Write strided values
            for iel in 0..count {
                writer.write_f32(data[iel * stride + offset]);
            }
        } else {
            writer.write_zeros_f32(elem_count);
        }
    }
    writer.newline();
}

/// Write a VTK TENSORS field from 6-component symmetric tensor data
/// (3D and SPH elements: xx, yy, zz, xy, xz, yz).
///
/// Expands each symmetric tensor into a full 3×3 matrix for VTK.
fn write_symmetric_tensor_6<W: Write>(
    writer: &mut VtkWriter<W>,
    name: &str,
    counts: &[usize],
    active_idx: usize,
    values: &[f32],         // [xx, yy, zz, xy, xz, yz] for each element
) {
    writer.write_header_name_suffix("TENSORS ", name, " float");
    
    for (idx, &count) in counts.iter().enumerate() {
        if idx == active_idx {
            for i in 0..count {
                let base = i * 6;
                let xx = values[base];
                let yy = values[base + 1];
                let zz = values[base + 2];
                let xy = values[base + 3];
                let xz = values[base + 4];
                let yz = values[base + 5];
                
                writer.write_f32_triple(xx, xy, xz);
                writer.write_f32_triple(xy, yy, yz);
                writer.write_f32_triple(xz, yz, zz);
            }
        } else {
            for _ in 0..count {
                writer.write_zero_tensor();
            }
        }
    }
    writer.newline();
}

/// Write a VTK TENSORS field from 3-component symmetric tensor data
/// (2D elements: xx, yy, xy).
///
/// The third row/column is filled with zeros for the 3×3 VTK format.
fn write_symmetric_tensor_3<W: Write>(
    writer: &mut VtkWriter<W>,
    name: &str,
    counts: &[usize],
    active_idx: usize,
    values: &[f32],         // [xx, yy, xy] for each element
) {
    writer.write_header_name_suffix("TENSORS ", name, " float");
    
    for (idx, &count) in counts.iter().enumerate() {
        if idx == active_idx {
            for i in 0..count {
                let base = i * 3;
                let xx = values[base];
                let yy = values[base + 1];
                let xy = values[base + 2];
                
                writer.write_f32_triple(xx, xy, 0.0);
                writer.write_f32_triple(xy, yy, 0.0);
                writer.write_f32_triple(0.0, 0.0, 0.0);
            }
        } else {
            for _ in 0..count {
                writer.write_zero_tensor();
            }
        }
    }
    writer.newline();
}

// =====================================================================
// Main conversion logic
// =====================================================================

/// Read an OpenRadioss animation file and write the corresponding VTK
/// Legacy Unstructured Grid to `writer`.
///
/// The function proceeds in two phases:
/// 1. **Read**: Parse the entire A-file sequentially (2D geometry, 3D,
///    1D, hierarchy, time-history, SPH).
/// 2. **Write**: Emit the VTK header, POINTS, CELLS, CELL_TYPES,
///    POINT_DATA (nodal fields), and CELL_DATA (elemental fields).
fn read_radioss_anim<W: Write>(
    file_name: &str,
    binary_format: bool,
    legacy_format: bool,
    writer: W,
) {
    let input_file = File::open(file_name).unwrap_or_else(|_| {
        eprintln!("Can't open input file {}", file_name);
        process::exit(1);
    });
    let mut inf = BufReader::with_capacity(4 * 1024 * 1024, input_file);

    let mut vtk = VtkWriter::new(writer, binary_format, legacy_format);

    let magic = read_i32(&mut inf);

    match magic {
        // OpenRadioss animation format version 10
        FASTMAGI10 => {
            let a_time = read_f32(&mut inf);
            let _time_text = read_text(&mut inf, 81);
            let _mod_anim_text = read_text(&mut inf, 81);
            let _radioss_run_text = read_text(&mut inf, 81);

            // Feature flags (10 integers):
            //   [0]=mass, [1]=numbering, [2]=3D, [3]=1D,
            //   [4]=hierarchy, [5]=time-history, [7]=SPH
            let flag_a = read_i32_vec(&mut inf, 10);

            // ----- 2D geometry (shells / quads / triangles) -----
            let nb_nodes = read_i32(&mut inf) as usize;
            let nb_facets = read_i32(&mut inf) as usize;
            let nb_parts = read_i32(&mut inf) as usize;
            let nb_func = read_i32(&mut inf) as usize;
            let nb_efunc = read_i32(&mut inf) as usize;
            let nb_vect = read_i32(&mut inf) as usize;
            let nb_tens = read_i32(&mut inf) as usize;
            let nb_skew = read_i32(&mut inf) as usize;

            if nb_skew > 0 {
                // Skew reference frames (read but not included in VTK output)
                let _skew_short = read_u16_vec(&mut inf, nb_skew * 6);
            }

            let coor_a = read_f32_vec(&mut inf, 3 * nb_nodes);

            let mut connect_a: Vec<i32> = Vec::new();
            let mut del_elt_a: Vec<u8> = Vec::new();
            if nb_facets > 0 {
                connect_a = read_i32_vec(&mut inf, nb_facets * 4);
                del_elt_a = read_bytes(&mut inf, nb_facets);
            }

            let mut def_part_a: Vec<i32> = Vec::new();
            let mut p_text_a: Vec<String> = Vec::new();
            if nb_parts > 0 {
                def_part_a = read_i32_vec(&mut inf, nb_parts);
                p_text_a = (0..nb_parts)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
            }

            let _norm_short_a = read_u16_vec(&mut inf, 3 * nb_nodes);

            let mut func_a: Vec<f32> = Vec::new();
            let mut efunc_a: Vec<f32> = Vec::new();
            let mut f_text_a_clean: Vec<String> = Vec::new();
            if nb_func + nb_efunc > 0 {
                f_text_a_clean = (0..nb_func + nb_efunc)
                    .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                    .collect();
                if nb_func > 0 {
                    func_a = read_f32_vec(&mut inf, nb_nodes * nb_func);
                }
                if nb_efunc > 0 {
                    efunc_a = read_f32_vec(&mut inf, nb_facets * nb_efunc);
                }
            }

            let mut v_text_a_clean: Vec<String> = Vec::new();
            if nb_vect > 0 {
                v_text_a_clean = (0..nb_vect)
                    .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                    .collect();
            }
            let vect_val_a = read_f32_vec(&mut inf, 3 * nb_nodes * nb_vect);

            let mut tens_val_a: Vec<f32> = Vec::new();
            let mut t_text_a_clean: Vec<String> = Vec::new();
            if nb_tens > 0 {
                t_text_a_clean = (0..nb_tens)
                    .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                    .collect();
                tens_val_a = read_f32_vec(&mut inf, nb_facets * 3 * nb_tens);
            }

            if flag_a[0] == 1 {
                let _e_mass_a = read_f32_vec(&mut inf, nb_facets);
                let _n_mass_a = read_f32_vec(&mut inf, nb_nodes);
            }

            let mut nod_num_a: Vec<i32> = Vec::new();
            let mut el_num_a: Vec<i32> = Vec::new();
            if flag_a[1] != 0 {
                nod_num_a = read_i32_vec(&mut inf, nb_nodes);
                el_num_a = read_i32_vec(&mut inf, nb_facets);
            }

            if flag_a[4] != 0 {
                let _part2subset_2d = read_i32_vec(&mut inf, nb_parts);
                let _part_material_2d = read_i32_vec(&mut inf, nb_parts);
                let _part_properties_2d = read_i32_vec(&mut inf, nb_parts);
            }

            // ----- 3D geometry (hexahedra / tetrahedra) -----
            let mut nb_elts_3d: usize = 0;
            let mut nb_efunc_3d: usize = 0;
            let mut nb_tens_3d: usize = 0;
            let mut connect_3d: Vec<i32> = Vec::new();
            let mut del_elt_3d: Vec<u8> = Vec::new();
            let mut def_part_3d: Vec<i32> = Vec::new();
            let mut p_text_3d: Vec<String> = Vec::new();
            let mut efunc_3d: Vec<f32> = Vec::new();
            let mut tens_val_3d: Vec<f32> = Vec::new();
            let mut f_text_3d_clean: Vec<String> = Vec::new();
            let mut t_text_3d_clean: Vec<String> = Vec::new();
            let mut el_num_3d: Vec<i32> = Vec::new();

            if flag_a[2] != 0 {
                nb_elts_3d = read_i32(&mut inf) as usize;
                let nb_parts_3d = read_i32(&mut inf) as usize;
                nb_efunc_3d = read_i32(&mut inf) as usize;
                nb_tens_3d = read_i32(&mut inf) as usize;

                connect_3d = read_i32_vec(&mut inf, nb_elts_3d * 8);
                del_elt_3d = read_bytes(&mut inf, nb_elts_3d);

                def_part_3d = read_i32_vec(&mut inf, nb_parts_3d);
                p_text_3d = (0..nb_parts_3d)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();

                if nb_efunc_3d > 0 {
                    f_text_3d_clean = (0..nb_efunc_3d)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    efunc_3d = read_f32_vec(&mut inf, nb_efunc_3d * nb_elts_3d);
                }

                if nb_tens_3d > 0 {
                    t_text_3d_clean = (0..nb_tens_3d)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    tens_val_3d = read_f32_vec(&mut inf, nb_elts_3d * 6 * nb_tens_3d);
                }

                if flag_a[0] == 1 {
                    let _e_mass_3d = read_f32_vec(&mut inf, nb_elts_3d);
                }
                if flag_a[1] == 1 {
                    el_num_3d = read_i32_vec(&mut inf, nb_elts_3d);
                }
                if flag_a[4] != 0 {
                    let _part2subset_3d = read_i32_vec(&mut inf, nb_parts_3d);
                    let _part_material_3d = read_i32_vec(&mut inf, nb_parts_3d);
                    let _part_properties_3d = read_i32_vec(&mut inf, nb_parts_3d);
                }
            }

            // ----- 1D geometry (beams / springs / trusses) -----
            let mut nb_elts_1d: usize = 0;
            let mut nb_efunc_1d: usize = 0;
            let mut nb_tors_1d: usize = 0;
            let mut connect_1d: Vec<i32> = Vec::new();
            let mut del_elt_1d: Vec<u8> = Vec::new();
            let mut def_part_1d: Vec<i32> = Vec::new();
            let mut p_text_1d: Vec<String> = Vec::new();
            let mut efunc_1d: Vec<f32> = Vec::new();
            let mut tors_val_1d: Vec<f32> = Vec::new();
            let mut f_text_1d_clean: Vec<String> = Vec::new();
            let mut t_text_1d_clean: Vec<String> = Vec::new();
            let mut el_num_1d: Vec<i32> = Vec::new();

            if flag_a[3] != 0 {
                nb_elts_1d = read_i32(&mut inf) as usize;
                let nb_parts_1d = read_i32(&mut inf) as usize;
                nb_efunc_1d = read_i32(&mut inf) as usize;
                nb_tors_1d = read_i32(&mut inf) as usize;
                let is_skew_1d = read_i32(&mut inf);

                connect_1d = read_i32_vec(&mut inf, nb_elts_1d * 2);
                del_elt_1d = read_bytes(&mut inf, nb_elts_1d);

                def_part_1d = read_i32_vec(&mut inf, nb_parts_1d);
                p_text_1d = (0..nb_parts_1d)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();

                if nb_efunc_1d > 0 {
                    f_text_1d_clean = (0..nb_efunc_1d)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    efunc_1d = read_f32_vec(&mut inf, nb_efunc_1d * nb_elts_1d);
                }

                if nb_tors_1d > 0 {
                    t_text_1d_clean = (0..nb_tors_1d)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    tors_val_1d = read_f32_vec(&mut inf, nb_elts_1d * 9 * nb_tors_1d);
                }

                if is_skew_1d != 0 {
                    let _elt2_skew_1d = read_i32_vec(&mut inf, nb_elts_1d);
                }
                if flag_a[0] == 1 {
                    let _e_mass_1d = read_f32_vec(&mut inf, nb_elts_1d);
                }
                if flag_a[1] == 1 {
                    el_num_1d = read_i32_vec(&mut inf, nb_elts_1d);
                }
                if flag_a[4] != 0 {
                    let _part2subset_1d = read_i32_vec(&mut inf, nb_parts_1d);
                    let _part_material_1d = read_i32_vec(&mut inf, nb_parts_1d);
                    let _part_properties_1d = read_i32_vec(&mut inf, nb_parts_1d);
                }
            }

            // ----- Part hierarchy (subsets, materials, properties) -----
            if flag_a[4] != 0 {
                let nb_subsets = read_i32(&mut inf) as usize;
                for _ in 0..nb_subsets {
                    let _subset_text = read_text(&mut inf, 50);
                    let _num_parent = read_i32(&mut inf);
                    let nb_subset_son = read_i32(&mut inf) as usize;
                    if nb_subset_son > 0 {
                        let _subset_son = read_i32_vec(&mut inf, nb_subset_son);
                    }
                    let nb_sub_part_2d = read_i32(&mut inf) as usize;
                    if nb_sub_part_2d > 0 {
                        let _sub_part_2d = read_i32_vec(&mut inf, nb_sub_part_2d);
                    }
                    let nb_sub_part_3d = read_i32(&mut inf) as usize;
                    if nb_sub_part_3d > 0 {
                        let _sub_part_3d = read_i32_vec(&mut inf, nb_sub_part_3d);
                    }
                    let nb_sub_part_1d = read_i32(&mut inf) as usize;
                    if nb_sub_part_1d > 0 {
                        let _sub_part_1d = read_i32_vec(&mut inf, nb_sub_part_1d);
                    }
                }

                let nb_materials = read_i32(&mut inf) as usize;
                let nb_properties = read_i32(&mut inf) as usize;
                let _material_texts: Vec<String> = (0..nb_materials)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
                let _material_types = read_i32_vec(&mut inf, nb_materials);
                let _properties_texts: Vec<String> = (0..nb_properties)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
                let _properties_types = read_i32_vec(&mut inf, nb_properties);
            }

            // ----- Time-history node/element references -----
            if flag_a[5] != 0 {
                let nb_nodes_th = read_i32(&mut inf) as usize;
                let nb_elts_2d_th = read_i32(&mut inf) as usize;
                let nb_elts_3d_th = read_i32(&mut inf) as usize;
                let nb_elts_1d_th = read_i32(&mut inf) as usize;

                let _nodes_2th = read_i32_vec(&mut inf, nb_nodes_th);
                let _n2th_texts: Vec<String> = (0..nb_nodes_th)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
                let _elt_2d_th = read_i32_vec(&mut inf, nb_elts_2d_th);
                let _elt_2d_th_texts: Vec<String> = (0..nb_elts_2d_th)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
                let _elt_3d_th = read_i32_vec(&mut inf, nb_elts_3d_th);
                let _elt_3d_th_texts: Vec<String> = (0..nb_elts_3d_th)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
                let _elt_1d_th = read_i32_vec(&mut inf, nb_elts_1d_th);
                let _elt_1d_th_texts: Vec<String> = (0..nb_elts_1d_th)
                    .map(|_| read_text(&mut inf, 50))
                    .collect();
            }

            // ----- SPH particles -----
            let mut nb_elts_sph: usize = 0;
            let mut nb_efunc_sph: usize = 0;
            let mut nb_tens_sph: usize = 0;
            let mut connec_sph: Vec<i32> = Vec::new();
            let mut del_elt_sph: Vec<u8> = Vec::new();
            let mut def_part_sph: Vec<i32> = Vec::new();
            let mut p_text_sph: Vec<String> = Vec::new();
            let mut efunc_sph: Vec<f32> = Vec::new();
            let mut tens_val_sph: Vec<f32> = Vec::new();
            let mut scal_text_sph_clean: Vec<String> = Vec::new();
            let mut tens_text_sph_clean: Vec<String> = Vec::new();
            let mut nod_num_sph: Vec<i32> = Vec::new();

            if flag_a[7] != 0 {
                nb_elts_sph = read_i32(&mut inf) as usize;
                let nb_parts_sph = read_i32(&mut inf) as usize;
                nb_efunc_sph = read_i32(&mut inf) as usize;
                nb_tens_sph = read_i32(&mut inf) as usize;

                if nb_elts_sph > 0 {
                    connec_sph = read_i32_vec(&mut inf, nb_elts_sph);
                    del_elt_sph = read_bytes(&mut inf, nb_elts_sph);
                }
                if nb_parts_sph > 0 {
                    def_part_sph = read_i32_vec(&mut inf, nb_parts_sph);
                    p_text_sph = (0..nb_parts_sph)
                        .map(|_| read_text(&mut inf, 50))
                        .collect();
                }
                if nb_efunc_sph > 0 {
                    scal_text_sph_clean = (0..nb_efunc_sph)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    efunc_sph = read_f32_vec(&mut inf, nb_efunc_sph * nb_elts_sph);
                }
                if nb_tens_sph > 0 {
                    tens_text_sph_clean = (0..nb_tens_sph)
                        .map(|_| replace_underscore(&read_text(&mut inf, 81)))
                        .collect();
                    tens_val_sph = read_f32_vec(&mut inf, nb_elts_sph * nb_tens_sph * 6);
                }
                if flag_a[0] == 1 {
                    let _e_mass_sph = read_f32_vec(&mut inf, nb_elts_sph);
                }
                if flag_a[1] == 1 {
                    nod_num_sph = read_i32_vec(&mut inf, nb_elts_sph);
                }
                if flag_a[4] != 0 {
                    let _num_parent_sph = read_i32_vec(&mut inf, nb_parts_sph);
                    let _mat_part_sph = read_i32_vec(&mut inf, nb_parts_sph);
                    let _prop_part_sph = read_i32_vec(&mut inf, nb_parts_sph);
                }
            }

            // ========== VTK output ==========
            vtk.write_header("# vtk DataFile Version 3.0");
            vtk.write_header("vtk output");
            if binary_format {
                vtk.write_header("BINARY");
            } else {
                vtk.write_header("ASCII");
            }
            vtk.write_header("DATASET UNSTRUCTURED_GRID");

            vtk.write_header("FIELD FieldData 2");
            vtk.write_header("TIME 1 1 double");
            vtk.write_f64(a_time as f64);
            if binary_format {
                vtk.newline();
            }
            vtk.write_header("CYCLE 1 1 int");
            vtk.write_i32(0);
            if binary_format {
                vtk.newline();
            }

            // --- POINTS (node coordinates) ---
            vtk.write_header_usize("POINTS ", nb_nodes, " float");
            if binary_format {
                vtk.write_f32_slice(&coor_a);
            } else {
                for inod in 0..nb_nodes {
                    vtk.write_f32_triple(
                        coor_a[3 * inod],
                        coor_a[3 * inod + 1],
                        coor_a[3 * inod + 2],
                    );
                }
            }
            vtk.newline();

            // --- Detect degenerate elements ---
            // 3D: hexahedra with only 4 unique nodes are tetrahedra
            let mut is_3d_cell_tetrahedron: Vec<bool> = Vec::with_capacity(nb_elts_3d);
            let mut tetra_nodes: Vec<[i32; 4]> = Vec::with_capacity(nb_elts_3d);
            let mut tetrahedron_count: usize = 0;
            for icon in 0..nb_elts_3d {
                let nodes = &connect_3d[icon * 8..icon * 8 + 8];
                if let Some(tet) = unique_sorted_4_of_8(nodes) {
                    is_3d_cell_tetrahedron.push(true);
                    tetra_nodes.push(tet);
                    tetrahedron_count += 1;
                } else {
                    is_3d_cell_tetrahedron.push(false);
                    tetra_nodes.push([0; 4]);
                }
            }

            // 2D: quads with only 3 unique nodes are triangles
            let mut is_2d_triangle: Vec<bool> = Vec::with_capacity(nb_facets);
            let mut _triangle_count: usize = 0;
            for icon in 0..nb_facets {
                let nodes = &connect_a[icon * 4..icon * 4 + 4];
                if unique_count_4(nodes) == 3 {
                    is_2d_triangle.push(true);
                    _triangle_count += 1;
                } else {
                    is_2d_triangle.push(false);
                }
            }

            // --- CELLS (element connectivity) ---
            let total_cells = nb_elts_1d + nb_facets + nb_elts_3d + nb_elts_sph;
            if total_cells > 0 {
                // cells_size = total number of integers in the CELLS section:
                // each cell row has (num_nodes + 1) integers (count prefix + node IDs)
                let cells_size = nb_elts_1d * 3
                    + nb_facets * 5
                    + tetrahedron_count * 5
                    + (nb_elts_3d - tetrahedron_count) * 9
                    + nb_elts_sph * 2;
                vtk.write_header_two_usize("CELLS ", total_cells, " ", cells_size, "");

                if binary_format {
                    // Binary: buffer cells in an i32 Vec, flush every 8192 values
                    let mut cell_buf: Vec<i32> = Vec::with_capacity(8192);
                    let flush_cells = |buf: &mut Vec<i32>, writer: &mut VtkWriter<W>| {
                        if !buf.is_empty() {
                            writer.write_i32_slice(buf);
                            buf.clear();
                        }
                    };
                    // 1D elements
                    for icon in 0..nb_elts_1d {
                        cell_buf.push(2);
                        cell_buf.push(connect_1d[icon * 2]);
                        cell_buf.push(connect_1d[icon * 2 + 1]);
                        if cell_buf.len() >= 8192 {
                            flush_cells(&mut cell_buf, &mut vtk);
                        }
                    }
                    // 2D elements
                    for icon in 0..nb_facets {
                        cell_buf.push(4);
                        cell_buf.push(connect_a[icon * 4]);
                        cell_buf.push(connect_a[icon * 4 + 1]);
                        cell_buf.push(connect_a[icon * 4 + 2]);
                        cell_buf.push(connect_a[icon * 4 + 3]);
                        if cell_buf.len() >= 8192 {
                            flush_cells(&mut cell_buf, &mut vtk);
                        }
                    }
                    // 3D elements
                    for icon in 0..nb_elts_3d {
                        if is_3d_cell_tetrahedron[icon] {
                            let tet = tetra_nodes[icon];
                            cell_buf.push(4);
                            cell_buf.push(tet[0]);
                            cell_buf.push(tet[1]);
                            cell_buf.push(tet[2]);
                            cell_buf.push(tet[3]);
                        } else {
                            cell_buf.push(8);
                            cell_buf.push(connect_3d[icon * 8]);
                            cell_buf.push(connect_3d[icon * 8 + 1]);
                            cell_buf.push(connect_3d[icon * 8 + 2]);
                            cell_buf.push(connect_3d[icon * 8 + 3]);
                            cell_buf.push(connect_3d[icon * 8 + 4]);
                            cell_buf.push(connect_3d[icon * 8 + 5]);
                            cell_buf.push(connect_3d[icon * 8 + 6]);
                            cell_buf.push(connect_3d[icon * 8 + 7]);
                        }
                        if cell_buf.len() >= 8192 {
                            flush_cells(&mut cell_buf, &mut vtk);
                        }
                    }
                    // SPH elements
                    for icon in 0..nb_elts_sph {
                        cell_buf.push(1);
                        cell_buf.push(connec_sph[icon]);
                        if cell_buf.len() >= 8192 {
                            flush_cells(&mut cell_buf, &mut vtk);
                        }
                    }
                    flush_cells(&mut cell_buf, &mut vtk);
                } else {
                    // 1D elements
                    for icon in 0..nb_elts_1d {
                        let vals = [
                            2,
                            connect_1d[icon * 2],
                            connect_1d[icon * 2 + 1],
                        ];
                        vtk.write_i32_line(&vals);
                    }
                    // 2D elements
                    for icon in 0..nb_facets {
                        let vals = [
                            4,
                            connect_a[icon * 4],
                            connect_a[icon * 4 + 1],
                            connect_a[icon * 4 + 2],
                            connect_a[icon * 4 + 3],
                        ];
                        vtk.write_i32_line(&vals);
                    }
                    // 3D elements
                    for icon in 0..nb_elts_3d {
                        if is_3d_cell_tetrahedron[icon] {
                            let tet = tetra_nodes[icon];
                            let vals = [4, tet[0], tet[1], tet[2], tet[3]];
                            vtk.write_i32_line(&vals);
                        } else {
                            let vals = [
                                8,
                                connect_3d[icon * 8],
                                connect_3d[icon * 8 + 1],
                                connect_3d[icon * 8 + 2],
                                connect_3d[icon * 8 + 3],
                                connect_3d[icon * 8 + 4],
                                connect_3d[icon * 8 + 5],
                                connect_3d[icon * 8 + 6],
                                connect_3d[icon * 8 + 7],
                            ];
                            vtk.write_i32_line(&vals);
                        }
                    }
                    // SPH elements
                    for icon in 0..nb_elts_sph {
                        let vals = [1, connec_sph[icon]];
                        vtk.write_i32_line(&vals);
                    }
                    vtk.flush_scratch();
                }
            }
            vtk.newline();

            // --- CELL_TYPES (VTK element type codes) ---
            // 1=vertex, 3=line, 5=triangle, 9=quad, 10=tetra, 12=hexa
            if total_cells > 0 {
                vtk.write_header_usize("CELL_TYPES ", total_cells, "");
                if binary_format {
                    let mut cell_type_buf: Vec<i32> = Vec::with_capacity(8192);
                    for _ in 0..nb_elts_1d {
                        cell_type_buf.push(3);
                        if cell_type_buf.len() == 8192 {
                            vtk.write_i32_slice(&cell_type_buf);
                            cell_type_buf.clear();
                        }
                    }
                    for icon in 0..nb_facets {
                        let val = if is_2d_triangle[icon] { 5 } else { 9 };
                        cell_type_buf.push(val);
                        if cell_type_buf.len() == 8192 {
                            vtk.write_i32_slice(&cell_type_buf);
                            cell_type_buf.clear();
                        }
                    }
                    for icon in 0..nb_elts_3d {
                        let val = if is_3d_cell_tetrahedron[icon] { 10 } else { 12 };
                        cell_type_buf.push(val);
                        if cell_type_buf.len() == 8192 {
                            vtk.write_i32_slice(&cell_type_buf);
                            cell_type_buf.clear();
                        }
                    }
                    for _ in 0..nb_elts_sph {
                        cell_type_buf.push(1);
                        if cell_type_buf.len() == 8192 {
                            vtk.write_i32_slice(&cell_type_buf);
                            cell_type_buf.clear();
                        }
                    }
                    if !cell_type_buf.is_empty() {
                        vtk.write_i32_slice(&cell_type_buf);
                    }
                } else {
                    // ASCII: use pre-formatted byte strings for known constant
                    // cell type codes, avoiding per-value integer-to-string conversion
                    vtk.write_repeated_line(b"3\n", nb_elts_1d);
                    for icon in 0..nb_facets {
                        if is_2d_triangle[icon] {
                            vtk.write_raw(b"5\n");
                        } else {
                            vtk.write_raw(b"9\n");
                        }
                    }
                    for icon in 0..nb_elts_3d {
                        if is_3d_cell_tetrahedron[icon] {
                            vtk.write_raw(b"10\n");
                        } else {
                            vtk.write_raw(b"12\n");
                        }
                    }
                    vtk.write_repeated_line(b"1\n", nb_elts_sph);
                    vtk.flush_scratch();
                }
            }
            vtk.newline();

            // --- POINT_DATA (nodal fields) ---
            vtk.write_header_usize("POINT_DATA ", nb_nodes, "");

            // Node IDs
            vtk.write_header("SCALARS NODE_ID int 1");
            vtk.write_header("LOOKUP_TABLE default");
            vtk.write_i32_slice(&nod_num_a);
            vtk.newline();

            for ifun in 0..nb_func {
                let name = &f_text_a_clean[ifun];
                vtk.write_header_parts(&["SCALARS ", name, " float 1"]);
                vtk.write_header("LOOKUP_TABLE default");
                for inod in 0..nb_nodes {
                    vtk.write_f32(func_a[ifun * nb_nodes + inod]);
                }
                vtk.newline();
            }

            for ivect in 0..nb_vect {
                let name = &v_text_a_clean[ivect];
                vtk.write_header_parts(&["VECTORS ", name, " float"]);
                if binary_format {
                    let start = ivect * 3 * nb_nodes;
                    let end = start + 3 * nb_nodes;
                    vtk.write_f32_slice(&vect_val_a[start..end]);
                } else {
                    for inod in 0..nb_nodes {
                        vtk.write_f32_triple(
                            vect_val_a[3 * inod + ivect * 3 * nb_nodes],
                            vect_val_a[3 * inod + 1 + ivect * 3 * nb_nodes],
                            vect_val_a[3 * inod + 2 + ivect * 3 * nb_nodes],
                        );
                    }
                }
                vtk.newline();
            }

            // --- CELL_DATA (elemental fields) ---
            vtk.write_header_usize("CELL_DATA ", total_cells, "");

            // Element IDs
            vtk.write_header("SCALARS ELEMENT_ID int 1");
            vtk.write_header("LOOKUP_TABLE default");
            write_cell_i32_values(&mut vtk, &[&el_num_1d, &el_num_a, &el_num_3d, &nod_num_sph]);

            // Part IDs (resolved from part boundary tables)
            vtk.write_header("SCALARS PART_ID int 1");
            vtk.write_header("LOOKUP_TABLE default");

            let mut part_1d_index: usize = 0;
            let mut part_2d_index: usize = 0;
            let mut part_3d_index: usize = 0;
            let mut part_0d_index: usize = 0;

            let mut part_buf: Vec<i32> = Vec::with_capacity(8192);
            for iel in 0..nb_elts_1d {
                let part_id = resolve_part_id(iel, &mut part_1d_index, &def_part_1d, &p_text_1d);
                part_buf.push(part_id);
                if part_buf.len() == 8192 {
                    vtk.write_i32_slice(&part_buf);
                    part_buf.clear();
                }
            }
            for iel in 0..nb_facets {
                let part_id = resolve_part_id(iel, &mut part_2d_index, &def_part_a, &p_text_a);
                part_buf.push(part_id);
                if part_buf.len() == 8192 {
                    vtk.write_i32_slice(&part_buf);
                    part_buf.clear();
                }
            }
            for iel in 0..nb_elts_3d {
                let part_id = resolve_part_id(iel, &mut part_3d_index, &def_part_3d, &p_text_3d);
                part_buf.push(part_id);
                if part_buf.len() == 8192 {
                    vtk.write_i32_slice(&part_buf);
                    part_buf.clear();
                }
            }
            for iel in 0..nb_elts_sph {
                let part_id = resolve_part_id(iel, &mut part_0d_index, &def_part_sph, &p_text_sph);
                part_buf.push(part_id);
                if part_buf.len() == 8192 {
                    vtk.write_i32_slice(&part_buf);
                    part_buf.clear();
                }
            }
            if !part_buf.is_empty() {
                vtk.write_i32_slice(&part_buf);
            }
            vtk.newline();

            // Erosion status (0 = active, 1 = eroded/deleted)
            vtk.write_header("SCALARS EROSION_STATUS int 1");
            vtk.write_header("LOOKUP_TABLE default");
            let to_erosion_status = |v: u8| if v == 1 { 1 } else { 0 };
            let mut erosion_buf: Vec<i32> = Vec::with_capacity(8192);
            for iel in 0..nb_elts_1d {
                erosion_buf.push(to_erosion_status(del_elt_1d[iel]));
                if erosion_buf.len() == 8192 {
                    vtk.write_i32_slice(&erosion_buf);
                    erosion_buf.clear();
                }
            }
            for iel in 0..nb_facets {
                erosion_buf.push(to_erosion_status(del_elt_a[iel]));
                if erosion_buf.len() == 8192 {
                    vtk.write_i32_slice(&erosion_buf);
                    erosion_buf.clear();
                }
            }
            for iel in 0..nb_elts_3d {
                erosion_buf.push(to_erosion_status(del_elt_3d[iel]));
                if erosion_buf.len() == 8192 {
                    vtk.write_i32_slice(&erosion_buf);
                    erosion_buf.clear();
                }
            }
            for iel in 0..nb_elts_sph {
                erosion_buf.push(to_erosion_status(del_elt_sph[iel]));
                if erosion_buf.len() == 8192 {
                    vtk.write_i32_slice(&erosion_buf);
                    erosion_buf.clear();
                }
            }
            if !erosion_buf.is_empty() {
                vtk.write_i32_slice(&erosion_buf);
            }
            vtk.newline();

            // 1D elemental scalar fields
            let counts = [nb_elts_1d, nb_facets, nb_elts_3d, nb_elts_sph];
            for iefun in 0..nb_efunc_1d {
                let name = &f_text_1d_clean[iefun];
                let start = iefun * nb_elts_1d;
                let end = start + nb_elts_1d;
                write_elemental_scalar(&mut vtk, &format!("1DELEM_{}", name), &counts, 0, &efunc_1d[start..end]);
            }

            // 1D beam torseur (forces F1-F3, moments M1-M6)
            let tors_suffixes = ["F1", "F2", "F3", "M1", "M2", "M3", "M4", "M5", "M6"];
            for iefun in 0..nb_tors_1d {
                let name = &t_text_1d_clean[iefun];
                let base_offset = 9 * iefun * nb_elts_1d;
                for j in 0..9usize {
                    write_elemental_scalar_strided(
                        &mut vtk,
                        &format!("1DELEM_{}{}", name, tors_suffixes[j]),
                        &counts,
                        0,
                        &tors_val_1d[base_offset..],
                        9,  // stride
                        j,  // offset within stride
                        nb_elts_1d,
                    );
                }
            }

            // 2D elemental scalar fields
            for iefun in 0..nb_efunc {
                let name = &f_text_a_clean[iefun + nb_func];
                let start = iefun * nb_facets;
                let end = start + nb_facets;
                write_elemental_scalar(&mut vtk, &format!("2DELEM_{}", name), &counts, 1, &efunc_a[start..end]);
            }

            // 2D symmetric tensors (xx, yy, xy)
            for ietens in 0..nb_tens {
                let name = &t_text_a_clean[ietens];
                let start = ietens * 3 * nb_facets;
                let end = start + 3 * nb_facets;
                write_symmetric_tensor_3(&mut vtk, &format!("2DELEM_{}", name), &counts, 1, &tens_val_a[start..end]);
            }

            // 3D elemental scalar fields
            for iefun in 0..nb_efunc_3d {
                let name = &f_text_3d_clean[iefun];
                let start = iefun * nb_elts_3d;
                let end = start + nb_elts_3d;
                write_elemental_scalar(&mut vtk, &format!("3DELEM_{}", name), &counts, 2, &efunc_3d[start..end]);
            }

            // 3D symmetric tensors (xx, yy, zz, xy, xz, yz)
            for ietens in 0..nb_tens_3d {
                let name = &t_text_3d_clean[ietens];
                let start = ietens * 6 * nb_elts_3d;
                let end = start + 6 * nb_elts_3d;
                write_symmetric_tensor_6(&mut vtk, &format!("3DELEM_{}", name), &counts, 2, &tens_val_3d[start..end]);
            }

            // SPH elemental scalar and tensor fields
            if flag_a[7] != 0 {
                for iefun in 0..nb_efunc_sph {
                    let name = &scal_text_sph_clean[iefun];
                    let start = iefun * nb_elts_sph;
                    let end = start + nb_elts_sph;
                    write_elemental_scalar(&mut vtk, &format!("SPHELEM_{}", name), &counts, 3, &efunc_sph[start..end]);
                }

                for ietens in 0..nb_tens_sph {
                    let name = &tens_text_sph_clean[ietens];
                    let start = ietens * 6 * nb_elts_sph;
                    let end = start + 6 * nb_elts_sph;
                    write_symmetric_tensor_6(&mut vtk, &format!("SPHELEM_{}", name), &counts, 3, &tens_val_sph[start..end]);
                }
            }

            vtk.flush();
        }

        _ => {
            eprintln!("Error in Anim Files version");
            process::exit(1);
        }
    }
}

// =====================================================================
// Entry point
// =====================================================================

/// Parse command-line arguments, validate input files, and launch
/// conversion threads.
///
/// Files are processed in parallel using a channel-based thread pool.
/// The number of threads is automatically limited to avoid exceeding
/// available memory.
fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <filename1> [filename2 ...] [--binary] [--threads N]", args[0]);
        eprintln!("  --binary : Output in binary VTK format (default is ASCII)");
        eprintln!("  --legacy : Match C++ ASCII float formatting (default uses fast shortest)");
        eprintln!("  --threads N : Override number of worker threads");
        eprintln!("  Output files will have .vtk extension added automatically");
        eprintln!("  Input files must have no extension and end with an uppercase letter followed by 3-4 digits");
        process::exit(1);
    }
    
    // Check if --binary flag is present
    let binary_format = args.iter().any(|arg| arg == "--binary" || arg == "-b");
    let legacy_format = args.iter().any(|arg| arg == "--legacy" || arg == "-l");
    let mut threads_override: Option<usize> = None;
    let mut idx = 1usize;
    while idx < args.len() {
        if args[idx] == "--threads" {
            if idx + 1 >= args.len() {
                eprintln!("Error: --threads requires a value");
                process::exit(1);
            }
            let val = args[idx + 1].parse::<usize>().unwrap_or(0);
            if val == 0 {
                eprintln!("Error: --threads value must be >= 1");
                process::exit(1);
            }
            threads_override = Some(val);
            idx += 2;
        } else {
            idx += 1;
        }
    }
    
    // Collect all input files (skip program name and --binary flag)
    let mut input_files: Vec<String> = args[1..]
        .iter()
        .filter(|arg| {
            *arg != "--binary"
                && *arg != "-b"
                && *arg != "--legacy"
                && *arg != "-l"
                && *arg != "--threads"
                && !arg.parse::<usize>().is_ok()
        })
        .cloned()
        .collect();

    // Filter out files with extensions and enforce the OpenRadioss
    // animation filename convention: must end with an uppercase letter
    // followed by 3 or 4 digits (e.g. "modelA001" or "modelA0001").
    let mut invalid_files: Vec<String> = Vec::new();
    input_files.retain(|file_name| {
        let filename = Path::new(file_name.as_str())
            .file_name()
            .and_then(|s| s.to_str())
            .unwrap_or("");

        let has_extension = filename.contains('.');
        if has_extension {
            invalid_files.push(file_name.clone());
            return false;
        }

        let valid_suffix = if filename.len() >= 4 {
            let suffix_4 = &filename[filename.len() - 4..];
            (suffix_4.chars().next().map(|c| c.is_ascii_uppercase()).unwrap_or(false)
                && suffix_4[1..].chars().all(|c| c.is_ascii_digit()))
                || (filename.len() >= 5
                    && {
                        let suffix_5 = &filename[filename.len() - 5..];
                        suffix_5.chars().next().map(|c| c.is_ascii_uppercase()).unwrap_or(false)
                            && suffix_5[1..].chars().all(|c| c.is_ascii_digit())
                    })
        } else {
            false
        };

        if !valid_suffix {
            invalid_files.push(file_name.clone());
            return false;
        }

        true
    });

    if !invalid_files.is_empty() {
        eprintln!("Warning: Skipping invalid input files:");
        for file in &invalid_files {
            eprintln!("  - {}", file);
        }
    }
    
    if input_files.is_empty() {
        eprintln!("Error: No valid input files specified");
        process::exit(1);
    }
    
    // Process each input file
    let mut failed_files: Vec<String> = Vec::new();
    let mut successful_files = 0;
    
    if binary_format && legacy_format {
        eprintln!("Warning: --legacy has no effect with --binary");
    }

    let mut jobs: Vec<(String, u64)> = Vec::new();
    for file_name in input_files {
        let file_path = std::path::Path::new(file_name.as_str());
        if !file_path.exists() {
            eprintln!("Error: Input file {} does not exist", file_name);
            failed_files.push(file_name);
            continue;
        }
        let size = match file_path.metadata() {
            Ok(meta) => meta.len(),
            Err(e) => {
                eprintln!("Error: Can't read metadata for {}: {}", file_name, e);
                failed_files.push(file_name);
                continue;
            }
        };
        jobs.push((file_name, size));
    }

    if jobs.is_empty() {
        eprintln!("Error: No valid input files to process");
        process::exit(1);
    }

    let file_sizes: Vec<u64> = jobs.iter().map(|(_, size)| *size).collect();
    let mut max_threads = compute_max_threads(&file_sizes);
    if let Some(override_threads) = threads_override {
        let clamped = override_threads.min(jobs.len()).max(1);
        max_threads = clamped;
        eprintln!("Using {} thread(s) (override)", max_threads);
    } else {
        if let Some(mem) = mem_available_bytes() {
            eprintln!("Using {} thread(s) (memory available: {:.2} GB)", max_threads, mem as f64 / 1_073_741_824.0);
        } else {
            eprintln!("Using {} thread(s) (memory available: unknown)", max_threads);
        }
    }
    

    // Dispatch files to worker threads via a shared channel.
    // Each thread pulls files from the channel until it is empty.
    let (job_tx, job_rx) = mpsc::channel::<(String, u64)>();
    for job in jobs {
        job_tx.send(job).unwrap();
    }
    drop(job_tx);

    let mut handles = Vec::new();
    let job_rx = Arc::new(Mutex::new(job_rx));
    for _ in 0..max_threads {
        let rx = Arc::clone(&job_rx);
        let handle = thread::spawn(move || {
            let mut local_success = 0usize;
            let mut local_failed: Vec<String> = Vec::new();
            loop {
                let job = {
                    let guard = rx.lock().unwrap();
                    guard.recv().ok()
                };
                let (file_name, _size) = match job {
                    Some(v) => v,
                    None => break,
                };
                let output_file_name = format!("{}.vtk", file_name);
                let output_file = match File::create(&output_file_name) {
                    Ok(f) => f,
                    Err(e) => {
                        eprintln!("Error: Can't create output file {}: {}", output_file_name, e);
                        local_failed.push(file_name);
                        continue;
                    }
                };
                eprintln!("Converting {} to {}", file_name, output_file_name);
                read_radioss_anim(&file_name, binary_format, legacy_format, output_file);
                local_success += 1;
            }
            (local_success, local_failed)
        });
        handles.push(handle);
    }

    for handle in handles {
        let (local_success, local_failed) = handle.join().unwrap();
        successful_files += local_success;
        failed_files.extend(local_failed);
    }
    
    // Report results
    if !failed_files.is_empty() {
        eprintln!("\nConversion summary: {} succeeded, {} failed", successful_files, failed_files.len());
        eprintln!("Failed files:");
        for file in &failed_files {
            eprintln!("  - {}", file);
        }
        process::exit(1);
    } else if successful_files > 1 {
        eprintln!("\nConversion complete: {} files converted successfully", successful_files);
    }
}
