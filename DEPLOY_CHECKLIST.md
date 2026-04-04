# ✅ 云端部署检查清单

按照以下步骤一步步操作，完成云端部署。

---

## □ 第一步：安装 Git（5分钟）

- [ ] 访问 https://git-scm.com/download/win
- [ ] 下载 Git 安装程序
- [ ] 运行安装程序，使用默认设置
- [ ] 打开新的 PowerShell，验证安装：
  ```bash
  git --version
  ```

---

## □ 第二步：配置 Git（3分钟）

- [ ] 设置用户名：
  ```bash
  git config --global user.name "你的GitHub用户名"
  ```
- [ ] 设置邮箱：
  ```bash
  git config --global user.email "你的GitHub注册邮箱"
  ```

---

## □ 第三步：创建 GitHub 仓库（5分钟）

- [ ] 访问 https://github.com/new
- [ ] Repository name: `strategy-report-app`
- [ ] 选择 Public 或 Private
- [ ] ✅ 勾选 "Add a README file"
- [ ] 点击 "Create repository"
- [ ] 复制仓库地址（如：`https://github.com/用户名/strategy-report-app.git`）

---

## □ 第四步：上传代码到 GitHub（5分钟）

- [ ] 在项目文件夹双击运行 `quick_deploy.bat`
- [ ] 或手动执行：
  ```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/用户名/strategy-report-app.git
  git branch -M main
  git push -u origin main
  ```
- [ ] 首次推送需要登录 GitHub（用户名 + Token）

---

## □ 第五步：创建 Supabase 数据库（10分钟）

- [ ] 访问 https://supabase.com
- [ ] 用 GitHub 账号登录
- [ ] 点击 "New Project"
- [ ] 填写信息：
  - **Project name**: `strategy-report-db`
  - **Database password**: 设置强密码（记下来！）
  - **Region**: Singapore 或 Tokyo
- [ ] 点击 "Create new project"
- [ ] 等待创建完成（约1-2分钟）

### 获取连接字符串

- [ ] 进入项目 → "Project Settings" → "Database"
- [ ] 找到 "Connection string" → URI 格式
- [ ] 复制并保存（将 `[YOUR-PASSWORD]` 替换为实际密码）

---

## □ 第六步：部署到 Render（15分钟）

### 注册和连接

- [ ] 访问 https://render.com
- [ ] 点击 "Get Started for Free"
- [ ] 选择 "Continue with GitHub"
- [ ] 授权 Render 访问你的仓库

### 创建 Web Service

- [ ] 点击 "New +" → "Web Service"
- [ ] 选择 `strategy-report-app` 仓库
- [ ] 配置：
  - **Name**: `strategy-report-app`
  - **Environment**: `Python 3`
  - **Region**: Singapore
  - **Build Command**: `pip install -r requirements.txt`
  - **Start Command**: `gunicorn app:app`

### 添加环境变量

- [ ] 点击 "Advanced" → "Add Environment Variable"
- [ ] 添加以下变量：
  
  | Key | Value |
  |-----|-------|
  | `DATABASE_URL` | `postgresql://postgres:密码@db.xxxxxxxx.supabase.co:5432/postgres` |
  | `SECRET_KEY` | 随机字符串（可用密码生成器生成） |

- [ ] 点击 "Create Web Service"

### 等待部署

- [ ] 查看构建日志（约3-5分钟）
- [ ] 部署成功后，会显示 URL
- [ ] 点击 URL 访问应用

---

## □ 第七步：验证部署（5分钟）

- [ ] 访问 Render 提供的 URL
- [ ] 确认页面正常加载
- [ ] 测试数据上传功能
- [ ] 测试 PDF 生成功能

---

## 🎉 部署完成！

现在你可以：
- ✅ 在任何地方通过 URL 访问应用
- ✅ 数据保存在云端 Supabase
- ✅ 本地修改代码后推送到 GitHub，云端自动更新

---

## 📝 日常使用

### 更新代码

```bash
# 修改代码后
git add .
git commit -m "描述修改内容"
git push origin main
# Render 会自动重新部署
```

### 查看日志

- 访问 Render Dashboard
- 点击你的服务
- 查看 "Logs" 标签页

---

## 🆘 遇到问题？

| 问题 | 解决方案 |
|------|---------|
| Git 推送失败 | 检查网络、确认仓库地址正确、使用 Token 代替密码 |
| 部署失败 | 查看 Render 日志、检查 requirements.txt |
| 数据库连接失败 | 检查 DATABASE_URL 格式、确认密码正确 |
| 页面无法访问 | 确认服务状态为 "Live"、查看日志排查错误 |

---

**详细教程请查看**：[DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)
