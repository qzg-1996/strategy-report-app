@echo off
chcp 65001
@echo =====================================================
@echo  期现交易策略汇报软件 - Git 初始化脚本
@echo =====================================================
echo.

REM 检查 git 是否安装
git --version >nul 2>&1
if errorlevel 1 (
    echo [错误] Git 未安装，请先安装 Git！
    echo 下载地址：https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [1/5] Git 已安装，继续初始化...

REM 配置用户信息（如果还没配置）
echo [2/5] 配置 Git 用户信息...
git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

REM 初始化本地仓库
echo [3/5] 初始化本地 Git 仓库...
git init

REM 添加所有文件
echo [4/5] 添加文件到仓库...
git add .

REM 提交
echo [5/5] 提交代码...
git commit -m "Initial commit: 期现交易策略汇报软件"

echo.
echo =====================================================
echo  本地仓库初始化完成！
echo =====================================================
echo.
echo 接下来请执行：
echo 1. 在 GitHub 创建仓库：https://github.com/new
    echo 2. 获取仓库地址（如：https://github.com/用户名/仓库名.git）
echo 3. 运行 upload_to_github.bat 上传到 GitHub
echo.
pause
