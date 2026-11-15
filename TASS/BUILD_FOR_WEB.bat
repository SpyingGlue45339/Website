@echo off
setlocal
cd /d "%~dp0"
echo Building the browser version of Totally Accurate Spaceflight Simulator...
python -m pygbag --build --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
if errorlevel 1 (
    echo.
    echo The build failed. Check the error messages above.
    pause
    exit /b 1
)
echo.
echo Build complete.
echo Your website files are in:
echo Llama_Space_Programme\build\web\
echo Copy the CONTENTS of that folder into your website's game folder.
pause
