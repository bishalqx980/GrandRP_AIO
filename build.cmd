@echo off
color a
setlocal
set "INFO=[+]"

echo ================================
echo         App Builder
echo ================================
echo.

color 4

set /p APP_NAME=App Name:

set ICON_PATH="icon.ico"

color 2

echo %INFO% installing dependencies...

start "" /wait cmd /c "pip install -r requirements.txt"
start "" /wait cmd /c "pip install pyinstaller"

echo %INFO% dependencies installed successfully.

echo.
echo %INFO% Building executable...

pyinstaller ^
--clean ^
--onefile ^
--noconsole ^
--uac-admin ^
--add-data "icon.ico;." ^
--icon=%ICON_PATH% ^
--name=%APP_NAME% ^
app\__main__.py

echo.
echo %INFO% Build complete!
pause
