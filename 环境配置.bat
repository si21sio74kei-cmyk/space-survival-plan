@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 深空AI生存系统 - 环境配置工具

echo ========================================
echo   深空AI生存系统 - 环境配置工具
echo ========================================
echo.

REM 检查Python是否安装（尝试python和python3）
python --version >nul 2>&1
if !errorlevel! neq 0 (
    python3 --version >nul 2>&1
    if !errorlevel! neq 0 (
        echo [错误] 未检测到Python，请先安装Python 3.11或更高版本
        echo 下载地址: https://www.python.org/downloads/
        pause
        exit /b 1
    ) else (
        set PYTHON_CMD=python3
    )
) else (
    set PYTHON_CMD=python
)

echo [√] Python已安装
%PYTHON_CMD% --version

REM 检查Python版本是否>=3.11
echo [检查] 验证Python版本...
for /f "tokens=2" %%i in ('%PYTHON_CMD% --version') do set PY_VERSION=%%i
for /f "tokens=1,2 delims=." %%a in ("!PY_VERSION!") do (
    set PY_MAJOR=%%a
    set PY_MINOR=%%b
)
if !PY_MAJOR! LSS 3 (
    echo [错误] Python版本过低 (!PY_VERSION!)，需要3.11或更高版本
    pause
    exit /b 1
)
if !PY_MAJOR! EQU 3 if !PY_MINOR! LSS 11 (
    echo [错误] Python版本过低 (!PY_VERSION!)，需要3.11或更高版本
    pause
    exit /b 1
)
echo [√] Python版本符合要求 (!PY_VERSION!)
echo.

REM 创建虚拟环境
echo [步骤1] 创建虚拟环境...
if not exist "venv" (
    %PYTHON_CMD% -m venv venv
    if !errorlevel! equ 0 (
        echo [√] 虚拟环境创建成功
    ) else (
        echo [×] 虚拟环境创建失败
        pause
        exit /b 1
    )
) else (
    echo [!] 虚拟环境已存在，跳过创建
)
echo.

REM 激活虚拟环境并安装依赖
echo [步骤2] 激活虚拟环境...
call "%~dp0venv\Scripts\activate.bat"
if !errorlevel! neq 0 (
    echo [×] 虚拟环境激活失败
    echo [提示] 请确保项目路径不含特殊字符
    pause
    exit /b 1
)
echo [√] 虚拟环境激活成功
echo.

REM 升级pip
echo [步骤3] 升级pip...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
if !errorlevel! equ 0 (
    echo [√] pip升级成功
) else (
    echo [!] 清华源升级失败，尝试默认源...
    python -m pip install --upgrade pip --quiet
    if !errorlevel! equ 0 (
        echo [√] pip升级成功
    ) else (
        echo [!] pip升级可能存在问题，继续安装依赖
    )
)
echo.

REM 安装依赖包（优先使用清华镜像源）
echo [步骤4] 安装项目依赖包...
echo [提示] 正在使用清华镜像源加速下载...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if !errorlevel! neq 0 (
    echo [!] 清华源安装失败，尝试默认源...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [×] 依赖包安装失败
        echo.
        echo [可能的原因]
        echo   1. 网络连接问题 - 请检查网络后重试
        echo   2. 权限不足 - 尝试以管理员身份运行此脚本
        echo   3. Python版本不兼容 - 确认Python版本>=3.11
        echo.
        echo [手动安装命令]
        echo   pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)
echo [√] 依赖包安装成功
echo.

REM 检查环境变量文件
echo [步骤5] 检查环境变量配置...
if not exist ".env" (
    echo [!] 未找到.env文件，从.env.example复制模板
    copy .env.example .env >nul
    echo [√] 已创建.env文件
    echo.
    echo [重要] 请编辑.env文件，填入您的API密钥：
    echo   - DEEPSEEK_API_KEY: DeepSeek API密钥
    echo   获取地址: https://platform.deepseek.com/
    echo.
) else (
    echo [√] .env文件已存在
)
echo.

REM 显示安装结果
echo ========================================
echo   环境配置完成！
echo ========================================
echo.
echo 已安装的依赖包：
pip list
echo.
echo 下一步操作：
echo 1. 编辑.env文件，填入您的API密钥
echo 2. 运行 '启动应用.bat' 启动系统
echo 3. 访问 http://localhost:5000
echo.
pause
