echo off

REM Copyright 1986-2023 Altair Engineering Inc.  
REM 
REM Permission is hereby granted, free of charge, to any person obtaining 
REM a copy of this software and associated documentation files (the "Software"), 
REM to deal in the Software without restriction, including without limitation 
REM the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or 
REM sell copies of the Software, and to permit persons to whom the Software is 
REM furnished to do so, subject to the following conditions:
REM 
REM The above copyright notice and this permission notice shall be included in all 
REM copies or substantial portions of the Software.
REM 
REM THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
REM IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
REM FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
REM AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
REM WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR 
REM IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


echo.
echo.
echo *********************************************
echo ** Generating Radioss Dynamic User Library **
echo **            Win64 Intel                  **
echo **            Single Precision             **
echo *********************************************
echo.

REM -------------------------------
REM Checking command line arguments
REM -------------------------------

set starter="none"
set engine="none"
set library="none"
set outfile="none"
set addflag=" "
set link_flags=" "
set free="no"
set freeflag="" 

set libname=libraduser_win64_sp.dll

IF (%1) == () GOTO ERROR

:ARG_LOOP

IF (%1) == () GOTO END_ARG_LOOP

  if %1==/STARTER (
     set starter=%2
  )

  if %1==/ENGINE (
     set engine=%2
  )

  if %1==/LIBRARY (
     set library=%2
  )

  if %1==/OUTFILE (
     set outfile=%2
  )
  
  if %1==/ADDFLAG (
     set addflag=%2
  )

  if %1==/FREE (
     set free="yes"
  )

  if %1==/LINK_FLAGS (
     set link_flags=%2
  )

 
SHIFT
GOTO ARG_LOOP

:END_ARG_LOOP


if %free% == "yes" ( set freeflag=/FREE )
if %outfile% == "none"  GOTO START

set libname=%outfile%

:START
set starter=%starter:~1,-1%
set engine=%engine:~1,-1%
set library=%library:~1,-1%
set addflag=%addflag:~1,-1%
set link_flags=%link_flags:~1,-1%


if EXIST %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\libraduser_win64_sp_intel.lib  (

echo.
echo.
echo Preparing Library
echo -----------------
echo.
echo.
mkdir _obj_win64
cd _obj_win64

lib -list %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\libraduser_win64_sp_intel.lib | findstr /c:.obj > liblist.txt
FOR /f %%f IN ('type liblist.txt') DO LIB /NOLOGO /EXTRACT:%%f %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\libraduser_win64_sp_intel.lib

) ELSE (
echo.
echo.
echo *** ERROR
echo.
echo %RAD_USERLIB_SDK_PATH%\%RAD_USERLIB_ARCH%\libraduser_win64_sp_intel.lib 
echo.
echo not found
echo.
echo Check environment variables:
echo.
echo RAD_USERLIB_SDK_PATH
echo RAD_USERLIB_ARCH

GOTO END
)

:LIBRARY
if "%library%" == "none" GOTO STARTER

echo.
echo adding %library% in library
echo -----------------------------
echo.
FOR %%l IN (%library%) DO (
cd ..
echo %%l
copy %%l _obj_win64
cd  _obj_win64
lib -list %%l | findstr /c:.obj > librarylist.txt
FOR /f %%f IN ('type librarylist.txt') DO LIB /NOLOGO /EXTRACT:%%f %%l
)


:STARTER
if "%starter%" == "none" GOTO ENGINE

echo.
echo.
echo Compiling: %starter%
echo ----------
echo.
FOR  %%f IN (%starter%) DO (
  echo %%f
  ifx /nologo %freeflag% /MODULE:%RAD_USERLIB_SDK_PATH%/%RAD_USERLIB_ARCH% /fpp /Qaxsse3 /Qimf-use-svml:true /align:array64byte /Qopenmp /O2 /fp:precise /Qftz /extend-source %addflag% -DMYREAL8 -DR8 /c ..\%%f
  echo.
)

:ENGINE
if "%engine%" == "none" GOTO :LINK
echo.
echo.
echo Compiling: %engine%
echo ----------
echo.
FOR  %%f IN (%engine%) DO (
   echo %%f
   ifx /nologo %freeflag% /MODULE:%RAD_USERLIB_SDK_PATH%/%RAD_USERLIB_ARCH% /fpp /Qaxsse3 /Qimf-use-svml:true /align:array64byte /Qopenmp /O3 /fp:precise /Qftz /extend-source %addflag% -DMYREAL8 -DR8 /c ..\%%f
   echo.
)

:LINK
echo.
echo.
echo Creating library: %libname%
echo ----------------
echo.

cd ..
ifx /nologo /DLL /MT -o %libname%  _obj_win64/*.obj  %link_flags%
del /q _obj_win64\*.*
rmdir _obj_win64


GOTO :END


:ERROR
echo.
echo Script Usage:
echo.
echo build_userlib_win64.bat /STARTER "Starter source files" /ENGINE "Engine Source files " [Optional Argument]
echo.
echo [Optional Argument]
echo.
echo /LIBRARY "additional static Library"
echo /OUTFILE "Library_name"
echo.
echo /FREE  : Source code is in Fortran 90 Free Format
echo /ADDFLAG "Additional compiler Flags" : Additional compiler flags to set
echo /LINK_FLAGS "Additional link flags"  : add link Flags like library files to link with.
echo.
:END
echo.
echo Done
echo ----
echo.
echo.
