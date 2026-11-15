@echo off
setlocal
cd /d "%~dp0"
echo Starting the local browser test server...
echo When the server is ready, open http://localhost:8000 in Chrome or Edge.
echo Press Ctrl+C in this window to stop the server.
python -m pygbag --title "Totally Accurate Spaceflight Simulator" Llama_Space_Programme
pause
