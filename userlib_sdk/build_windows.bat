echo OFF

REM Copyright>  Copyright 1986-2023 Altair Engineering Inc.  
REM Copyright> 
REM Copyright>  Permission is hereby granted, free of charge, to any person obtaining 
REM Copyright>  a copy of this software and associated documentation files (the "Software"), 
REM Copyright>  to deal in the Software without restriction, including without limitation 
REM Copyright>  the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
REM Copyright>  sell copies of the Software, and to permit persons to whom the Software is 
REM Copyright>  furnished to do so, subject to the following conditions:
REM Copyright> 
REM Copyright>  The above copyright notice and this permission notice shall be included in all 
REM Copyright>  copies or substantial portions of the Software.
REM Copyright> 
REM Copyright>  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
REM Copyright>  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
REM Copyright>  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
REM Copyright>  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIAsBILITY, 
REM Copyright>  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
REM Copyright>  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

REM Variable setting
REM ----------------
set arch=win64
set prec=dp
set compiler=oneapi
set verbose=
set clean=0

REM Command Line Argument parsing
REM -----------------------------
IF (%1) == () GOTO ERROR

:ARG_LOOP
IF (%1) == () GOTO END_ARG_LOOP

   IF %1==-arch (
       set arch=%2
    )

   IF %1==-prec (
       set prec=%2
    )

   IF %1==-compiler (
        set compiler=%2
    )

   IF %1==-verbose (
        set verbose=-v
    )

   IF %1==-clean (
        set clean=1
    )

SHIFT
GOTO ARG_LOOP

:END_ARG_LOOP

REM Build directory
set build_directory=cbuild_%arch%_%compiler%_%prec%_ninja

if %prec%==sp ( 
    set sdk_directory=%arch%_sp_%compiler%
) else (
    set sdk_directory=%arch%_%compiler%
)

Rem clean
if %clean%==1 (
  echo.
  echo Cleaning %build_directory%
  RMDIR /S /Q %build_directory%
  goto END_SCRIPT
)


REM Print build informations
REM ------------------------

echo.
echo Build Radioss(TM) Userlib SDK
echo ------------------------------
echo Build Arguments :
echo arch=             %arch%
echo compiler=         %compiler%
echo build_directoty   %build_directory%
echo sdk_directory     %sdk_directory%
echo.


if exist %build_directory% (
  cd  %build_directory%
) else (
  mkdir %build_directory%
  cd  %build_directory%
)

call ..\source\Cmake_Compilers\cmake_%compiler%_compilers.bat

cmake -G Ninja -Darch=%arch% -Dcompiler=%compiler% -Dprecision=%prec% -DCMAKE_Fortran_COMPILER=%fcomp% -DCMAKE_C_COMPILER=%ccomp% ..\source
ninja %verbose% 

copy *.lib ..\userlib_sdk\%sdk_directory% >nul 2>nul
copy *.a ..\userlib_sdk\%sdk_directory% >nul 2>nul
copy *.mod ..\userlib_sdk\%sdk_directory% >nul

cd ..
goto END_SCRIPT

:ERROR

  echo.
  echo  Userlib_sdk build script 
  echo -------------------------
  echo.
  echo  Use with arguments : 
  echo  -arch=[linux64, linuxa64, win64]
  echo  -compiler=[armflang, gfortran, intel]
  echo             Defaults :
  echo               linux64  : gfortran
  echo               win64    : oneapi
  echo               linuxa64 : gfortran
  echo  -prec=[dp, sp]
  echo               set precision - dp (default), sp
  echo.
  echo  -verbose : Build verbose mode.
  echo  -clean : delete build
  echo.
  echo.

:END_SCRIPT


set arch=
set prec=
set compiler=
set verbose=
set clean=

echo Terminating
echo.


