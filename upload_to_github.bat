@echo off
chcp 65001
@echo =====================================================
@echo  上传到 GitHub 脚本
@echo =====================================================
echo.

set /p GITHUB_URL="请输入 GitHub 仓库地址（如：https://github.com/用户名/仓库名.git）: "

echo.
echo [1/3] 添加远程仓库...
git remote add origin %GITHUB_URL%
if errorlevel 1 (
    echo 远程仓库已存在，更新地址...
    git remote set-url origin %GITHUB_URL%
)

echo [2/3] 推送到 GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo [错误] 推送失败，可能需要登录授权。
    echo 请尝试在浏览器中登录 GitHub，然后重新运行此脚本。
    pause
    exit /b 1
)

echo [3/3] 推送完成！
echo.
echo =====================================================
echo  代码已成功上传到 GitHub！
echo =====================================================
echo.
echo 仓库地址：%GITHUB_URL%
echo.
pause
