# anim_to_vtk

anim_to_vtk is an external tool to convert OpenRadioss animation files to legacy VTK format (ASCII or binary).

## How to build

A Rust toolchain installation is required. Install from https://rustup.rs/

### Linux

Enter the platform directory : anim_to_vtk/linux64
Apply the build script : ./build.bash

Executable will be copied in [OpenRadioss]/exec directory

### Linux ARM64

Enter the platform directory : anim_to_vtk/linuxa64
Apply the build script : ./build.bash

Executable will be copied in [OpenRadioss]/exec directory

### Windows

Enter the platform directory : anim_to_vtk/win64
Apply the script : build.bat

Executable is copied in [OpenRadioss]/exec

### Using Cargo directly

From the anim_to_vtk directory:

        cargo build --release

The executable will be in target/release/anim_to_vtk (or target\release\anim_to_vtk.exe on Windows).

## How to use

### Basic Usage

The tool automatically creates output files with `.vtk` extension added to the input filename.

#### Convert a single file

Generate ASCII VTK format (default):

        ./anim_to_vtk_linux64_gf [Deck Rootname]A001

This creates `[Deck Rootname]A001.vtk`

To generate binary VTK format (smaller file size, faster I/O), use the `--binary` flag:

        ./anim_to_vtk_linux64_gf [Deck Rootname]A001 --binary

To match the legacy C++ ASCII float formatting, use `--legacy` (ASCII only):

        ./anim_to_vtk_linux64_gf [Deck Rootname]A001 --legacy

#### Convert multiple files

You can convert multiple files in a single command:

        ./anim_to_vtk_linux64_gf [Deck Rootname]A001 [Deck Rootname]A002 [Deck Rootname]A003

Or with binary format:

        ./anim_to_vtk_linux64_gf [Deck Rootname]A001 [Deck Rootname]A002 [Deck Rootname]A003 --binary

The `--binary` and `--legacy` flags can be placed anywhere in the command line arguments.

#### Convert all animation files using wildcards

Using shell wildcards to convert all animation files at once:

        ./anim_to_vtk_linux64_gf [Deck Rootname]A*

Or with binary format:

        ./anim_to_vtk_linux64_gf [Deck Rootname]A* --binary

### Legacy Batch Conversion Script (Optional)

The following Linux bash script can still be used for more complex batch processing:

        #!/bin/bash
        #
        # Script to be launched in Animation file directory
        #
        Rootname=[Deck Rootname]
        OpenRadioss_root=[Path to OpenRadioss installation]
        # Use "--binary" for binary VTK or leave empty for ASCII VTK
        FORMAT="--binary"
        ${OpenRadioss_root}/exec/anim_to_vtk_linuxa64_gf ${Rootname}A* ${FORMAT}

In Paraview, the vtk files are bundled and can be loaded in one step.

### Output Format Options

- **ASCII format** (default): Human-readable text format, larger file size
- **Binary format** (`--binary` or `-b` flag): Compact binary format with approximately 70-80% smaller file size and faster loading times in visualization software
- **Legacy formatting** (`--legacy` or `-l` flag): C++-compatible ASCII float formatting to match historical VTK output

## Performance

The Rust implementation is significantly faster than previous C++ implementations due to:
- Specialized number formatting libraries (ryu, itoa)
- Efficient buffered I/O strategy
- Zero-allocation data processing
- Reusable scratch buffers

For detailed performance analysis and optimization techniques, see [PERFORMANCE.md](PERFORMANCE.md).
