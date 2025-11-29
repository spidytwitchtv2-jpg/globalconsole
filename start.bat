@echo off
echo Starting the application...
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause