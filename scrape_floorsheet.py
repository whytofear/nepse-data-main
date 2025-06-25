from selenium import webdriver
from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import sys
import time


def setup_driver():
    """Initialize the Chrome driver with appropriate options"""
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=VizDisplayCompositor')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--headless=new')  # Use new headless mode for Chrome 112+
    options.add_argument('--remote-debugging-port=9222')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-plugins')
    options.add_argument('--disable-images')
    options.add_argument('--single-process')
    options.add_argument('--disable-background-timer-throttling')
    options.add_argument('--disable-backgrounding-occluded-windows')
    options.add_argument('--disable-renderer-backgrounding')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-default-apps')
    options.add_argument('--disable-sync')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    
    # Set a unique user data directory to avoid conflicts
    import os
    import tempfile
    user_data_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    
    # Check if running in GitHub Actions or similar CI environment
    if os.environ.get('GITHUB_ACTIONS') or os.environ.get('CI'):
        print("Running in CI environment, configuring for headless Chrome...")
        
        # Set Chrome binary path for GitHub Actions
        chrome_bin = os.environ.get('CHROME_BIN', '/usr/bin/google-chrome-stable')
        if os.path.exists(chrome_bin):
            options.binary_location = chrome_bin
            print(f"Using Chrome binary at: {chrome_bin}")
            
            # Verify DISPLAY is set
            display = os.environ.get('DISPLAY')
            print(f"DISPLAY environment variable: {display}")
        else:
            print(f"Chrome binary not found at: {chrome_bin}")
            # Try alternative paths
            alternative_paths = ['/usr/bin/google-chrome', '/usr/bin/chromium-browser']
            for path in alternative_paths:
                if os.path.exists(path):
                    options.binary_location = path
                    print(f"Using alternative Chrome binary at: {path}")
                    break
    
    try:
        # Initialize Chrome service
        from selenium.webdriver.chrome.service import Service
        service = Service()
        
        print("Attempting to start Chrome driver...")
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(240)
        print("Chrome driver initialized successfully")
        
        # Test basic functionality
        driver.get("data:text/html,<html><body><h1>Test</h1></body></html>")
        print("Chrome driver test page loaded successfully")
        
        return driver
    except Exception as e:
        print(f"Error initializing Chrome driver: {str(e)}")
        print("Trying to get more details about the error...")
        import traceback
        traceback.print_exc()
        raise


def load_page(driver):
    """Load the Nepal Stock floor sheet page"""
    try:
        driver.get("https://www.nepalstock.com/floor-sheet")
        # Wait for the page to load completely
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        print("Page loaded successfully")
        return True
    except TimeoutException:
        print("Page failed to load within timeout period")
        return False
    except Exception as e:
        print(f"Error loading page: {str(e)}")
        return False


def set_items_per_page(driver, items_count=10):
    """Set the number of items per page in the dropdown"""
    try:
        # Look for the items per page dropdown
        items_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "items_per_page"))
        )
        select = Select(items_dropdown)
        select.select_by_value(str(items_count))
        time.sleep(2)  # Wait for the page to reload
        print(f"Set items per page to {items_count}")
        return True
    except Exception as e:
        print(f"Could not set items per page: {str(e)}")
        return False


def get_table_data(driver):
    """Extract table data from the current page"""
    try:
        # Wait for table to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find the main data table
        table = soup.find("table")
        if not table:
            print("No table found on the page")
            return pd.DataFrame()
        
        rows = []
        for row in table.find_all("tr"):
            cells = row.find_all(["th", "td"])
            row_data = [cell.get_text(strip=True) for cell in cells]
            if row_data:  # Only add non-empty rows
                rows.append(row_data)
        
        if rows:
            df = pd.DataFrame(rows)
            print(f"Extracted {len(df)} rows from current page")
            return df
        else:
            print("No data rows found in table")
            return pd.DataFrame()
            
    except Exception as e:
        print(f"Error extracting table data: {str(e)}")
        return pd.DataFrame()


def has_next_page(driver):
    """Check if there's a next page available"""
    try:
        # Look for pagination controls - this might need adjustment based on actual HTML structure
        next_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), 'Next')] | //button[contains(text(), 'Next')] | //a[contains(@aria-label, 'Next')]")
        
        for btn in next_buttons:
            if btn.is_enabled() and btn.is_displayed():
                return True, btn
        return False, None
    except Exception as e:
        print(f"Error checking for next page: {str(e)}")
        return False, None


def go_to_next_page(driver):
    """Navigate to the next page"""
    try:
        has_next, next_btn = has_next_page(driver)
        if has_next and next_btn:
            driver.execute_script("arguments[0].click();", next_btn)
            time.sleep(3)  # Wait for page to load
            return True
        return False
    except Exception as e:
        print(f"Error navigating to next page: {str(e)}")
        return False


def scrape_all_data(driver):
    """Scrape data from all pages"""
    all_data = pd.DataFrame()
    page_count = 0
    
    while True:
        page_count += 1
        print(f"Scraping page {page_count}")
        
        # Get data from current page
        page_data = get_table_data(driver)
        
        if not page_data.empty:
            all_data = pd.concat([all_data, page_data], ignore_index=True)
        else:
            print("No data found on current page")
        
        # Try to go to next page
        if not go_to_next_page(driver):
            print("No more pages available or failed to navigate")
            break
    
    print(f"Total pages scraped: {page_count}")
    print(f"Total rows collected: {len(all_data)}")
    return all_data


def clean_data(df):
    """Clean and process the scraped data"""
    if df.empty:
        print("No data to clean")
        return df
    
    # Remove duplicate rows
    df = df.drop_duplicates(keep='first')
    
    # Set the first row as header if it contains column names
    if not df.empty:
        # Check if first row contains header-like data
        first_row = df.iloc[0].astype(str).str.lower()
        if any(header_word in ' '.join(first_row) for header_word in ['contract', 'stock', 'symbol', 'buyer', 'seller', 'quantity', 'rate', 'amount']):
            new_header = df.iloc[0]
            df = df[1:]  # Remove header row from data
            df.columns = new_header
        else:
            # Set default column names based on the screenshot structure
            expected_columns = ['SN', 'Contract No.', 'Stock Symbol', 'Buyer', 'Seller', 'Quantity', 'Rate (Rs)', 'Amount (Rs)']
            if len(df.columns) == len(expected_columns):
                df.columns = expected_columns
            else:
                print(f"Warning: Expected {len(expected_columns)} columns, but got {len(df.columns)}")
    
    # Clean numeric columns
    if 'Rate (Rs)' in df.columns:
        df['Rate (Rs)'] = df['Rate (Rs)'].astype(str).str.replace(',', '').str.replace('Rs', '').str.strip()
        df['Rate (Rs)'] = pd.to_numeric(df['Rate (Rs)'], errors='coerce')
    
    if 'Amount (Rs)' in df.columns:
        df['Amount (Rs)'] = df['Amount (Rs)'].astype(str).str.replace(',', '').str.replace('Rs', '').str.strip()
        df['Amount (Rs)'] = pd.to_numeric(df['Amount (Rs)'], errors='coerce')
    
    if 'Quantity' in df.columns:
        df['Quantity'] = df['Quantity'].astype(str).str.replace(',', '').str.strip()
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
    
    # Remove rows with all NaN values
    df = df.dropna(how='all')
    
    # Reset index
    df = df.reset_index(drop=True)
    
    print(f"Data cleaned. Final shape: {df.shape}")
    return df


def main():
    """Main function to orchestrate the scraping process"""
    print("Starting Nepal Stock floor sheet scraper...")
    
    # Check environment
    import os
    if os.environ.get('GITHUB_ACTIONS'):
        print("Running in GitHub Actions environment")
    
    driver = None
    try:
        # Initialize driver
        print("Initializing Chrome driver...")
        driver = setup_driver()
        print("Chrome driver initialized successfully")
        
        # Load the main page
        print("Loading Nepal Stock floor sheet page...")
        if not load_page(driver):
            print("Failed to load the main page. Exiting.")
            return
        
        print("Page loaded successfully")
        
        # Set items per page to maximum for efficiency
        print("Setting items per page...")
        set_items_per_page(driver, 10)  # You can change this to 25, 50, 100 if available
        
        # Scrape all data
        print("Starting data extraction...")
        raw_data = scrape_all_data(driver)
        
        if raw_data.empty:
            print("No data was scraped. Please check the website structure.")
            return
        
        print(f"Raw data extracted. Shape: {raw_data.shape}")
        
        # Clean the data
        print("Cleaning data...")
        cleaned_data = clean_data(raw_data)
        
        if cleaned_data.empty:
            print("No data remaining after cleaning.")
            return
        
        print(f"Data cleaned successfully. Shape: {cleaned_data.shape}")
        
        # Save to CSV
        today = datetime.today().strftime('%Y-%m-%d')
        filename = f"data/nepal_stock_floorsheet_{today}.csv"
        
        # Create data directory if it doesn't exist
        import os
        os.makedirs("data", exist_ok=True)
        
        cleaned_data.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
        print(f"Total records saved: {len(cleaned_data)}")
        
        # Display sample of the data
        print("\nFirst 5 rows of scraped data:")
        print(cleaned_data.head())
        
    except Exception as e:
        print(f"An error occurred during scraping: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Always close the driver
        if driver:
            try:
                driver.quit()
                print("Browser closed successfully.")
            except Exception as e:
                print(f"Error closing browser: {str(e)}")
        else:
            print("No browser to close.")


if __name__ == "__main__":
    main()
