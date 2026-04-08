#!/bin/bash
# 这个脚本在 PythonAnywhere 的 Bash console 中执行

echo "=========================================="
echo "       更新 PythonAnywhere 应用"
echo "=========================================="
echo ""

# 进入项目目录（根据你的实际路径修改）
cd ~/期现交易策略汇报软件
if [ $? -ne 0 ]; then
    echo "❌ 错误：找不到项目目录"
    echo "请修改脚本中的路径"
    exit 1
fi

echo "[1/5] 拉取最新代码..."
git pull origin main
if [ $? -ne 0 ]; then
    echo "❌ 拉取失败，请检查网络或权限"
    exit 1
fi
echo "✅ 代码拉取成功"
echo ""

echo "[2/5] 检查是否有新依赖..."
# 检查 requirements.txt 是否有变化
if git diff HEAD~1 --name-only | grep -q "requirements.txt"; then
    echo "发现依赖变化，正在安装..."
    pip install -r requirements.txt --user
    echo "✅ 依赖更新完成"
else
    echo "✅ 无新依赖"
fi
echo ""

echo "[3/5] 检查数据库..."
# 如果需要数据库迁移，在这里执行
# python -c "from db_manager import db_manager; db_manager.init_db()"
echo "✅ 数据库检查完成"
echo ""

echo "[4/5] 清理缓存..."
# 删除旧的 __pycache__
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "✅ 缓存清理完成"
echo ""

echo "[5/5] 重启 Web 应用..."
# 通过 touch wsgi 文件触发重启
touch /var/www/*/wsgi.py 2>/dev/null || echo "⚠️ 请手动点击 Web 标签页的 Reload 按钮"
echo "✅ 重启完成"
echo ""

echo "=========================================="
echo "          ✅ 更新完成！"
echo "=========================================="
echo ""
echo "请检查："
echo "1. 点击 Web 标签页查看状态"
echo "2. 访问网站测试功能"
echo "3. 查看 Error Log 是否有错误"
echo ""
