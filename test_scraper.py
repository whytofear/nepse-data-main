#!/usr/bin/env python3
"""
Test script for Nepal Stock floor sheet scraper
This script runs the scraper with visible browser for debugging
"""

from scrape_floorsheet import setup_driver, load_page, get_table_data, clean_data
import sys

def test_scraper():
    """Test the scraper functionality step by step"""
    print("Testing Nepal Stock scraper...")
    
    # Initialize driver with visible browser (no headless mode)
    driver = setup_driver()
    
    try:
        print("\n1. Testing page loading...")
        if not load_page(driver):
            print("❌ Failed to load page")
            return False
        print("✅ Page loaded successfully")
        
        print("\n2. Testing data extraction...")
        data = get_table_data(driver)
        if data.empty:
            print("❌ No data extracted")
            return False
        print(f"✅ Extracted {len(data)} rows")
        print("Sample raw data:")
        print(data.head())
        
        print("\n3. Testing data cleaning...")
        cleaned = clean_data(data)
        if cleaned.empty:
            print("❌ No data after cleaning")
            return False
        print(f"✅ Cleaned data has {len(cleaned)} rows")
        print("Sample cleaned data:")
        print(cleaned.head())
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False
    
    finally:
        input("Press Enter to close browser...")
        driver.quit()

if __name__ == "__main__":
    success = test_scraper()
    sys.exit(0 if success else 1)
