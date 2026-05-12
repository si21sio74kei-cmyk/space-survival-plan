@echo off
chcp 65001 >nul
echo ========================================
echo   深空AI生存系统 - Flask版本
echo ========================================
echo.
echo 正在启动服务器...
echo 访问地址: http://localhost:5000
echo.

cd /d "%~dp0"
python app.py

pause
