# 🖼️ Visual Guide to Deploy on Render (Free)

Follow these simple steps with screenshots to deploy your NEPSE Data API on Render for free.

## Step 1: Sign up for Render

![Sign up for Render](https://i.imgur.com/XjJKqww.png)
Go to https://render.com and click "Sign Up"

## Step 2: Connect with GitHub

![Connect with GitHub](https://i.imgur.com/QKHwR3Z.png)
Choose "Continue with GitHub" for the easiest experience

## Step 3: Create a New Web Service

![Create New Web Service](https://i.imgur.com/8FzUzVP.png)
Click the "New +" button and select "Web Service"

## Step 4: Find Your Repository

![Find Repository](https://i.imgur.com/4rJb5oA.png)
Find and click on your "nepse-data-main" repository

## Step 5: Configure Your Service

![Configure Service](https://i.imgur.com/YZpXdCH.png)
Fill in these exact settings:

- Name: nepse-data-api (or any name)
- Environment: Python
- Region: Choose any
- Branch: main
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn api_server:app`

## Step 6: Create Web Service

![Create Service](https://i.imgur.com/Y7dQ8jx.png)
Scroll down and click "Create Web Service"

## Step 7: Wait for Deployment

![Wait for Deployment](https://i.imgur.com/PRbJvRW.png)
Render will build and deploy your API (5-10 minutes)

## Step 8: Your API is Live!

![API Live](https://i.imgur.com/zHG7E8n.png)
Click on the link (ends with .onrender.com) to access your API

## Step 9: (Optional) Add GitHub Token for Better Performance

![Add Environment Variables](https://i.imgur.com/JLukBfV.png)

1. Click "Environment" in the left menu
2. Click "Add Environment Variable"
3. Add GITHUB_TOKEN, your GitHub username, and repo name
4. Click "Save Changes"

## Step 10: Enjoy Your API!

Now anyone can access your API at your custom Render URL.

---

**Note**: The screenshots are representative and may look slightly different as Render updates their interface.
