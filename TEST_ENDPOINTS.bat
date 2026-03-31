@echo off
REM Test all OpenEnv endpoints

echo ========================================
echo Testing Medical OCR OpenEnv Endpoints
echo ========================================
echo.

echo [1/4] Testing health endpoint...
curl https://ryozoryo-medical-ocr-openenv.hf.space/
echo.
echo.

echo [2/4] Testing tasks list...
curl https://ryozoryo-medical-ocr-openenv.hf.space/tasks
echo.
echo.

echo [3/4] Testing reset endpoint (easy task)...
curl -X POST https://ryozoryo-medical-ocr-openenv.hf.space/reset -H "Content-Type: application/json" -d "{\"task_id\": \"easy_printed_prescription\"}"
echo.
echo.

echo [4/4] Testing state endpoint...
curl https://ryozoryo-medical-ocr-openenv.hf.space/state
echo.
echo.

echo ========================================
echo All tests complete!
echo ========================================
pause
