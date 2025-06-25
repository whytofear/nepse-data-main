#!/usr/bin/env python3
"""
Quick fix for NEPSE scraper - handles SSL and connection issues
"""

import os
import sys
import time
import subprocess

def main():
    print("🔧 NEPSE Scraper Quick Fix")
    print("=" * 50)
    
    # Check if we're in GitHub Actions
    if os.environ.get('GITHUB_ACTIONS'):
        print("Running in GitHub Actions - applying CI fixes...")
        
        # Update system certificates
        try:
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ca-certificates'], check=True)
            print("✅ Updated system certificates")
        except Exception as e:
            print(f"⚠️ Could not update certificates: {e}")
    
    # Test the scraper
    print("\n📊 Testing scraper...")
    try:
        import scrape_floorsheet
        print("✅ Scraper module imported successfully")
        
        # Try to run the main function
        scrape_floorsheet.main()
        print("✅ Scraper completed successfully")
        
        # Check if data was created
        data_files = []
        if os.path.exists('data'):
            data_files = [f for f in os.listdir('data') if f.endswith('.csv')]
        
        if data_files:
            print(f"✅ Found {len(data_files)} CSV files in data directory")
            for file in data_files[-3:]:  # Show last 3 files
                filepath = os.path.join('data', file)
                size = os.path.getsize(filepath)
                print(f"   - {file} ({size} bytes)")
        else:
            print("❌ No CSV files found in data directory")
            
    except Exception as e:
        print(f"❌ Scraper failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
