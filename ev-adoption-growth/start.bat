@echo off
echo ========================================
echo EV Adoption Growth Dashboard
echo ========================================
echo.
echo Starting Flask Backend...
start cmd /k "python app.py"
timeout /t 3
echo.
echo Starting React Frontend...
cd frontend
start cmd /k "npm start"
cd ..
echo.
echo ========================================
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo ========================================
