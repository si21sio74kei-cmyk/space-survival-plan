@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   深空AI生存系统 - 太空数据中心测试
echo ========================================
echo.
echo 步骤1: 安装依赖包...
echo.

pip install requests -q

if %errorlevel% neq 0 (
    echo.
    echo [错误] 依赖安装失败！
    pause
    exit /b 1
)

echo.
echo [成功] 依赖安装完成
echo.
echo ========================================
echo 步骤2: 启动Flask应用...
echo ========================================
echo.
echo 提示: 请保持此窗口运行，在新窗口中访问 http://localhost:5000
echo.

start python app.py

echo.
echo 等待应用启动...
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo 步骤3: 运行API测试...
echo ========================================
echo.

python test_space_api.py

echo.
echo ========================================
echo 测试完成！
echo ========================================
echo.
echo 下一步操作:
echo 1. 打开浏览器访问 http://localhost:5000
echo 2. 点击左侧导航栏的"太空数据中心"（卫星图标）
echo 3. 查看实时太空/地球数据
echo.
pause
