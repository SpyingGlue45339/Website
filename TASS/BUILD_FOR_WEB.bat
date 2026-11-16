@echo off
setlocal
cd /d "%~dp0"
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

if exist "Llama_Space_Programme\build" (
    echo Removing the previous browser build so this run uses the new source...
    rmdir /s /q "Llama_Space_Programme\build"
)

echo ============================================================
echo BUILDING TOTALLY ACCURATE SPACEFLIGHT SIMULATOR
echo ============================================================
echo.
echo Source folder: Llama_Space_Programme
echo.
python -m pygbag --build --ume_block=1 --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
if errorlevel 1 (
    echo.
    echo BUILD FAILED. Please keep this window open and send me the error.
    pause
    exit /b 1
)
echo.
echo BUILD COMPLETE.
echo Web files created in:
echo %~dp0Llama_Space_Programme\build\web\
echo.
echo For GitHub Pages, copy the CONTENTS of build\web into Website\TASS\game\
pause
