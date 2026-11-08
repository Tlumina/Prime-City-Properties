@echo off
title Prime City Properties Launcher
echo ========================================================
echo          PRIME CITY PROPERTIES REAL ESTATE
echo            "Stop Searching. Start Living."
echo ========================================================
echo.

cd /d "%~dp0"

IF NOT EXIST "venv\Scripts\python.exe" (
    echo [1/4] Creating Python virtual environment...
    python -m venv venv
) ELSE (
    echo [1/4] Virtual environment verified.
)

echo [2/4] Installing / Updating dependencies...
call .\venv\Scripts\python.exe -m pip install --quiet -r requirements.txt

echo [3/4] Running database migrations & seeding initial data...
call .\venv\Scripts\python.exe manage.py migrate --noinput
call .\venv\Scripts\python.exe manage.py seed_properties

echo.
echo [4/4] Starting Prime City Properties Server...
echo Site will be available at: http://127.0.0.1:8000/
echo Admin Dashboard available at: http://127.0.0.1:8000/admin/
echo [SECURITY NOTICE] Change default credentials on your dashboard or via CLI:
echo ^> python manage.py changepassword admin@primecityproperties.ng
echo.
echo Press Ctrl+C in this window to stop the server.
echo ========================================================

start http://127.0.0.1:8000/
call .\venv\Scripts\python.exe manage.py runserver 0.0.0.0:8000

pause
