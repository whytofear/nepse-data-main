# 🚀 3-Step Quick Start for Total Beginners

## Step 1: Upload to GitHub

1. Go to GitHub.com and create an account
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name it "nepse-data-main"
5. Make it "Public"
6. Click "Create repository"
7. Click "uploading an existing file"
8. Drag and drop all files from your nepse-data-main folder
9. Click "Commit changes"

## Step 2: Deploy on Render (Free)

1. Go to Render.com and sign up with your GitHub account
2. Click "New +" and select "Web Service"
3. Find and select your "nepse-data-main" repository
4. Fill in these settings exactly:
   - Name: nepse-data-api
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn api_server:app`
5. Click "Create Web Service"
6. Wait about 5-10 minutes for deployment to complete

## Step 3: Use Your API

1. When deployment is complete, click the link (ends with .onrender.com)
2. You'll see a beautiful web interface for your API
3. Click "List All Files" to see your data
4. Share your API link with others!

That's it! Your NEPSE Data API is now live for everyone to use, completely free!

For more detailed instructions with pictures, see:

- [RENDER_VISUAL_GUIDE.md](RENDER_VISUAL_GUIDE.md) (with screenshots)
- [BEGINNER_GUIDE.md](BEGINNER_GUIDE.md) (full details)
- [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) (technical details)
