#!/usr/bin/env python3
"""
Test script to verify Chrome setup for GitHub Actions
"""

import os
import sys
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_chrome_setup():
    """Test Chrome setup similar to GitHub Actions environment"""
    print("Testing Chrome setup...")
    
    # Simulate GitHub Actions environment
    os.environ['GITHUB_ACTIONS'] = 'true'
    os.environ['CI'] = 'true'
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--single-process')
    options.add_argument('--disable-blink-features=AutomationControlled')
    
    # Set a unique user data directory
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        
        # Test basic functionality
        driver.get("data:text/html,<html><body><h1>Test Page</h1></body></html>")
        title = driver.title
        print(f"Test page loaded successfully. Title: {title}")
        
        # Test loading a real webpage
        driver.get("https://httpbin.org/get")
        print("Real webpage loaded successfully")
        
        driver.quit()
        print("✅ Chrome setup test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Chrome setup test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chrome_setup()
    sys.exit(0 if success else 1)
