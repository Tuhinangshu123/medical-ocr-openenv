# Deployment Guide - Hugging Face Spaces

## Step 1: Create Hugging Face Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Space name**: `medical-ocr-openenv` (or your choice)
   - **License**: MIT
   - **SDK**: Docker
   - **Hardware**: CPU basic (free tier is fine)
3. Add tag: `openenv`
4. Click "Create Space"

## Step 2: Prepare Repository

```bash
cd matrika/matrika/openenv-adapter

# Initialize git if not already
git init

# Add all files
git add .
git commit -m "Initial OpenEnv medical OCR environment"
```

## Step 3: Push to Hugging Face

```bash
# Add HF Space as remote (replace YOUR_USERNAME and SPACE_NAME)
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv

# Push to Space
git push space main
```

If you need to login:
```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login
```

## Step 4: Set Environment Secrets

1. Go to your Space settings: `https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv/settings`
2. Scroll to "Repository secrets"
3. Add these secrets:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `MODEL_NAME`: `gpt-4` (or `gpt-3.5-turbo` for cheaper testing)
   - `API_BASE_URL`: `https://api.openai.com/v1`

## Step 5: Wait for Build

The Space will automatically build the Docker image. This takes 5-10 minutes.

Watch the build logs in the "Logs" tab.

## Step 6: Test Deployment

Once built, test the endpoints:

```bash
# Replace with your actual Space URL
SPACE_URL="https://YOUR_USERNAME-medical-ocr-openenv.hf.space"

# Test health check
curl $SPACE_URL/

# Test reset
curl -X POST $SPACE_URL/reset \
  -H "Content-Type: application/json" \
  -d '{"task_id": "easy_printed_prescription"}'

# Test step
curl -X POST $SPACE_URL/step \
  -H "Content-Type: application/json" \
  -d '{"action": {"action_type": "process_image", "parameters": {}}}'
```

## Step 7: Run Validation Script

```bash
# Download and run official validation
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- $SPACE_URL
```

## Step 8: Test Inference Script

You can test the inference script locally (without Tesseract) or on the Space:

```bash
# Set environment variables
export OPENAI_API_KEY="your-key-here"
export MODEL_NAME="gpt-4"
export API_BASE_URL="https://api.openai.com/v1"

# Run inference
python inference.py
```

## Troubleshooting

### Build fails
- Check Dockerfile syntax
- Verify all files are committed
- Check build logs for specific errors

### Space doesn't respond
- Wait 1-2 minutes after build completes
- Check if Space is "Running" (not "Building" or "Sleeping")
- Try refreshing the Space page

### Tesseract errors
- Tesseract is installed in Docker, not needed locally
- If errors persist, check Dockerfile has tesseract-ocr package

### Inference script fails
- Verify OPENAI_API_KEY is set
- Check API quota/billing
- Try with gpt-3.5-turbo first (cheaper)

## Alternative: Test Locally with Docker

```bash
# Build image
docker build -t medical-ocr-env .

# Run container
docker run -p 7860:7860 \
  -e OPENAI_API_KEY="your-key" \
  -e MODEL_NAME="gpt-4" \
  -e API_BASE_URL="https://api.openai.com/v1" \
  medical-ocr-env

# Test
curl http://localhost:7860/
```

## Submission Checklist

Before submitting to the hackathon:

- [ ] Space is deployed and running
- [ ] Health check endpoint returns 200
- [ ] Reset endpoint works
- [ ] Step endpoint works
- [ ] Validation script passes
- [ ] Inference script completes without error
- [ ] README is comprehensive
- [ ] Test data is included
- [ ] Graders produce varying scores (already tested ✅)

## Quick Commands Reference

```bash
# Clone your space locally
git clone https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv

# Make changes and push
git add .
git commit -m "Update environment"
git push

# View logs
# Go to: https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv/logs

# Restart space
# Go to settings and click "Restart Space"
```

## Next Steps After Deployment

1. Document baseline scores in README
2. Add demo video/GIF
3. Polish documentation
4. Submit to hackathon when ready
5. Monitor for feedback and iterate

## Support

- HF Spaces docs: https://huggingface.co/docs/hub/spaces
- OpenEnv Discord: (link from hackathon page)
- Docker docs: https://docs.docker.com/
