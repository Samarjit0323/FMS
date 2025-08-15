#!/bin/bash

# Start AdminHub Frontend Server
# Default: http://10.115.124.225:3000

echo "🚀 Starting AdminHub Frontend Server..."
echo "📍 Server will be available at: http://10.115.124.225:3000"
echo ""

# Check if http-server is installed
if ! command -v npx &> /dev/null; then
    echo "❌ Error: npx is not installed. Please install Node.js first."
    exit 1
fi

# Start the server
echo "✅ Starting server..."
npx http-server Frontend -p 3000 -a 10.115.124.225 -o

echo ""
echo "🛑 Server stopped."
