@echo off
chcp 65001 >nul
echo ========================================
echo   深空AI生存冷链决策系统 - 启动程序
echo ========================================
echo.

cd /d "%~dp0"

echo [1/3] 检查虚拟环境...
if not exist "venv\Scripts\activate.bat" (
    echo 错误: 未找到虚拟环境，正在创建...
    python -m venv venv
)

echo [2/3] 激活虚拟环境并安装依赖...
call venv\Scripts\activate.bat
pip install -q -r backend\requirements.txt

echo [3/3] 启动后端服务...
echo.
echo ========================================
echo   后端服务已启动！
echo   API地址: http://localhost:8001
echo   WebSocket: ws://localhost:8001/ws
echo ========================================
echo.
echo 请在浏览器中打开: frontend\index.html
echo.
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

cd backend
python main.py
