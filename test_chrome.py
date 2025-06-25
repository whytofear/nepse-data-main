#!/usr/bin/env python3
"""
Test script to verify Chrome setup for GitHub Actions
"""
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

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
