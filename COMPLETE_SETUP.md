# 🚀 Complete Professional Setup Guide

## Overview

This guide will help you deploy your Medical OCR OpenEnv environment to both GitHub and HuggingFace Spaces for the hackathon submission.

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Git installed (check: `git --version`)
- [ ] GitHub account created
- [ ] HuggingFace account created
- [ ] OpenAI API key (optional, can add later)

## 🎯 Setup Process (Step-by-Step)

### Phase 1: Local Git Setup (5 minutes)

Open PowerShell in the `openenv-adapter` directory and run:

```powershell
# 1. Initialize git repository
git init

# 2. Configure git with your information
git config user.name "Your Name"
git config user.email "your.email@example.com"

# 3. Add all files
git add .

# 4. Create initial commit
git commit -m "Initial commit: Medical OCR OpenEnv environment for hackathon"

# 5. Create main branch
git branch -M main
```

**✅ Checkpoint**: Run `git log` - you should see your commit

---

### Phase 2: GitHub Repository Setup (5 minutes)

#### Option A: Via GitHub Website (Recommended)

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `medical-ocr-openenv`
   - **Description**: `OpenEnv environment for medical prescription OCR - Hackathon submission`
   - **Visibility**: Public ✅
   - **Initialize**: Leave ALL unchecked (we have files already)
3. Click "Create repository"
4. Copy the repository URL shown (looks like: `https://github.com/USERNAME/medical-ocr-openenv.git`)

#### Option B: Via GitHub CLI

```powershell
# Install GitHub CLI from: https://cli.github.com/
gh auth login
gh repo create medical-ocr-openenv --public --source=. --remote=origin --push
```

---

### Phase 3: Push to GitHub (2 minutes)

```powershell
# Add GitHub as remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/USERNAME/medical-ocr-openenv.git

# Push to GitHub
git push -u origin main
```

**✅ Checkpoint**: Visit `https://github.com/USERNAME/medical-ocr-openenv` - you should see all files

---

### Phase 4: HuggingFace Space Setup (10 minutes)

#### Step 4.1: Create Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `medical-ocr-openenv`
   - **License**: MIT
   - **SDK**: Docker ⚠️ IMPORTANT
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public
3. Click "Create Space"

#### Step 4.2: Add OpenEnv Tag

1. After creation, click "Settings" tab
2. Scroll to "Tags"
3. Add tag: `openenv` ⚠️ REQUIRED for hackathon
4. Save

#### Step 4.3: Login to HuggingFace

```powershell
# Install HuggingFace CLI
pip install huggingface_hub

# Login (will open browser for authentication)
huggingface-cli login
```

When prompted, paste your token from: https://huggingface.co/settings/tokens
(Create new token with "Write" permission if needed)

#### Step 4.4: Push to Space

```powershell
# Add HF Space as remote (replace USERNAME with your HF username)
git remote add space https://huggingface.co/spaces/USERNAME/medical-ocr-openenv

# Push to Space
git push space main
```

**✅ Checkpoint**: Go to your Space page - you should see "Building" status

---

### Phase 5: Configure Environment Variables (5 minutes)

While the Space is building:

1. Go to: `https://huggingface.co/spaces/USERNAME/medical-ocr-openenv/settings`
2. Scroll to "Repository secrets"
3. Add these three secrets:

**Secret 1: OPENAI_API_KEY**
- Click "Add a secret"
- Name: `OPENAI_API_KEY`
- Value: Your OpenAI API key (or `sk-dummy-key-for-testing` if you don't have one)
- Click "Save"

**Secret 2: MODEL_NAME**
- Click "Add a secret"
- Name: `MODEL_NAME`
- Value: `gpt-4` (or `gpt-3.5-turbo` for cheaper)
- Click "Save"

**Secret 3: API_BASE_URL**
- Click "Add a secret"
- Name: `API_BASE_URL`
- Value: `https://api.openai.com/v1`
- Click "Save"

---

### Phase 6: Wait for Build (10 minutes)

1. Go to your Space: `https://huggingface.co/spaces/USERNAME/medical-ocr-openenv`
2. Click "Logs" tab
3. Watch the build progress
4. Wait for status to change from "Building" → "Running"

**Common build steps you'll see:**
- Pulling Docker base image
- Installing system packages (tesseract)
- Installing Python packages
- Starting server

**✅ Checkpoint**: Status shows "Running" with green indicator

---

### Phase 7: Test Deployment (5 minutes)

Once "Running", test your endpoints:

#### Test 1: Health Check
```powershell
curl https://USERNAME-medical-ocr-openenv.hf.space/
```

**Expected response:**
```json
{
  "name": "Medical Prescription OCR Environment",
  "version": "1.0.0",
  "status": "running",
  "openenv": true
}
```

#### Test 2: List Tasks
```powershell
curl https://USERNAME-medical-ocr-openenv.hf.space/tasks
```

**Expected response:**
```json
{
  "tasks": [
    {"id": "easy_printed_prescription", "difficulty": "easy", ...},
    {"id": "medium_handwritten_prescription", "difficulty": "medium", ...},
    {"id": "hard_complex_prescription", "difficulty": "hard", ...}
  ]
}
```

#### Test 3: Reset Environment
```powershell
curl -X POST https://USERNAME-medical-ocr-openenv.hf.space/reset -H "Content-Type: application/json" -d "{\"task_id\": \"easy_printed_prescription\"}"
```

**Expected**: JSON with observation data

---

### Phase 8: Run Official Validation (5 minutes)

If you have bash/WSL/Git Bash:

```bash
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://USERNAME-medical-ocr-openenv.hf.space
```

**Expected output:**
```
✅ HF Space deploys
✅ OpenEnv spec compliance
✅ Dockerfile builds
✅ Baseline reproducible
✅ 3+ tasks with graders
```

---

### Phase 9: Test Inference Script (Optional, 10 minutes)

If you have an OpenAI API key:

```powershell
# Set environment variables
$env:OPENAI_API_KEY="your-api-key-here"
$env:MODEL_NAME="gpt-4"
$env:API_BASE_URL="https://api.openai.com/v1"

# Run inference
python inference.py
```

This will test the baseline agent and produce scores.

---

## ✅ Final Verification Checklist

Before submitting to hackathon:

- [ ] GitHub repository is public and accessible
- [ ] HuggingFace Space is public and running
- [ ] Space has "openenv" tag
- [ ] Health check endpoint returns 200
- [ ] Reset endpoint works
- [ ] Step endpoint works
- [ ] Tasks endpoint lists 3 tasks
- [ ] Validation script passes (if you ran it)
- [ ] Space URL is documented

---

## 📝 Your Submission URLs

After completion, you'll have:

**GitHub Repository:**
```
https://github.com/USERNAME/medical-ocr-openenv
```

**HuggingFace Space:**
```
https://huggingface.co/spaces/USERNAME/medical-ocr-openenv
```

**Live API Endpoint:**
```
https://USERNAME-medical-ocr-openenv.hf.space
```

**Submit this URL to the hackathon!** ☝️

---

## 🆘 Troubleshooting

### Issue: "git push" asks for password

**Solution:**
```powershell
# Use personal access token instead
# Get token from: https://github.com/settings/tokens
# When prompted for password, paste the token
```

### Issue: HuggingFace build fails

**Check:**
1. Go to "Logs" tab
2. Look for red error messages
3. Common fixes:
   - Make sure all files are committed: `git add . && git commit -m "fix" && git push space main`
   - Check Dockerfile syntax
   - Verify requirements.txt is present

### Issue: Space shows "Sleeping"

**Solution:**
- Click on the Space to wake it up
- Wait 30 seconds for it to start
- Free tier Spaces sleep after inactivity

### Issue: Endpoints return 404

**Solution:**
- Wait 1-2 minutes after build completes
- Refresh the Space page
- Check status is "Running" not "Building"

### Issue: Validation script fails

**Solution:**
- Make sure Space is fully running
- Test endpoints manually first
- Check Space logs for errors
- Verify openenv.yaml is present

---

## 🎯 What to Do After Setup

1. **Document your Space URL** in README.md
2. **Test all endpoints** work correctly
3. **Take screenshots** of working environment
4. **Submit to hackathon** with your Space URL
5. **Monitor Space logs** for any issues

---

## 📊 Expected Timeline

- Phase 1 (Local Git): 5 minutes
- Phase 2 (GitHub): 5 minutes
- Phase 3 (Push): 2 minutes
- Phase 4 (HF Space): 10 minutes
- Phase 5 (Secrets): 5 minutes
- Phase 6 (Build): 10 minutes
- Phase 7 (Test): 5 minutes
- Phase 8 (Validate): 5 minutes

**Total: ~45 minutes**

---

## 🎉 Success!

Once all phases are complete:
- ✅ Your environment is live
- ✅ It's accessible via public URL
- ✅ It's ready for hackathon submission
- ✅ Judges can test it automatically

**You're ready to win! 🏆**

---

## 📞 Need Help?

- **GitHub Issues**: https://github.com/USERNAME/medical-ocr-openenv/issues
- **HF Discussions**: https://huggingface.co/spaces/USERNAME/medical-ocr-openenv/discussions
- **OpenEnv Discord**: (link from hackathon page)

---

## 📚 Additional Resources

- `SETUP_INSTRUCTIONS.md` - Detailed setup guide
- `DEPLOY_GUIDE.md` - Deployment specifics
- `README.md` - Environment documentation
- `FINAL_CHECKLIST.md` - Pre-submission checklist
- `TROUBLESHOOTING.md` - Common issues and fixes
