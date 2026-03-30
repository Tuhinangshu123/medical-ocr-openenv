@echo off
REM Quick deployment script for Hugging Face Spaces (Windows)

echo ==========================================
echo Medical OCR OpenEnv - Quick Deploy
echo ==========================================
echo.

REM Check if git is initialized
if not exist ".git" (
    echo Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit: Medical OCR OpenEnv environment"
)

REM Get HF username and space name
set /p HF_USERNAME="Enter your Hugging Face username: "
set /p SPACE_NAME="Enter your Space name (e.g., medical-ocr-openenv): "

REM Add remote
set SPACE_URL=https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
echo.
echo Adding remote: %SPACE_URL%

git remote | findstr "space" >nul
if %errorlevel% equ 0 (
    echo Remote 'space' already exists, updating...
    git remote set-url space %SPACE_URL%
) else (
    git remote add space %SPACE_URL%
)

REM Push to space
echo.
echo Pushing to Hugging Face Space...
echo You may need to login with: huggingface-cli login
echo.

git push space main

echo.
echo ==========================================
echo Deployment initiated!
echo ==========================================
echo.
echo Next steps:
echo 1. Go to: https://huggingface.co/spaces/%HF_USERNAME%/%SPACE_NAME%
echo 2. Wait for build to complete (5-10 minutes)
echo 3. Set environment secrets in Settings:
echo    - OPENAI_API_KEY
echo    - MODEL_NAME (e.g., gpt-4)
echo    - API_BASE_URL (e.g., https://api.openai.com/v1)
echo 4. Test the Space:
echo    curl https://%HF_USERNAME%-%SPACE_NAME%.hf.space/
echo 5. Run validation script
echo.
echo Good luck! 🚀
echo.
pause
