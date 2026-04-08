# 云端更新指南（Git + PythonAnywhere）

## 更新流程

### 第一步：本地更新并推送

```bash
# 1. 进入项目目录
cd "C:\Users\15199\Desktop\期现交易策略汇报软件"

# 2. 查看修改状态
git status

# 3. 添加所有修改
git add .

# 4. 提交修改（写有意义的提交信息）
git commit -m "优化基差走势图：支持自定义时间范围，交互式图表"

# 5. 推送到 GitHub
git push origin main
```

### 第二步：PythonAnywhere 拉取更新

#### 方法 A：通过 Web 控制台（推荐）

1. 登录 PythonAnywhere: https://www.pythonanywhere.com
2. 打开 **Consoles** 标签
3. 点击你的 **Bash console**（或新建一个）
4. 执行以下命令：

```bash
# 进入项目目录
cd ~/期现交易策略汇报软件  # 或者你的实际项目路径

# 拉取最新代码
git pull origin main

# 如果有新的依赖，安装更新
pip install -r requirements.txt --user

# 重启 Web 应用
# 方法1：点击 Web 标签页的 "Reload" 按钮
# 方法2：或执行触摸 wsgi 文件
touch /var/www/www_yourdomain_com_wsgi.py
```

#### 方法 B：通过 SSH（如果你开通了 SSH 权限）

```bash
ssh your_username@ssh.pythonanywhere.com
cd ~/期现交易策略汇报软件
git pull origin main
pip install -r requirements.txt --user
touch /var/www/www_yourdomain_com_wsgi.py
```

---

## 一键更新脚本

### 本地推送脚本（Windows）

创建文件 `push_to_cloud.bat`：

```batch
@echo off
chcp 65001
echo ===== 推送到云端 =====
cd /d "C:\Users\15199\Desktop\期现交易策略汇报软件"

echo [1/3] 检查修改...
git status

echo [2/3] 提交修改...
git add .
git commit -m "update: %date% %time%"

echo [3/3] 推送到 GitHub...
git push origin main

echo ===== 推送完成 =====
pause
```

### PythonAnywhere 更新脚本

在 PythonAnywhere 的 Bash console 中执行：

```bash
#!/bin/bash
# save as update.sh

echo "===== 开始更新 ====="

cd ~/期现交易策略汇报软件 || exit 1

echo "[1/3] 拉取最新代码..."
git pull origin main

echo "[2/3] 更新依赖..."
pip install -r requirements.txt --user

echo "[3/3] 重启应用..."
touch /var/www/www_yourdomain_com_wsgi.py

echo "===== 更新完成 ====="
```

然后只需运行：
```bash
bash update.sh
```

---

## 检查更新是否成功

### 1. 查看 Git 日志
```bash
git log --oneline -5
```

### 2. 检查文件是否更新
```bash
# 查看某个文件的修改时间
ls -la modules/basis_chart.py
```

### 3. 查看应用日志
在 PythonAnywhere 的 Web 标签页，点击 **Logs** 查看错误日志。

---

## 常见问题

### Q1: git pull 提示冲突
```bash
# 先保存本地修改（如果有）
git stash

# 拉取更新
git pull origin main

# 恢复本地修改（如果有）
git stash pop
```

### Q2: 更新后页面没有变化
- 清除浏览器缓存（Ctrl+F5 或 Cmd+Shift+R）
- 检查 PythonAnywhere 的 Web 应用是否已重启
- 查看 Error Log 是否有错误

### Q3: 依赖安装失败
```bash
# 使用 --user 参数安装
pip install -r requirements.txt --user

# 或更新 pip
pip install --upgrade pip --user
```

### Q4: 数据库结构变更
如果代码有数据库结构变更，需要登录 PythonAnywhere 执行：
```bash
cd ~/期现交易策略汇报软件
python -c "from db_manager import db_manager; db_manager.init_db()"
```

---

## 快速检查清单

更新前确认：
- [ ] 本地测试通过
- [ ] `requirements.txt` 已更新（如有新依赖）
- [ ] 数据库迁移脚本已准备（如有结构变更）

更新后确认：
- [ ] `git log` 显示最新提交
- [ ] Web 应用状态为 "Running"
- [ ] 网站功能正常
- [ ] 错误日志无异常
