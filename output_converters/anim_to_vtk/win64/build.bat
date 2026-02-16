echo off

if not exist ..\..\..\exec (
  echo "--- Creating exec directory"
  mkdir ..\..\..\exec
)

cd ..
cargo build --release

set error_var=%errorlevel%
if %error_var%==0 (
  copy target\release\anim_to_vtk.exe ..\..\..\exec\anim_to_vtk_win64.exe
  echo.
  echo Build succeeded
  echo.
  exit /b %error_var%
) else (
  echo.
  echo Build failed
  echo.
  exit /b %error_var%
)
