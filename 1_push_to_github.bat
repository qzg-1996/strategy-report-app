@echo off
chcp 65001
echo ===== 推送到 GitHub =====
cd /d "C:\Users\15199\Desktop\期现交易策略汇报软件"

echo [1/4] 检查修改状态...
git status

echo.
echo [2/4] 添加修改...
git add .

echo.
echo [3/4] 提交修改...
git commit -m "优化基差走势图：支持自定义时间范围，优化策略匹配逻辑"

echo.
echo [4/4] 推送到 GitHub...
git push origin main

echo.
echo ===== 推送完成 =====
echo.
echo 如果推送成功，请去 PythonAnywhere 更新代码
echo.
pause
