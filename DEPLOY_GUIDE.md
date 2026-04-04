# 🚀 云端部署完整指南

## 整体架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   你的电脑   │────▶│   GitHub    │────▶│   Render    │
│  (开发更新)  │     │  (代码托管)  │     │ (免费云服务器)│
└─────────────┘     └─────────────┘     └──────┬──────┘
                                                │
                                       ┌────────┴────────┐
                                       │   Supabase      │
                                       │ (云端PostgreSQL) │
                                       │   + 文件存储    │
                                       └─────────────────┘
```

---

## 第一步：安装 Git

### Windows 用户

1. **下载 Git**
   - 访问：https://git-scm.com/download/win
   - 或国内镜像：https://registry.npmmirror.com/binary.html?path=git-for-windows/
   - 下载 `Git-2.42.0-64-bit.exe`

2. **安装**
   - 双击运行安装程序
   - 一路点击 "Next"（使用默认设置即可）
   - 安装完成后，重新打开 PowerShell 或 CMD

3. **验证安装**
   ```bash
   git --version
   ```
   应该显示：`git version 2.42.0.windows.2` 或类似版本

4. **配置 Git 用户信息**
   ```bash
   git config --global user.name "你的GitHub用户名"
   git config --global user.email "你的GitHub注册邮箱"
   ```

---

## 第二步：创建 GitHub 仓库

1. **登录 GitHub**
   - 访问：https://github.com
   - 使用你注册的账号登录

2. **创建新仓库**
   - 点击右上角 "+" → "New repository"
   - 填写信息：
     - **Repository name**: `strategy-report-app`（或你喜欢的名字）
     - **Description**: 期现交易策略汇报软件
     - 选择 **Public**（公开）或 **Private**（私有）
     - ✅ 勾选 "Add a README file"
   - 点击 **Create repository**

3. **获取仓库地址**
   - 创建完成后，点击绿色的 "<> Code" 按钮
   - 复制 HTTPS 地址，如：`https://github.com/你的用户名/strategy-report-app.git`

---

## 第三步：上传代码到 GitHub

### 方法 A：使用脚本（推荐）

1. 在项目文件夹中，双击运行 `setup_git.bat`
2. 运行完成后，双击运行 `upload_to_github.bat`
3. 按提示输入 GitHub 仓库地址

### 方法 B：手动命令

在项目文件夹（`期现交易策略汇报软件`）中打开 PowerShell，执行：

```bash
# 初始化本地仓库
git init

# 添加所有文件
git add .

# 提交代码
git commit -m "Initial commit: 期现交易策略汇报软件"

# 关联远程仓库（替换为你的GitHub仓库地址）
git remote add origin https://github.com/你的用户名/strategy-report-app.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

**首次推送需要登录 GitHub**：
- 会弹出窗口让你登录 GitHub
- 或者需要输入用户名和个人访问令牌（Token）

---

## 第四步：配置 Supabase 数据库

### 4.1 创建 Supabase 项目

1. 访问：https://supabase.com
2. 使用 GitHub 账号登录
3. 点击 "New Project"
4. 填写信息：
   - **Organization**: 选择或创建一个组织
   - **Project Name**: `strategy-report-db`
   - **Database Password**: 设置一个强密码（记下来！）
   - **Region**: 选择 `East Asia (Singapore)` 或 `Northeast Asia (Tokyo)`（离中国近）
5. 点击 "Create new project"
6. 等待项目创建完成（约1-2分钟）

### 4.2 获取数据库连接信息

1. 进入项目后，点击左侧菜单 "Project Settings"
2. 点击 "Database"
3. 找到 "Connection string" 部分
4. 复制 URI 格式的连接字符串，如：
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxx.supabase.co:5432/postgres
   ```
5. 将 `[YOUR-PASSWORD]` 替换为你设置的密码

### 4.3 测试本地连接（可选）

```bash
# 安装 PostgreSQL 客户端（如果还没安装）
pip install psycopg2-binary

# 测试连接（用实际参数替换）
python -c "import psycopg2; conn = psycopg2.connect('postgresql://postgres:密码@db.xxxxxxxx.supabase.co:5432/postgres'); print('连接成功'); conn.close()"
```

---

## 第五步：部署到 Render（免费云服务器）

### 5.1 注册 Render 账号

1. 访问：https://render.com
2. 点击 "Get Started for Free"
3. 选择 "Continue with GitHub"
4. 授权 Render 访问你的 GitHub 仓库

### 5.2 创建 Web 服务

1. 登录后，点击 "New +" → "Web Service"
2. 在列表中找到并选择 `strategy-report-app` 仓库
3. 配置服务：
   - **Name**: `strategy-report-app`
   - **Environment**: `Python 3`
   - **Region**: `Singapore` 或 `Oregon`
   - **Branch**: `main`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. 点击 "Advanced" 展开高级设置
5. 添加环境变量：
   - 点击 "Add Environment Variable"
   - **Key**: `DATABASE_URL`
   - **Value**: `postgresql://postgres:你的密码@db.xxxxxxxx.supabase.co:5432/postgres`（Supabase的连接字符串）
   - 再添加一个：
   - **Key**: `SECRET_KEY`
   - **Value**: 随机字符串（可以在线生成器生成一个64位随机字符串）
6. 点击 "Create Web Service"

### 5.3 等待部署完成

- Render 会自动构建和部署你的应用
- 大概需要 3-5 分钟
- 部署完成后，会显示一个 URL，如：`https://strategy-report-app.onrender.com`

### 5.4 访问你的云端应用

1. 点击 Render 提供的 URL
2. 第一次访问可能会稍慢（免费服务会休眠）
3. 登录后，数据会自动保存到 Supabase 云端数据库

---

## 第六步：日常使用流程

### 本地开发更新

1. **修改代码**后，在项目文件夹执行：
   ```bash
   # 查看修改的文件
   git status
   
   # 添加修改的文件
   git add .
   
   # 提交修改
   git commit -m "描述这次修改的内容"
   
   # 推送到 GitHub
   git push origin main
   ```

2. **Render 会自动检测 GitHub 更新并重新部署**

### 云端数据备份

Supabase 数据库会自动备份。你也可以手动导出：

1. 登录 Supabase 控制台
2. 点击 "Database" → "Backups"
3. 点击 "Download" 下载备份

---

## 常见问题

### Q1: Git 推送失败，提示权限不足？

**解决**：
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成 Token 并复制
5. 推送时，用户名输入你的 GitHub 用户名，密码输入刚才的 Token

### Q2: Render 部署失败？

**检查**：
1. 查看 Render 的日志（Logs 标签页）
2. 确认 `requirements.txt` 包含所有依赖
3. 确认环境变量 `DATABASE_URL` 设置正确

### Q3: 数据库连接失败？

**检查**：
1. 确认 Supabase 项目已创建完成
2. 确认连接字符串中的密码正确
3. 确认 Render 所在地区能访问 Supabase

### Q4: 上传的文件在云端丢失？

**原因**：Render 的免费服务有临时文件系统，重启后会清空。

**解决**：使用 Supabase Storage 存储文件（后续可升级支持）

---

## 费用说明

| 服务 | 免费额度 | 说明 |
|------|---------|------|
| **GitHub** | 无限 | 代码托管 |
| **Supabase** | 500MB 数据库 + 1GB 存储 | 足够个人/小团队使用 |
| **Render** | 750小时/月 | 免费服务会在15分钟无访问后休眠 |

---

## 下一步优化（可选）

1. **自定义域名**：在 Render 中添加自己的域名
2. **CDN 加速**：使用 Cloudflare 加速访问
3. **文件存储**：将上传的文件保存到 Supabase Storage
4. **自动备份**：设置定时备份策略

---

## 需要帮助？

- GitHub 文档：https://docs.github.com/zh
- Supabase 文档：https://supabase.com/docs
- Render 文档：https://render.com/docs
