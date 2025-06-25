# Deploying NEPSE Data API to Render

This guide will walk you through deploying the NEPSE Floor Sheet API on Render, a free alternative to Heroku.

## Prerequisites

1. A [Render account](https://render.com/) (free to sign up)
2. Your code pushed to a GitHub repository
3. GitHub token (optional, but recommended for higher rate limits)

## Step-by-Step Deployment Guide

### 1. Sign up for Render

Visit [render.com](https://render.com/) and sign up for a free account.

### 2. Connect Your GitHub Repository

1. After logging in to Render, click on the "New +" button in the dashboard
2. Select "Web Service"
3. Connect your GitHub account if prompted
4. Find and select your NEPSE data repository

### 3. Configure Your Web Service

Fill in the following details:

- **Name**: `nepse-data-api` (or any name you prefer)
- **Environment**: Python
- **Region**: Choose the closest region to your users
- **Branch**: `main` (or your default branch)
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn api_server:app`

Under the "Advanced" section:

1. Click on "Add Environment Variable"
2. Add the following (if using GitHub token):

   - Key: `GITHUB_TOKEN`
   - Value: Your GitHub personal access token

3. Configure additional environment variables (optional):

   - Key: `GITHUB_REPO_OWNER`
   - Value: Your GitHub username

   - Key: `GITHUB_REPO_NAME`
   - Value: Your repository name

### 4. Deploy Your Service

1. Click "Create Web Service"
2. Render will automatically start building and deploying your application
3. Wait for the deployment to complete (this may take a few minutes)

### 5. Access Your API

Once deployed, your API will be available at:

```
https://nepse-data-api.onrender.com
```

(Replace `nepse-data-api` with the name you chose)

## Verification

1. Visit the URL of your deployed application
2. You should see the web interface for the NEPSE Floor Sheet API
3. Test the `/api/files` endpoint to ensure it returns a list of CSV files
4. Test other endpoints as needed

## Render Free Tier Limitations

The free tier of Render has some limitations:

- Services spin down after 15 minutes of inactivity
- When a request comes in after inactivity, there's a brief startup delay
- 750 hours of service per month (enough for most small projects)
- 100 GB bandwidth per month

## Troubleshooting

### API Not Working

- Check the Render logs in your dashboard for error messages
- Verify your environment variables are set correctly
- Ensure your GitHub repository is accessible

### GitHub Rate Limiting

- If you see GitHub API rate limit errors, add your GitHub token as described above

### Service Spinning Down

- The free tier spins down after 15 minutes of inactivity
- The first request after inactivity may be slow
- For more consistent performance, upgrade to a paid plan

## Maintenance

- Monitor your service in the Render dashboard
- Check logs periodically for any issues
- Update your code on GitHub, and Render will automatically redeploy

## Additional Features

Render offers several additional features you might find useful:

- Custom domains (may require a paid plan)
- Automatic HTTPS certificates
- Continuous deployment from GitHub

You have now successfully deployed your NEPSE Data API to Render's free tier!
