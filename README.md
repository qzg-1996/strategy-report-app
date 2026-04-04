# 📊 期现交易策略汇报软件

一款专业的期现交易策略汇报生成工具，支持基差走势图生成、策略盈亏计算和 PDF 报告导出。

## ✨ 功能特性

- 📈 **基差走势图** - 自动生成策略相关的基差走势图表
- 📊 **策略管理** - 管理套期保值、基差交易、趋势交易等策略
- 💰 **盈亏计算** - 自动计算持仓盈亏和平仓盈亏
- 📄 **PDF 报告** - 生成专业的策略执行周报 PDF
- ☁️ **云端部署** - 支持部署到云端，随时随地访问

## 🚀 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 运行应用
python app.py

# 打开浏览器访问 http://localhost:5000
```

### 云端部署

#### 方式一：使用快速部署脚本（推荐）

1. 安装 Git：https://git-scm.com/download/win
2. 在 GitHub 创建仓库：https://github.com/new
3. 双击运行 `quick_deploy.bat`

#### 方式二：手动部署

详细步骤请查看 [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md)

**部署架构：**
- **GitHub** - 代码托管
- **Render** - 免费云服务器
- **Supabase** - 云端 PostgreSQL 数据库

## 📁 项目结构

```
.
├── app.py                      # 主应用入口
├── config.py                   # 配置文件
├── db_manager.py               # 数据库管理器（支持 SQLite/PostgreSQL）
├── requirements.txt            # Python 依赖
├── modules/                    # 功能模块
│   ├── basis_chart_generator.py   # 基差走势图生成
│   ├── data_processor.py          # 数据处理器
│   ├── report_generator.py        # PDF 报告生成
│   └── strategy_manager.py        # 策略管理
├── templates/                  # HTML 模板
├── static/                     # 静态资源
├── render.yaml                 # Render 部署配置
├── Procfile                    # 进程配置文件
└── DEPLOY_GUIDE.md             # 详细部署指南
```

## 🛠️ 技术栈

- **后端**: Python + Flask
- **数据库**: SQLite (本地) / PostgreSQL (云端)
- **前端**: Bootstrap 5 + JavaScript
- **图表**: Matplotlib
- **PDF**: ReportLab
- **部署**: Render + Supabase

## 🔧 环境变量

创建 `.env` 文件（本地开发）：

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///strategy.db
```

云端部署时，在 Render 平台设置：

```env
SECRET_KEY=随机字符串（用于加密会话）
DATABASE_URL=postgresql://postgres:密码@db.xxxxxxxx.supabase.co:5432/postgres
```

## 📝 更新日志

### v1.0.0
- ✨ 支持云端部署
- ✨ 支持 Supabase PostgreSQL 数据库
- ✨ 代码与数据分离，支持多端同步

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**有问题？** 查看 [DEPLOY_GUIDE.md](DEPLOY_GUIDE.md) 获取详细的部署教程。
