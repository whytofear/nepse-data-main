#!/usr/bin/env python3
"""
Simple test script to verify Chrome and ChromeDriver work in GitHub Actions
"""

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def test_chrome_setup():
    """Test Chrome setup for GitHub Actions"""
    print("Testing Chrome setup...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-web-security')
    
    # Set unique user data directory
    import tempfile
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Check environment
    print(f"GITHUB_ACTIONS: {os.environ.get('GITHUB_ACTIONS', 'Not set')}")
    print(f"CI: {os.environ.get('CI', 'Not set')}")
    print(f"DISPLAY: {os.environ.get('DISPLAY', 'Not set')}")
    print(f"CHROME_BIN: {os.environ.get('CHROME_BIN', 'Not set')}")
    
    # Set Chrome binary if in CI
    if os.environ.get('GITHUB_ACTIONS') or os.environ.get('CI'):
        chrome_bin = os.environ.get('CHROME_BIN', '/usr/bin/google-chrome')
        if os.path.exists(chrome_bin):
            options.binary_location = chrome_bin
            print(f"Using Chrome binary: {chrome_bin}")
    
    try:
        # Test Chrome driver
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(30)
        
        # Test basic functionality
        driver.get("data:text/html,<html><body><h1>Chrome Test Success</h1></body></html>")
        title = driver.title
        print(f"Test page title: {title}")
        
        # Test actual website (simple GET request)
        print("Testing Nepal Stock website...")
        driver.get("https://www.nepalstock.com")
        print(f"Nepal Stock website title: {driver.title}")
        
        driver.quit()
        print("✅ Chrome setup test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ Chrome setup test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_chrome_setup()
    sys.exit(0 if success else 1)

def test_chrome_setup():
    """Test if Chrome can be initialized with CI-friendly options"""
    print("Testing Chrome setup for GitHub Actions...")
    
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    options.add_argument('--window-size=1280,720')
    
    # Set environment to simulate CI
    os.environ['GITHUB_ACTIONS'] = 'true'
    
    try:
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
        print("✅ Chrome driver initialized successfully")
        
        # Test basic navigation
        driver.get("https://www.google.com")
        title = driver.title
        print(f"✅ Successfully navigated to Google. Title: {title}")
        
        driver.quit()
        print("✅ Chrome driver closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_chrome_setup()
    sys.exit(0 if success else 1)
