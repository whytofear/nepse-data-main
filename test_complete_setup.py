#!/usr/bin/env python3
"""
Quick Test Script for NEPSE API
Run this to test everything locally before deploying
"""

import subprocess
import sys
import time
import requests
import os

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success")
            return True
        else:
            print(f"❌ {description} - Failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Error: {str(e)}")
        return False

def test_api():
    """Test the API endpoints"""
    print("\n🌐 Testing API endpoints...")
    base_url = "http://localhost:5000"
    
    endpoints = [
        ("/", "Main page"),
        ("/api/files", "List files"),
        ("/api/stats", "Statistics"),
        ("/health", "Health check")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", timeout=10)
            if response.status_code == 200:
                print(f"✅ {description} - Working")
            else:
                print(f"⚠️  {description} - Status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"❌ {description} - Server not running")
        except Exception as e:
            print(f"❌ {description} - Error: {str(e)}")

def main():
    print("🚀 NEPSE Project Quick Test")
    print("=" * 40)
    
    # Check Python
    print(f"🐍 Python version: {sys.version}")
    
    # Check if data directory exists
    if os.path.exists("data"):
        csv_files = [f for f in os.listdir("data") if f.endswith('.csv')]
        print(f"📁 Data files found: {len(csv_files)}")
        if csv_files:
            print(f"📊 Latest file: {sorted(csv_files)[-1]}")
    else:
        print("📁 No data directory found")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing requirements"):
        print("⚠️  Some packages may not be installed properly")
    
    # Test scraper (quick test)
    print("\n🔄 Testing scraper (this may take a moment)...")
    scraper_result = run_command("timeout 30 python scrape_floorsheet.py || true", "Running scraper test")
    
    # Start API server in background for testing
    print("\n🌐 Starting API server for testing...")
    print("📍 Server will be available at: http://localhost:5000")
    print("💡 Press Ctrl+C to stop when done testing")
    
    try:
        # Import and run the API server
        import api_server
        api_server.app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Test complete!")
    except Exception as e:
        print(f"\n❌ Server error: {str(e)}")
        print("💡 Try running: python api_server.py")

if __name__ == "__main__":
    main()
