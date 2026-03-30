#!/bin/bash
# Quick deployment script for Hugging Face Spaces

echo "=========================================="
echo "Medical OCR OpenEnv - Quick Deploy"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Medical OCR OpenEnv environment"
fi

# Get HF username and space name
echo "Enter your Hugging Face username:"
read HF_USERNAME

echo "Enter your Space name (e.g., medical-ocr-openenv):"
read SPACE_NAME

# Add remote
SPACE_URL="https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo ""
echo "Adding remote: $SPACE_URL"

if git remote | grep -q "space"; then
    echo "Remote 'space' already exists, updating..."
    git remote set-url space $SPACE_URL
else
    git remote add space $SPACE_URL
fi

# Push to space
echo ""
echo "Pushing to Hugging Face Space..."
echo "You may need to login with: huggingface-cli login"
echo ""

git push space main

echo ""
echo "=========================================="
echo "Deployment initiated!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Go to: https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME"
echo "2. Wait for build to complete (5-10 minutes)"
echo "3. Set environment secrets in Settings:"
echo "   - OPENAI_API_KEY"
echo "   - MODEL_NAME (e.g., gpt-4)"
echo "   - API_BASE_URL (e.g., https://api.openai.com/v1)"
echo "4. Test the Space:"
echo "   curl https://$HF_USERNAME-$SPACE_NAME.hf.space/"
echo "5. Run validation:"
echo "   curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://$HF_USERNAME-$SPACE_NAME.hf.space"
echo ""
echo "Good luck! 🚀"
