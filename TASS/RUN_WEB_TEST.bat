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
echo RUNNING LOCAL BROWSER TEST
echo ============================================================
echo.
echo Pygbag will build/serve the Llama_Space_Programme folder.
echo First click the Pygbag page prompt if it asks to enable browser media.
echo Then click START on the game's title screen.
echo Open http://localhost:8000 in Chrome or Edge.
echo Keep this window open while testing.
echo Press Ctrl+C here to stop the server.
echo.
python -m pygbag --ume_block=1 --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
if errorlevel 1 (
    echo.
    echo LOCAL TEST FAILED. Send me the final error lines from this window.
    pause
)
