echo off

rem create OpenRadioss_GUI folder in AppData : settings and cache will be stored here
if not exist C:\Users\%USERNAME%\AppData\Local\OpenRadioss_GUI (
    mkdir C:\Users\%USERNAME%\AppData\Local\OpenRadioss_GUI
)
set PYTHONPYCACHEPREFIX=C:\Users\%USERNAME%\AppData\Local\OpenRadioss_GUI\__pycache__

python ./Openradioss_gui.py

set PYTHONPYCACHEPREFIX=