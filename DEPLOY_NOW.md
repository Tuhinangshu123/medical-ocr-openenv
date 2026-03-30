# 🚀 DEPLOY NOW - Simple Manual Steps

You're already in the right directory! Here's what to do:

## Step 1: Initialize Git (if needed)

```powershell
# Check if git is initialized
git status

# If you get an error, initialize git:
git init
git add .
git commit -m "Initial commit: Medical OCR OpenEnv"
```

## Step 2: Create Hugging Face Space

1. Open browser: https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `medical-ocr-openenv`
   - **License**: MIT
   - **Select the SDK**: Docker
   - **Space hardware**: CPU basic (free)
3. Click "Create Space"
4. **IMPORTANT**: Add tag `openenv` after creation (in Space settings)

## Step 3: Get Your Space URL

After creating, you'll see your Space at:
```
https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv
```

Note down YOUR_USERNAME - you'll need it!

## Step 4: Login to Hugging Face (if needed)

```powershell
# Install HF CLI if not installed
pip install huggingface_hub

# Login
huggingface-cli login
```

It will ask for your token. Get it from: https://huggingface.co/settings/tokens

## Step 5: Add Remote and Push

Replace `YOUR_USERNAME` with your actual HuggingFace username:

```powershell
# Add HF Space as remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv

# Push to Space
git push space main
```

If `main` branch doesn't exist, try:
```powershell
git branch -M main
git push space main
```

## Step 6: Set Environment Secrets

1. Go to: `https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv/settings`
2. Scroll down to "Repository secrets"
3. Click "Add a secret" three times to add:

**Secret 1:**
- Name: `OPENAI_API_KEY`
- Value: Your OpenAI API key (get from https://platform.openai.com/api-keys)

**Secret 2:**
- Name: `MODEL_NAME`
- Value: `gpt-4` (or `gpt-3.5-turbo` for cheaper testing)

**Secret 3:**
- Name: `API_BASE_URL`
- Value: `https://api.openai.com/v1`

## Step 7: Wait for Build

1. Go to your Space: `https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv`
2. Click on "Logs" tab
3. Watch the build progress (takes 5-10 minutes)
4. Wait until status changes from "Building" to "Running"

## Step 8: Test Your Space

Once it's "Running", test it:

```powershell
# Replace YOUR_USERNAME with your actual username
curl https://YOUR_USERNAME-medical-ocr-openenv.hf.space/
```

Expected response:
```json
{
  "name": "Medical Prescription OCR Environment",
  "version": "1.0.0",
  "status": "running",
  "openenv": true
}
```

## Step 9: Test Reset Endpoint

```powershell
curl -X POST https://YOUR_USERNAME-medical-ocr-openenv.hf.space/reset -H "Content-Type: application/json" -d '{\"task_id\": \"easy_printed_prescription\"}'
```

## Step 10: Run Validation (Optional)

If you have bash/WSL:
```bash
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://YOUR_USERNAME-medical-ocr-openenv.hf.space
```

## ✅ You're Done!

Your environment is now live at:
```
https://YOUR_USERNAME-medical-ocr-openenv.hf.space
```

You can submit this URL to the hackathon!

## 🆘 Troubleshooting

### "git push failed - authentication required"
Run: `huggingface-cli login` and enter your token

### "Space build failed"
- Check the "Logs" tab in your Space
- Look for red error messages
- Common fix: Make sure all files are committed (`git add .` then `git commit`)

### "Space shows 404"
- Wait 1-2 minutes after build completes
- Refresh the page
- Check status is "Running" not "Sleeping"

### "Don't have OpenAI API key"
- You can still deploy without it
- Just skip the secrets for now
- Add them later when you have a key
- The Space will still deploy and pass validation

## 📋 Quick Command Reference

```powershell
# You're here: C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

# Initialize git
git init
git add .
git commit -m "Initial commit"

# Add remote (replace YOUR_USERNAME)
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/medical-ocr-openenv

# Push
git push space main

# Test (replace YOUR_USERNAME)
curl https://YOUR_USERNAME-medical-ocr-openenv.hf.space/
```

## 🎉 Next Steps

After deployment:
1. Test all endpoints work
2. Run validation script
3. Document your Space URL
4. Submit to hackathon!

Good luck! 🚀
