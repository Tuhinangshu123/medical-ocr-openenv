# 🚀 YOUR PERSONALIZED DEPLOYMENT GUIDE

## Your Information
- **GitHub**: Tuhinangshu123
- **HuggingFace**: ryozoryo
- **OpenAI API Key**: ✅ Provided

## Your URLs (After Deployment)
- **GitHub Repo**: https://github.com/Tuhinangshu123/medical-ocr-openenv
- **HF Space**: https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv
- **Live API**: https://ryozoryo-medical-ocr-openenv.hf.space

---

## 🎯 COPY-PASTE COMMANDS (Ready to Run!)

### Step 1: Initialize Git (2 minutes)

```powershell
# You should be in: C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

# Initialize git
git init

# Configure git
git config user.name "Tuhinangshu Das"
git config user.email "tuhinangshudas610@gmail.com"

# Add all files
git add .

# Create commit
git commit -m "Initial commit: Medical OCR OpenEnv for hackathon"

# Create main branch
git branch -M main
```

---

### Step 2: Create GitHub Repository (3 minutes)

**Do this in your browser:**

1. Go to: https://github.com/new
2. Repository name: `medical-ocr-openenv`
3. Description: `OpenEnv environment for medical prescription OCR - Hackathon submission`
4. Public: ✅ YES
5. Initialize with: ❌ NOTHING (leave all unchecked)
6. Click "Create repository"

---

### Step 3: Push to GitHub (1 minute)

```powershell
# Add GitHub remote
git remote add origin https://github.com/Tuhinangshu123/medical-ocr-openenv.git

# Push to GitHub
git push -u origin main
```

**✅ Check**: Visit https://github.com/Tuhinangshu123/medical-ocr-openenv

---

### Step 4: Create HuggingFace Space (5 minutes)

**Do this in your browser:**

1. Go to: https://huggingface.co/new-space
2. Owner: ryozoryo
3. Space name: `medical-ocr-openenv`
4. License: MIT
5. SDK: **Docker** ⚠️ IMPORTANT
6. Hardware: CPU basic (free)
7. Public: ✅ YES
8. Click "Create Space"

**After creation:**
- Click "Settings" tab
- Scroll to "Tags"
- Add tag: `openenv` ⚠️ REQUIRED
- Save

---

### Step 5: Login to HuggingFace (2 minutes)

```powershell
# Install HF CLI (if not installed)
pip install huggingface_hub

# Login
huggingface-cli login
```

When prompted, paste your HF token from: https://huggingface.co/settings/tokens
(Create new token with "Write" permission if you don't have one)

---

### Step 6: Push to HuggingFace Space (1 minute)

```powershell
# Add HF Space remote
git remote add space https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv

# Push to Space
git push space main
```

**✅ Check**: Visit https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv

---

### Step 7: Add Environment Secrets (3 minutes)

**Do this in your browser:**

1. Go to: https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv/settings
2. Scroll to "Repository secrets"
3. Add these 3 secrets:

**Secret 1:**
- Name: `OPENAI_API_KEY`
- Value: `your-openai-api-key-here` (use your actual key)

**Secret 2:**
- Name: `MODEL_NAME`
- Value: `gpt-4`

**Secret 3:**
- Name: `API_BASE_URL`
- Value: `https://api.openai.com/v1`

---

### Step 8: Wait for Build (10 minutes)

1. Go to: https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv
2. Click "Logs" tab
3. Watch the build (takes 5-10 minutes)
4. Wait for status: "Running" ✅

---

### Step 9: Test Your Deployment (2 minutes)

Once "Running", test these:

```powershell
# Test 1: Health check
curl https://ryozoryo-medical-ocr-openenv.hf.space/

# Test 2: List tasks
curl https://ryozoryo-medical-ocr-openenv.hf.space/tasks

# Test 3: Reset environment
curl -X POST https://ryozoryo-medical-ocr-openenv.hf.space/reset -H "Content-Type: application/json" -d "{\"task_id\": \"easy_printed_prescription\"}"
```

**Expected**: All return JSON responses

---

### Step 10: Run Validation (Optional, 5 minutes)

If you have Git Bash or WSL:

```bash
curl -fsSL https://raw.githubusercontent.com/openenv/openenv/main/scripts/validate-submission.sh | bash -s -- https://ryozoryo-medical-ocr-openenv.hf.space
```

---

## ✅ SUCCESS CHECKLIST

After completing all steps:

- [ ] GitHub repo created: https://github.com/Tuhinangshu123/medical-ocr-openenv
- [ ] HF Space created: https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv
- [ ] Space has "openenv" tag
- [ ] Space status is "Running"
- [ ] Health check works: `curl https://ryozoryo-medical-ocr-openenv.hf.space/`
- [ ] All 3 environment secrets added
- [ ] Can access live API

---

## 🎉 YOU'RE DONE!

Your submission URL for the hackathon:
```
https://ryozoryo-medical-ocr-openenv.hf.space
```

---

## 🆘 Quick Troubleshooting

### Git push asks for password
Use your GitHub Personal Access Token:
1. Go to: https://github.com/settings/tokens
2. Generate new token (classic)
3. Select "repo" scope
4. Use token as password when prompted

### HF Space build fails
Check logs at: https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv/logs
Common fix: `git add . && git commit -m "fix" && git push space main`

### Space shows "Sleeping"
Click on the Space to wake it up, wait 30 seconds

---

## 📊 Timeline

- Step 1-3 (Git + GitHub): 6 minutes
- Step 4-6 (HF Space): 8 minutes
- Step 7 (Secrets): 3 minutes
- Step 8 (Build): 10 minutes
- Step 9-10 (Test): 7 minutes

**Total: ~35 minutes**

---

## 🏆 Next Steps

1. Test all endpoints work
2. Submit your Space URL to hackathon
3. Monitor Space logs for any issues
4. Update README with your Space URL

Good luck! 🚀
