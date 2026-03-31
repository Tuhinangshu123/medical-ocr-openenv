@echo off
echo Testing /reset endpoint...
echo.

curl -X POST https://ryozoryo-medical-ocr-openenv.hf.space/reset -H "Content-Type: application/json" -d "{\"task_id\": \"easy_printed_prescription\"}"

echo.
echo.
echo If you see observation data above, the endpoint is working!
echo If you see an error, you need to add API secrets.
pause
