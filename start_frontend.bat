@echo off
echo 🤖 Virtual Therapist Frontend Startup
echo ======================================

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js is installed

REM Navigate to frontend directory
cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo 📦 Installing dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Dependencies are ready

REM Start the React development server
echo 🚀 Starting Virtual Therapist Frontend...
echo 📍 Frontend will be available at: http://localhost:3000
echo 📍 Make sure the backend is running on port 5000
echo 🛑 Press Ctrl+C to stop the server
echo ----------------------------------------

npm start

pause
