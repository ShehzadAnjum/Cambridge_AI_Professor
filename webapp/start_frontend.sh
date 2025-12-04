#!/bin/bash
# Script to start the Next.js frontend development server

cd "$(dirname "$0")/frontend"

echo "Starting Next.js frontend server..."
echo "Frontend will be available at: http://localhost:3000"
echo ""

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

npm run dev


