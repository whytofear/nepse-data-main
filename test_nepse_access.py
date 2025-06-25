#!/usr/bin/env python3
"""
Simple test to check NEPSE website accessibility and basic scraping functionality
"""

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

def test_website_accessibility():
    """Test if NEPSE website is accessible"""
    try:
        print("Testing NEPSE website accessibility...")
        response = requests.get("https://www.nepalstock.com/floor-sheet", timeout=10)
        print(f"HTTP Status Code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            print("✅ NEPSE website is accessible")
            return True
        else:
            print(f"❌ NEPSE website returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing NEPSE website: {str(e)}")
        return False

def setup_test_driver():
    """Setup Chrome driver for testing"""
    options = Options()
    
    # Add all the options we use in the main scraper
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--window-size=1920,1080')
    
    # Add user agent
    options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    # GitHub Actions specific settings
    if os.environ.get('GITHUB_ACTIONS'):
        print("Configuring for GitHub Actions environment...")
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-default-apps')
        options.add_argument('--disable-sync')
        
        # Set Chrome binary path if available
        chrome_bin = os.environ.get('CHROME_BIN')
        if chrome_bin:
            options.binary_location = chrome_bin
            print(f"Using Chrome binary: {chrome_bin}")
    
    try:
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome driver initialized successfully")
        return driver
    except Exception as e:
        print(f"❌ Error initializing Chrome driver: {str(e)}")
        return None

def test_page_loading():
    """Test if we can load the NEPSE floor sheet page"""
    driver = setup_test_driver()
    if not driver:
        return False
    
    try:
        print("Loading NEPSE floor sheet page...")
        driver.get("https://www.nepalstock.com/floor-sheet")
        
        # Wait for page to load
        print("Waiting for page to load...")
        time.sleep(5)
        
        # Check page title
        title = driver.title
        print(f"Page title: {title}")
        
        # Check if we can find the floor sheet table
        print("Looking for floor sheet table...")
        
        # Try to find the table element
        try:
            table = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "table"))
            )
            print("✅ Floor sheet table found")
            
            # Try to find table rows
            rows = table.find_elements(By.TAG_NAME, "tr")
            print(f"Found {len(rows)} table rows")
            
            if len(rows) > 1:  # Header + at least one data row
                print("✅ Table has data rows")
                
                # Print first few rows for debugging
                print("First 3 rows:")
                for i, row in enumerate(rows[:3]):
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if not cells:  # Try th for header
                        cells = row.find_elements(By.TAG_NAME, "th")
                    row_text = [cell.text.strip() for cell in cells]
                    print(f"Row {i}: {row_text}")
                
                return True
            else:
                print("❌ Table found but no data rows")
                return False
                
        except Exception as e:
            print(f"❌ Could not find floor sheet table: {str(e)}")
            
            # Try to get page source for debugging
            page_source = driver.page_source
            print("Page source preview (first 500 chars):")
            print(page_source[:500])
            
            return False
            
    except Exception as e:
        print(f"❌ Error loading page: {str(e)}")
        return False
    finally:
        if driver:
            driver.quit()
            print("Browser closed")

def main():
    """Run all tests"""
    print("🧪 Starting NEPSE scraper diagnostic tests...")
    print("=" * 50)
    
    # Test 1: Website accessibility
    print("\n1. Testing website accessibility...")
    accessible = test_website_accessibility()
    
    # Test 2: Page loading and table detection
    print("\n2. Testing page loading and table detection...")
    page_loaded = test_page_loading()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print(f"Website accessible: {'✅' if accessible else '❌'}")
    print(f"Page loads with data: {'✅' if page_loaded else '❌'}")
    
    if accessible and page_loaded:
        print("\n🎉 All tests passed! The scraper should work.")
    else:
        print("\n⚠️ Some tests failed. Check the output above for details.")
        
        if not accessible:
            print("- The NEPSE website might be down or blocking requests")
        if not page_loaded:
            print("- The page structure might have changed or data is not loading")

if __name__ == "__main__":
    main()
