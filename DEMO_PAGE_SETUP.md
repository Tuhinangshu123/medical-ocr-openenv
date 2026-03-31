# How to Make demo.html Publicly Accessible

## Option 1: Open Locally (You)

**Windows:**
1. Open File Explorer
2. Go to: `C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter\`
3. Double-click `demo.html`
4. It opens in your browser!

**Or use command:**
```bash
cd C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter
start demo.html
```

## Option 2: Add to GitHub (For Judges)

Make demo.html accessible via GitHub Pages:

### Step 1: Copy demo.html to GitHub repo
```bash
cd C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

# Copy demo.html to root of repo
cp demo.html ../../../

# Or manually copy the file to:
# C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\demo.html
```

### Step 2: Commit and push
```bash
cd C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

git add demo.html
git commit -m "Add interactive demo page"
git push origin main
```

### Step 3: Enable GitHub Pages
1. Go to: https://github.com/Tuhinangshu123/medical-ocr-openenv/settings/pages
2. Under "Source", select "main" branch
3. Click "Save"
4. Your demo will be at: https://tuhinangshu123.github.io/medical-ocr-openenv/demo.html

## Option 3: Share via HuggingFace Space

Add demo.html to your Space:

```bash
cd C:\Users\Ryo\Downloads\matrika.zip\matrika\matrika\openenv-adapter

# Add to git
git add demo.html
git commit -m "Add interactive demo page"

# Push to Space
git push space main
```

Then judges can access it at:
https://huggingface.co/spaces/ryozoryo/medical-ocr-openenv/blob/main/demo.html

(They'll need to download and open it, or you can add a static file server)

## Option 4: Use a Free Hosting Service

Upload demo.html to:
- **Netlify Drop**: https://app.netlify.com/drop
- **Vercel**: https://vercel.com
- **GitHub Gist**: https://gist.github.com (as HTML)

Just drag and drop demo.html!

## Recommended: GitHub Pages (Best for Judges)

This gives you a permanent URL like:
```
https://tuhinangshu123.github.io/medical-ocr-openenv/demo.html
```

Judges can click and test immediately!

## What Judges See in demo.html

When they open it:
1. Beautiful purple gradient interface
2. Three sections:
   - Health Check (test if Space is running)
   - Available Tasks (see all 3 tasks)
   - Run a Task (test easy/medium/hard)
3. Real-time results in console-style output
4. One-click testing with buttons

## Current Status

Your Space is already getting traffic! The logs show:
- ✅ Health checks working
- ✅ Tasks endpoint working
- ✅ Reset endpoint working

People are already testing your environment!
