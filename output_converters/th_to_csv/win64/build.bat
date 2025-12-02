echo off
setlocal
if not exist ..\..\..\exec (
  echo "--- Creating exec directory"
  mkdir ..\..\..\exec
)

cl /Fe..\..\..\exec\th_to_csv_win64.exe ..\src\th_to_csv.c

set error_var=%errorlevel%
if %error_var%==0 (
  echo.
  echo Build succeeded
  echo.
  endlocal
  del *.obj
  exit /b %error_var%
) else (
  echo.
  echo Build failed
  echo.
  endlocal
  exit /b %error_var%
)

