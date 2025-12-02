echo off

if not exist ..\..\..\exec (
  echo "--- Creating exec directory"
  mkdir ..\..\..\exec
)

cl -DWIN32 /Fe..\..\..\exec\anim_to_vtk_win64.exe ..\src\anim_to_vtk.cpp Ws2_32.lib

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
