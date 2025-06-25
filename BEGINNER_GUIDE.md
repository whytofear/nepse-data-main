# 🚀 Complete Beginner's Guide to NEPSE Analysis

## 📋 Table of Contents

1. [What is this project?](#what-is-this-project)
2. [How to see the data analysis](#how-to-see-analysis)
3. [How to deploy API to Heroku](#deploy-to-heroku)
4. [How to use the API](#how-to-use-api)
5. [Understanding the analysis](#understanding-analysis)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 What is this project?

This project automatically collects daily trading data from Nepal Stock Exchange and provides:

- **📊 Data Collection**: Automatically scrapes daily floor sheet data
- **🔍 Market Analysis**: Detects suspicious trading patterns and manipulation
- **🌐 REST API**: Provides easy access to data via web interface
- **📈 Visual Reports**: Easy-to-understand charts and graphs

---

## 📊 How to see the analysis

### Method 1: Jupyter Notebook (Recommended for beginners)

1. **Install Python** (if not already installed):

   - Download from: https://www.python.org/downloads/
   - Install and make sure to check "Add Python to PATH"

2. **Open Terminal/Command Prompt** and navigate to your project folder:

   ```bash
   cd /Users/user/Desktop/nepse-data-main
   ```

3. **Install required packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Collect some data first** (run the scraper):

   ```bash
   python scrape_floorsheet.py
   ```

   This will create CSV files in the `data/` folder.

5. **Open the analysis notebook**:

   ```bash
   jupyter notebook floorsheet_analysis.ipynb
   ```

   This will open in your web browser.

6. **Use the Interactive Dashboard**:
   - Run all cells in the notebook (Cell → Run All)
   - Scroll to the bottom for the interactive dashboard
   - Select stock and timeframe from dropdowns
   - Click "Run Analysis" to see results

### Method 2: Quick Test (5 minutes)

1. **Run the test scraper** to see how it works:
   ```bash
   python test_scraper.py
   ```
   This opens a browser window so you can see what's happening.

---

## 🚀 Deploy to Heroku (Step-by-step for beginners)

### Step 1: Prepare your GitHub repository

1. **Create GitHub account** if you don't have one: https://github.com
2. **Upload your code** to GitHub:

   - Create new repository named `nepse-data-main`
   - Upload all files from your project folder
   - Make sure the repository is public

3. **Update the API configuration**:
   - Open `api_server.py`
   - Change line 12: `GITHUB_REPO_OWNER = "YOUR_GITHUB_USERNAME"`
   - Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username

### Step 2: Deploy to Heroku

1. **Create Heroku account**: https://signup.heroku.com/

2. **Install Heroku CLI**:

   - Download from: https://devcenter.heroku.com/articles/heroku-cli
   - Install and restart your terminal

3. **Login to Heroku**:

   ```bash
   heroku login
   ```

4. **Create Heroku app**:

   ```bash
   heroku create your-nepse-api
   ```

   Replace `your-nepse-api` with any unique name you want.

5. **Deploy your code**:

   ```bash
   # In your project directory
   git init
   git add .
   git commit -m "Initial commit"
   heroku git:remote -a your-nepse-api
   git push heroku main
   ```

6. **Set environment variables**:

   ```bash
   heroku config:set GITHUB_TOKEN=your_github_token
   ```

   To get GitHub token:

   - Go to GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with "repo" permissions
   - Copy the token and use it above

7. **Open your API**:
   ```bash
   heroku open
   ```

### Step 3: Test your API

Your API will be available at: `https://your-nepse-api.herokuapp.com`

---

## 🌐 How to use the API

### Web Interface (Easiest)

1. **Open your API URL** in browser: `https://your-nepse-api.herokuapp.com`
2. **Click the buttons** to try different features:
   - "List All Files" - See available data files
   - "Get Latest Data" - See most recent trading data
   - "Get Statistics" - See summary statistics

### API Endpoints (for developers)

```bash
# List all available files
curl https://your-nepse-api.herokuapp.com/api/files

# Get latest data
curl https://your-nepse-api.herokuapp.com/api/latest

# Get specific file data
curl https://your-nepse-api.herokuapp.com/api/data/nepal_stock_floorsheet_2025-06-25.csv

# Get data for specific stock
curl https://your-nepse-api.herokuapp.com/api/stock/ALBSL

# Get statistics
curl https://your-nepse-api.herokuapp.com/api/stats
```

---

## 📈 Understanding the Analysis

### 🚨 What the Red Flags Mean:

1. **Broker Dominance (>60%)**:

   - **What it is**: One broker controls most of the trading
   - **Why it's suspicious**: May indicate artificial price manipulation
   - **Example**: Broker #44 bought 80% of ALBSL stock today

2. **Wash Trading**:

   - **What it is**: Same broker appears as both buyer and seller
   - **Why it's suspicious**: Illegal practice to create fake volume
   - **Example**: Broker #22 sold to Broker #22 (same broker)

3. **Volume Surge**:

   - **What it is**: Trading volume suddenly jumps 3x normal
   - **Why it's suspicious**: Often precedes price manipulation
   - **Example**: OMPL normally trades 1000 shares, today it's 5000

4. **Aggressive Buying**:
   - **What it is**: Buying consistently at higher prices
   - **Why it's suspicious**: May be trying to drive price up
   - **Example**: Market price Rs. 800, but someone keeps buying at Rs. 820

### 📊 How to Read the Charts:

- **Green = Normal/Good**
- **Red = Suspicious/Warning**
- **Yellow = Watch closely**

### 📋 Net Holdings:

- **Net Buyer**: Bought more than sold (bullish)
- **Net Seller**: Sold more than bought (bearish)
- **Balanced**: Equal buying and selling

---

## 🔧 Troubleshooting

### Common Issues:

**1. "No module named 'pandas'"**

```bash
pip install pandas
```

**2. ChromeDriver not found**

- Download ChromeDriver: https://chromedriver.chromium.org/
- Put it in your system PATH

**3. Jupyter notebook won't open**

```bash
pip install jupyter
jupyter notebook
```

**4. Heroku deployment failed**

- Check your GitHub username in `api_server.py`
- Make sure all files are committed to git
- Check Heroku logs: `heroku logs --tail`

**5. API returns "No files found"**

- Run the scraper first: `python scrape_floorsheet.py`
- Make sure data files are in GitHub repository
- Check GitHub token permissions

**6. Analysis shows no data**

- Ensure CSV files exist in `data/` folder
- Check file format matches expected columns
- Run test scraper to verify data collection

### Getting Help:

1. **Check the logs**:

   ```bash
   # For Heroku
   heroku logs --tail

   # For local testing
   python api_server.py
   ```

2. **Test locally first**:

   ```bash
   python test_scraper.py
   python api_server.py
   ```

   Then open: http://localhost:5000

3. **Verify data files**:
   ```bash
   ls data/
   ```
   Should show `.csv` files with dates

---

## 🎉 You're Ready!

After following this guide, you'll have:

- ✅ Working data scraper
- ✅ Interactive analysis notebook
- ✅ REST API deployed on Heroku
- ✅ Web interface for easy access
- ✅ Understanding of market analysis

**Next Steps:**

1. Set up GitHub Actions for daily automation
2. Share your API URL with others
3. Customize analysis parameters
4. Add more stocks to monitor

**Need more help?** Check the main README.md file for additional details!
