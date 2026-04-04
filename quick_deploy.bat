@echo off
chcp 65001
echo.
echo =====================================================
echo   🚀 期现交易策略汇报软件 - 快速部署脚本
echo =====================================================
echo.

REM 检查 git
git --version >nul 2>&1
if errorlevel 1 (
    echo [✗] Git 未安装！
    echo 请先安装 Git：https://git-scm.com/download/win
    pause
    exit /b 1
)
echo [✓] Git 已安装

REM 检查 GitHub 配置
for /f "tokens=*" %%a in ('git config user.name') do set GIT_USER=%%a
if "%GIT_USER%"=="" (
    echo.
    echo [⚠] 需要配置 Git 用户信息
    set /p GIT_USERNAME="请输入你的 GitHub 用户名: "
    set /p GIT_EMAIL="请输入你的 GitHub 邮箱: "
    git config --global user.name "%GIT_USERNAME%"
    git config --global user.email "%GIT_EMAIL%"
)

echo.
echo =====================================================
echo   步骤 1: 初始化本地仓库
echo =====================================================
if not exist .git (
    git init
    echo [✓] 本地仓库已初始化
) else (
    echo [✓] 本地仓库已存在
)

echo.
echo =====================================================
echo   步骤 2: 添加文件到仓库
echo =====================================================
git add .
echo [✓] 文件已添加

echo.
echo =====================================================
echo   步骤 3: 提交代码
echo =====================================================
git commit -m "Update: 支持云端部署" 2>nul
echo [✓] 代码已提交

echo.
echo =====================================================
echo   步骤 4: 推送到 GitHub
echo =====================================================
git remote get-url origin >nul 2>&1
if errorlevel 1 (
    echo.
    echo [⚠] 尚未关联远程仓库
    echo 请在 GitHub 创建仓库后，运行以下命令：
    echo.
    echo   git remote add origin https://github.com/你的用户名/你的仓库名.git
    echo   git branch -M main
    echo   git push -u origin main
    echo.
) else (
    for /f "tokens=*" %%a in ('git remote get-url origin') do set REMOTE_URL=%%a
    echo [✓] 远程仓库: %REMOTE_URL%
    echo [⏳] 正在推送代码到 GitHub...
    git push origin main
    if errorlevel 1 (
        echo [✗] 推送失败，请检查网络或权限
    ) else (
        echo [✓] 推送成功！
    )
)

echo.
echo =====================================================
echo   部署指南
echo =====================================================
echo.
echo  接下来请按以下步骤操作：
echo.
echo  1. 确保代码已推送到 GitHub
echo.
echo  2. 访问 https://render.com 创建免费账户
echo     用 GitHub 账号登录
echo.
echo  3. 在 Render 中创建 Web Service：
echo     - 选择你的 GitHub 仓库
echo     - Build Command: pip install -r requirements.txt
echo     - Start Command: gunicorn app:app
echo.
echo  4. 添加环境变量：
echo     - DATABASE_URL: (Supabase 连接字符串)
echo     - SECRET_KEY: (随机字符串)
echo.
echo  详细步骤请查看 DEPLOY_GUIDE.md
echo.
pause
