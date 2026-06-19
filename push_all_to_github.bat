@echo off
REM Push all code to GitHub. Requires GITHUB_TOKEN env var or git credentials configured.
cd /d D:\Lobster_Workspace

REM Set remote (first time only, ignore error if exists)
git remote add origin https://github.com/wanhe-tools/wanhe-tools.git 2>nul

REM If GITHUB_TOKEN is set, use it for auth
if defined GITHUB_TOKEN (
    git remote set-url origin https://x-access-token:%GITHUB_TOKEN%@github.com/wanhe-tools/wanhe-tools.git
)

git add .
git commit -m "Auto update: %date% %time%"
git push -u origin main

if %errorlevel% equ 0 (
    echo Push successful!
) else (
    echo Push failed. Check your GitHub token or network.
)
pause
