@echo off
cd /d "%~dp0"
chcp 65001 >nul
echo ======================================
echo   期现交易策略汇报软件
echo ======================================
echo.

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python，请安装Python 3.8或更高版本
    pause
    exit /b 1
)

REM 安装依赖
echo 正在检查依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 警告：依赖安装可能不完整
)

echo.
echo 启动服务器...
echo 请在浏览器中访问：http://127.0.0.1:5000
echo.
python app.py

pause
