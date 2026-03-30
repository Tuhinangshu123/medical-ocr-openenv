# Complete Setup Instructions

## 📋 What You Need

Before starting, gather:

1. **GitHub Account** - https://github.com/signup
2. **HuggingFace Account** - https://huggingface.co/join
3. **OpenAI API Key** (optional) - https://platform.openai.com/api-keys
4. **Git installed** - https://git-scm.com/downloads

## 🚀 Complete Setup Process

### Step 1: Prepare Your Accounts

#### 1.1 GitHub Setup
1. Create account at https://github.com/signup
2. Verify your email
3. Note your username: `YOUR_GITHUB_USERNAME`

#### 1.2 HuggingFace Setup
1. Create account at https://huggingface.co/join
2. Verify your email
3. Note your username: `YOUR_HF_USERNAME`
4. Get your token:
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Name: "OpenEnv Deployment"
   - Role: "Write"
   - Copy the token

#### 1.3 OpenAI Setup (Optional)
1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Name it "OpenEnv Testing"
4. Copy the key (starts with `sk-...`)

### Step 2: Local Setup

Open PowerShell in the `openenv-adapter` directory:

```powershell
# You should be here:
# C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

# Check git is installed
git --version

# If not installed, download from: https://git-scm.com/downloads
```

### Step 3: Initialize Git Repository

```powershell
# Initialize git
git init

# Configure git (replace with YOUR info)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Medical OCR OpenEnv environment"
```

### Step 4: Create GitHub Repository

#### Option A: Via GitHub Website (Easier)
1. Go to https://github.com/new
2. Repository name: `medical-ocr-openenv`
3. Description: `OpenEnv environment for medical prescription OCR`
4. Visibility: Public
5. **DO NOT** initialize with README, .gitignore, or license (we have them)
6. Click "Create repository"

#### Option B: Via GitHub CLI
```powershell
# Install GitHub CLI: https://cli.github.com/
gh repo create medical-ocr-openenv --public --source=. --remote=origin
```

### Step 5: Push to GitHub

```powershell
# Add GitHub as remote (replace YOUR_GITHUB_USERNAME)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/medical-ocr-openenv.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Step 6: Create HuggingFace Space

1. Go to https://huggingface.co/new-space
2. Fill in:
   - **Owner**: Your username
   - **Space name**: `medical-ocr-openenv`
   - **License**: MIT
   - **Select the SDK**: Docker
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public
3. Click "Create Space"
4. After creation, click "Settings" and add tag: `openenv`

### Step 7: Push to HuggingFace Space

```powershell
# Login to HuggingFace
pip install huggingface_hub
huggingface-cli login
# Paste your HF token when prompted

# Add HF Space as remote (replace YOUR_HF_USERNAME)
git remote add space https://huggingface.co/spaces/YOUR_HF_USERNAME/medical-ocr-openenv

# Push to Space
git push space main
```

### Step 8: Configure Space Secrets

1. Go to your Space: `https://huggingface.co/spaces/YOUR_HF_USERNAME/medical-ocr-openenv`
2. Click "Settings" tab
3. Scroll to "Repository secrets"
4. Add these secrets:

**Secret 1:**
- Name: `OPENAI_API_KEY`
- Value: Your OpenAI API key (or leave empty for now)

**Secret 2:**
- Name: `MODEL_NAME`
- Value: `gpt-4` (or `gpt-3.5-turbo`)

**Secret 3:**
- Name: `API_BASE_URL`
- Value: `https://api.openai.com/v1`

### Step 9: Wait for Build

1. Go to your Space page
2. Click "Logs" tab
3. Watch the build (5-10 minutes)
4. Wait for status: "Running"

### Step 10: Test Your Deployment

```powershell
# Test health check (replace YOUR_HF_USERNAME)
curl https://YOUR_HF_USERNAME-medical-ocr-openenv.hf.space/

# Expected response:
# {"name":"Medical Prescription OCR Environment","version":"1.0.0","status":"running","openenv":true}
```

### Step 11: Run Validation

```bash
# If you have bash/WSL
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://YOUR_HF_USERNAME-medical-ocr-openenv.hf.space
```

## ✅ Verification Checklist

After setup, verify:

- [ ] GitHub repository created and pushed
- [ ] HuggingFace Space created
- [ ] Space has "openenv" tag
- [ ] Space is "Running" (not Building or Sleeping)
- [ ] Health check returns 200
- [ ] Reset endpoint works
- [ ] Step endpoint works
- [ ] Validation script passes

## 📝 Your URLs

After setup, you'll have:

- **GitHub Repo**: `https://github.com/YOUR_GITHUB_USERNAME/medical-ocr-openenv`
- **HF Space**: `https://huggingface.co/spaces/YOUR_HF_USERNAME/medical-ocr-openenv`
- **Live API**: `https://YOUR_HF_USERNAME-medical-ocr-openenv.hf.space`

## 🆘 Troubleshooting

### Git push fails
```powershell
# Check remote is correct
git remote -v

# If wrong, remove and re-add
git remote remove origin
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/medical-ocr-openenv.git
```

### HuggingFace login fails
```powershell
# Make sure you have a token with "Write" permissions
# Get new token: https://huggingface.co/settings/tokens
huggingface-cli login
```

### Space build fails
- Check "Logs" tab for errors
- Common issues:
  - Dockerfile syntax error
  - Missing files
  - Wrong Python version
- Fix and push again: `git push space main --force`

### Can't access Space URL
- Wait 1-2 minutes after build completes
- Check Space status is "Running"
- Try refreshing the page
- Check Space isn't "Sleeping" (click to wake it)

## 🎯 Next Steps

After successful setup:

1. Test all endpoints
2. Run validation script
3. Document baseline scores
4. Submit to hackathon!

## 📞 Need Help?

- GitHub Docs: https://docs.github.com
- HuggingFace Docs: https://huggingface.co/docs/hub/spaces
- OpenEnv Discord: (link from hackathon page)

## 🎉 You're Ready!

Once all steps are complete, your environment is live and ready for submission!
