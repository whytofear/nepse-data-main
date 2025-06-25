# NEPSE Floor Sheet Scraper

Extracting daily floor sheet data from [Nepal Stock Exchange Ltd (NEPSE)](https://www.nepalstock.com/floor-sheet).

## Recent Updates

**✅ Updated scraper source**: Changed from Mero Lagani to the official Nepal Stock Exchange website

- **New Source**: https://www.nepalstock.com/floor-sheet
- **Improved Data Quality**: Direct access to official NEPSE data
- **Enhanced Error Handling**: Better debugging and error management

## Features

- 📊 **Daily Floor Sheet Data**: Scrapes complete floor sheet data including:
  - Contract Numbers
  - Stock Symbols
  - Buyer/Seller information
  - Quantity, Rate, and Amount details
- 🔄 **Automatic Pagination**: Handles multiple pages of data
- 🧹 **Data Cleaning**: Automatically cleans and formats the scraped data
- 💾 **CSV Export**: Saves data in organized CSV format
- 🐛 **Debug Mode**: Test script included for troubleshooting

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Make sure you have Chrome browser installed and ChromeDriver in your PATH

## Usage

### Quick Start

```bash
python scrape_floorsheet.py
```

### Testing/Debugging

```bash
python test_scraper.py
```

The test script runs with a visible browser window so you can see what's happening.

## Output

Data is saved as: `data/nepal_stock_floorsheet_YYYY-MM-DD.csv`

### Sample Data Structure

```
SN,Contract No.,Stock Symbol,Buyer,Seller,Quantity,Rate (Rs),Amount (Rs)
1,2025062403007134,ALBSL,44,22,42,805.00,33810.00
2,2025062401017779,OMPL,42,94,10,1385.00,13850.00
...
```

## Configuration

You can modify the scraper behavior by editing these parameters in `scrape_floorsheet.py`:

- **Items per page**: Change the `items_count` parameter in `set_items_per_page()`
- **Timeout settings**: Adjust `WebDriverWait` timeout values
- **Browser options**: Modify Chrome options in `setup_driver()`

## Troubleshooting

1. **Page not loading**: Check your internet connection and verify the NEPSE website is accessible
2. **ChromeDriver issues**: Ensure ChromeDriver is installed and matches your Chrome version
3. **No data extracted**: Run the test script to see detailed error messages

## Project Status

### Completed

- [x] ~~Create a scraper for Mero Lagani~~ **Updated to official NEPSE source**
- [x] Updated scraper for Nepal Stock Exchange official website
- [x] Enhanced data cleaning and error handling
- [x] Added debug/test functionality

### To-DO

- [x] **Create GitHub Actions for automated daily scraping** ✅
- [x] **Create a REST API for reading CSV files** ✅
- [x] **Deploy the API to Heroku** ✅
- [x] **Create Floor Sheet Analysis Notebook** ✅
- [ ] Add support for date range filtering
- [ ] Implement data validation and quality checks

## 🚀 New Features Added

### 🌐 REST API (`api_server.py`)

- **Web Interface**: User-friendly dashboard at your API URL
- **Multiple Endpoints**: `/api/files`, `/api/latest`, `/api/stats`, `/api/stock/<symbol>`
- **GitHub Integration**: Reads CSV files directly from your GitHub repository
- **Real-time Data**: Always serves the latest scraped data

### 📖 Complete Beginner's Guide (`BEGINNER_GUIDE.md`)

- **Step-by-step instructions** for complete beginners
- **Heroku deployment guide** with screenshots and commands
- **API usage examples** with real endpoints
- **Troubleshooting section** for common issues

### 🎯 Quick Setup Options

#### Option 1: Complete Test (Recommended)

```bash
python test_complete_setup.py
```

#### Option 2: Quick Start Script

```bash
./quick_start.sh
```

#### Option 3: Manual Setup

```bash
pip install -r requirements.txt
python scrape_floorsheet.py  # Collect data
python api_server.py         # Start API server
```

## 📊 Floor Sheet Analysis Features

### 🔍 Market Manipulation Detection

- **🚨 Broker Dominance**: Flags brokers controlling >60-80% of volume
- **🔄 Wash Trading**: Detects same brokers on both buy/sell sides
- **📈 Volume Surge**: Identifies unusual volume spikes and responsible brokers
- **💰 Aggressive Buying**: Finds brokers consistently buying at premium prices

### 📋 Comprehensive Analysis

- **Multi-timeframe**: Daily, Weekly, Monthly, Quarterly, Yearly, 15-day periods
- **Net Holdings**: Track broker positions and share turnover
- **Interactive Dashboard**: User-friendly interface for non-technical users
- **Visual Reports**: Charts and graphs for easy understanding

### 🎛️ Easy to Use

```bash
# Run the analysis notebook
jupyter notebook floorsheet_analysis.ipynb
```

The notebook includes an interactive dashboard where you can:

- Select any stock symbol or analyze all stocks
- Choose different timeframes
- Run specific analyses or comprehensive reports
- Get visual charts and easy-to-understand summaries

## 🌐 API Usage Examples

### 🎯 For Complete Beginners

**Want to see your data right now?**

1. **Deploy to Heroku** (5 minutes):

   ```bash
   # Create Heroku app
   heroku create your-nepse-api

   # Deploy
   git add .
   git commit -m "Deploy API"
   git push heroku main

   # Set GitHub token
   heroku config:set GITHUB_TOKEN=your_github_token

   # Open your API
   heroku open
   ```

2. **Use the Web Interface**:
   - Open your Heroku app URL
   - Click "List All Files" to see your data
   - Click "Get Latest Data" to see recent trades
   - Click "Get Statistics" for market summary

### 📊 API Endpoints

```bash
# Your API will be at: https://your-app-name.herokuapp.com

# List available data files
GET /api/files

# Get latest trading data
GET /api/latest

# Get specific stock data
GET /api/stock/ALBSL

# Get market statistics
GET /api/stats

# Get data from specific date
GET /api/data/nepal_stock_floorsheet_2025-06-25.csv
```

### 💡 Real Examples

```bash
# See all available files
curl https://your-nepse-api.herokuapp.com/api/files

# Get latest 10 records
curl "https://your-nepse-api.herokuapp.com/api/latest?limit=10"

# Get all ALBSL trades
curl https://your-nepse-api.herokuapp.com/api/stock/ALBSL

# Get market summary
curl https://your-nepse-api.herokuapp.com/api/stats
```

## Free Deployment Options

You can deploy the NEPSE Floor Sheet API for free using Render:

### Render Deployment (Recommended)

Render offers a generous free tier and is easy to set up:

1. Follow the step-by-step guide in [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md)
2. Your API will be available at `https://your-app-name.onrender.com`
3. Free tier includes 750 hours of runtime per month and automatic HTTPS

#### Render Benefits:

- Easy GitHub integration with automatic deployments
- Free SSL certificates
- Custom domains (may require paid plan)
- Simple environment variable configuration

For complete deployment instructions, see [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md).
