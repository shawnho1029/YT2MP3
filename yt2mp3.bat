@echo off
setlocal
cd /d "%~dp0"

if "%~1"=="" (
    echo Starting interactive mode...
    .\venv\Scripts\python.exe yt2mp3.py -i
    echo.
    echo Press any key to exit...
    pause >nul
) else (
    .\venv\Scripts\python.exe yt2mp3.py %*
    if %errorlevel% neq 0 (
        echo.
        echo Program exited with error code %errorlevel%
        pause
    )
)
