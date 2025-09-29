#!/bin/bash

echo "🤖 Virtual Therapist Frontend Startup"
echo "======================================"

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed or not in PATH"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js is installed"

# Navigate to frontend directory
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install dependencies"
        exit 1
    fi
fi

echo "✅ Dependencies are ready"

# Start the React development server
echo "🚀 Starting Virtual Therapist Frontend..."
echo "📍 Frontend will be available at: http://localhost:3000"
echo "📍 Make sure the backend is running on port 5000"
echo "🛑 Press Ctrl+C to stop the server"
echo "----------------------------------------"

npm start
