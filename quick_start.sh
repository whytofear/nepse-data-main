#!/bin/bash

echo "🚀 NEPSE API Quick Setup Script"
echo "==============================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

echo "✅ Python 3 found"

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Create data directory if it doesn't exist
mkdir -p data

# Run test scraper to collect sample data
echo "🔄 Running test scraper to collect sample data..."
python3 test_scraper.py

# Check if data was collected
if [ "$(ls -A data)" ]; then
    echo "✅ Sample data collected successfully"
else
    echo "⚠️  No data collected. You may need to run the scraper manually."
fi

# Start the API server
echo "🌐 Starting API server..."
echo "📍 API will be available at: http://localhost:5000"
echo "💡 Press Ctrl+C to stop the server"
echo ""

python3 api_server.py
