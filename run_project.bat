@echo off
echo ===================================================
echo   ReVive - Refurbished Marketplace Startup
echo ===================================================
echo.
echo [1/2] Starting Flask Backend API on http://127.0.0.1:5000...
start "ReVive Backend" cmd /k "cd /d %~dp0backend && python app.py"

echo [2/2] Starting React + Vite Frontend on http://localhost:5173...
start "ReVive Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"

echo.
echo Both servers are launching!
echo Frontend will be accessible at: http://localhost:5173
echo Backend API will be accessible at: http://127.0.0.1:5000
echo.

