@echo off
echo [%date% %time%] Starting AI Toolbox...
start "ToolboxBackend" "C:\Users\鹈垣\AppData\Local\Programs\Python\Python313\python.exe" "D:\Lobster_Workspace\projects\ai_toolbox\toolbox_backend.py"
timeout /t 3 >nul
echo Toolbox started: http://localhost:8888
