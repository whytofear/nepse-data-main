# 🚀 Complete Beginner's Guide to NEPSE Analysis

## 📋 Table of Contents

1. [What is this project?](#what-is-this-project)
2. [How to see the data analysis](#how-to-s### API Endpoints (for developers)

```bash
# List all available files
curl https://nepse-data-api.onrender.com/api/files

# Get latest data
curl https://nepse-data-api.onrender.com/api/latest

# Get specific file data
curl https://nepse-data-api.onrender.com/api/data/nepal_stock_floorsheet_2025-06-25.csv

# Get data for specific stock
curl https://nepse-data-api.onrender.com/api/stock/ALBSL

# Get statistics
curl https://nepse-data-api.onrender.com/api/stats
```

Replace "nepse-data-api" with whatever name you chose for your service.ow to deploy API to Render (Free)](#deploy-to-render)
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

## 🚀 Deploy to Render (Step-by-step for beginners)

### Step 1: Prepare your GitHub repository

1. **Create GitHub account** if you don't have one: https://github.com
2. **Upload your code** to GitHub:

   - Create new repository named `nepse-data-main`
   - Upload all files from your project folder
   - Make sure the repository is public

3. **Update the API configuration**:
   - Open `api_server.py`
   - The code now automatically reads from environment variables
   - You'll configure these in Render later

### Step 2: Deploy to Render (Free) - Super Easy Instructions

1. **Create Render account**:
   - Go to: https://dashboard.render.com/register
   - Click "Sign Up"
   - Choose "Continue with GitHub" (easiest option)
   - Authorize Render to access your GitHub account

2. **Connect your GitHub repository**:
   - After signing in, you'll see the Render dashboard
   - Click the big purple "New +" button in the top right
   - Select "Web Service" from the dropdown

3. **Find your repository**:
   - You'll see a list of your GitHub repositories
   - Find and click on "nepse-data-main"

4. **Set up your service** (just copy these exact settings):
   - **Name**: `nepse-data-api` (or choose any name)
   - **Environment**: Select "Python"
   - **Region**: Choose any (closest to you is best)
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn api_server:app`
   - Leave all other settings as default

5. **Create your web service**:
   - Scroll down and click the purple "Create Web Service" button
   - Render will start building your application (this takes 5-10 minutes)
   - You'll see logs showing the progress

6. **Your API is ready!**
   - When you see "Your service is live 🎉", it's ready
   - Click the link at the top (ends with `.onrender.com`) to see your API

7. **(Optional) Add GitHub token for better performance**:
   - On your web service page, click "Environment" in the left menu
   - Click "Add Environment Variable"
   - Add these one by one:
     - Key: `GITHUB_TOKEN`, Value: (your GitHub token)
     - Key: `GITHUB_REPO_OWNER`, Value: (your GitHub username)
     - Key: `GITHUB_REPO_NAME`, Value: `nepse-data-main`
   - Click "Save Changes"
   - Render will automatically redeploy your application

### How to get a GitHub token (if you want better performance):

1. Go to GitHub.com and log in
2. Click your profile picture in the top right
3. Choose "Settings"
4. Scroll down and click "Developer settings" (bottom left)
5. Click "Personal access tokens" → "Tokens (classic)"
6. Click "Generate new token" → "Generate new token (classic)"
7. Name it "NEPSE API Token"
8. Check the box next to "repo"
9. Scroll down and click "Generate token"
10. Copy the token (it looks like a long random string)
11. Paste it as the value for GITHUB_TOKEN in step 7 above

### Step 3: Test your API

Your API will be available at: `https://nepse-data-api.onrender.com`
(Replace "nepse-data-api" with whatever name you chose)

### 📸 Visual Step-by-Step Guide

For a complete visual guide with screenshots for each step, see:
[RENDER_VISUAL_GUIDE.md](RENDER_VISUAL_GUIDE.md)

This includes pictures of exactly what to click and where to find everything!

---

## 🌐 How to use the API

### Web Interface (Easiest)

1. **Open your API URL** in browser: `https://your-nepse-api.onrender.com`
2. **Click the buttons** to try different features:
   - "List All Files" - See available data files
   - "Get Latest Data" - See most recent trading data
   - "Get Statistics" - See summary statistics

### API Endpoints (for developers)

```bash
# List all available files
curl https://your-nepse-api.onrender.com/api/files

# Get latest data
curl https://your-nepse-api.onrender.com/api/latest

# Get specific file data
curl https://your-nepse-api.onrender.com/api/data/nepal_stock_floorsheet_2025-06-25.csv

# Get data for specific stock
curl https://your-nepse-api.onrender.com/api/stock/ALBSL

# Get statistics
curl https://nepse-data-api.onrender.com/api/stats
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

**4. Render deployment failed**

- Check your GitHub repository is accessible (should be public)
- Make sure all files are committed to git
- Check Render logs in the dashboard
- Try setting GITHUB_TOKEN environment variable in Render dashboard

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

   For Render deployment:
   - Go to your Render dashboard
   - Click on your service ("nepse-data-api")
   - Click "Logs" in the left menu
   - Select "Live" to see real-time logs

   For local testing:
   ```bash
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
- ✅ REST API deployed on Render (free)
- ✅ Web interface for easy access
- ✅ Understanding of market analysis

**Next Steps:**

1. Set up GitHub Actions for daily automation
2. Share your API URL with others
3. Customize analysis parameters
4. Add more stocks to monitor

**Need more help?** Check the main README.md file for additional details!
