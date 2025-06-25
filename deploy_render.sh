#!/bin/bash
# Script to prepare and deploy to Render

echo "📦 Preparing your NEPSE Data API for Render deployment..."

# Check if git is installed
if ! command -v git &> /dev/null
then
    echo "❌ Git is required but not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit for Render deployment"
fi

# Make sure all changes are committed
if [ -n "$(git status --porcelain)" ]; then
    echo "📝 Committing changes before deployment..."
    git add .
    git commit -m "Prepare for Render deployment"
fi

echo "✅ All changes committed to git"

# Check for render.yaml
if [ ! -f render.yaml ]; then
    echo "❌ render.yaml not found. Please create this file first."
    echo "📝 See RENDER_DEPLOYMENT.md for details."
    exit 1
fi

echo "🚀 Your project is ready for Render deployment!"
echo ""
echo "Next steps:"
echo "1. Create a Render account if you don't have one: https://render.com"
echo "2. Push your repository to GitHub"
echo "3. Connect your GitHub repository to Render"
echo "4. Deploy your web service following the instructions in RENDER_DEPLOYMENT.md"
echo ""
echo "For more details, refer to RENDER_DEPLOYMENT.md"
