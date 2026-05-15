# Web文件下载上传系统 📁

[![Flask](https://img.shields.io/badge/Flask-2.3.2-blue)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-green)](https://www.sqlalchemy.org/)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

一个基于Flask框架的轻量级文件管理系统。支持用户注册、登录、文件上传/下载/删除，以及完整的管理员后台管理功能。

> 📝 **作者声明**：本项目为初学者学习作品，代码可能存在改进空间。如有任何问题或改进建议，**欢迎提出批评和指正**！

## 🌟 主要特性

### 👤 用户管理
- ✅ 用户注册与登录（支持用户名或邮箱登录）
- ✅ 密码加密存储（Werkzeug bcrypt）
- ✅ 会话管理（支持30天持久化登录）
- ✅ **第一个注册用户自动为管理员**

### 📦 文件管理
- ✅ 文件上传（仅支持`.7z`和`.zip`压缩包）
- ✅ 文件下载（已登录用户可下载自己的文件）
- ✅ 文件删除（删除的文件自动移至回收站）
- ✅ 文件列表展示

### 🛡️ 管理员功能
- ✅ **用户管理**：查看、搜索、删除用户
- ✅ **回收站管理**：查看、恢复、永久删除回收站文件
- ✅ **系统管理**：清空所有用户数据

### 🔒 安全特性
- 🔐 密码加密存储
- 🔐 路径穿越防护
- 🔐 Session加密保护
- 🔐 管理员权限验证

## 🚀 快速开始

### 前置要求
- Python 3.7+
- pip

### 安装步骤

#### 1️⃣ 克隆项目
```bash
git clone <repository-url>
cd web_download_upload
```

#### 2️⃣ 创建虚拟环境（推荐）
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

#### 3️⃣ 安装依赖
```bash
pip install -r requirements.txt
```

#### 4️⃣ 初始化数据库
```bash
python init_db.py
```

✅ 完成！项目已准备好运行

#### 5️⃣ 运行应用
```bash
python app.py
```

打开浏览器访问：`http://localhost:5000`

---

## 📖 使用指南

### 首次使用

1. **访问首页** → 点击"注册"
2. **创建账号** → 第一个注册的用户自动成为管理员！
3. **上传文件** → 选择`.7z`或`.zip`文件上传
4. **管理文件** → 在主页查看、下载或删除文件

### 管理员功能

登录管理员账号后，可访问以下功能：

| 功能 | URL | 说明 |
|------|-----|------|
| 管理员首页 | `/admin` | 查看用户总数 |
| 用户管理 | `/admin_user` | 查看、搜索、删除用户 |
| 回收站管理 | `/admin/trash` | 查看回收站文件、恢复或永久删除 |

## 📁 项目结构

```
web_download_upload/
├── app.py                    # 主应用程序
├── config.py                 # 配置文件
├── init_db.py                # 数据库初始化脚本
├── requirements.txt          # 项目依赖
├── .gitignore               # Git忽略文件
├── README.md                # 项目说明
├── templates/               # HTML模板
│   ├── index.html          # 首页
│   ├── login.html          # 登录页
│   ├── add.html            # 注册页
│   ├── home.html           # 用户主页
│   ├── upload.html         # 上传页
│   ├── admin.html          # 管理员后台
│   └── nav.html            # 导航栏
├── uploads/                # 用户上传文件目录（自动创建）
├── delete/                 # 回收站目录（自动创建）
└── app.db                  # SQLite数据库（首次运行时创建）
```

## 💾 数据库模型

### User 表

| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 用户ID（主键） |
| username | String(50) | 用户名 |
| password | String(200) | 密码哈希值 |
| email | String(50) | 邮箱 |
| is_admin | Boolean | 是否为管理员（第一个用户自动为True） |
| remove_number | String(50) | 删除计数（生成回收站文件名） |

## 🔧 技术栈

| 技术 | 用途 |
|------|------|
| **Flask** | Web框架 |
| **SQLAlchemy** | ORM数据库操作 |
| **SQLite** | 数据库（开箱即用） |
| **Werkzeug** | 密码加密、HTTP工具 |
| **Flask-SQLAlchemy** | Flask数据库集成 |
| **Flask-Migrate** | 数据库迁移管理 |

## 🎓 学习资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Werkzeug安全模块](https://werkzeug.palletsprojects.com/security/)

## 📋 配置说明

### config.py

```python
# 数据库配置 - 默认使用SQLite
SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

# 文件上传目录
UPLOAD_FOLDER = 'uploads'

# 回收站目录
DELETE_FOLDER = 'delete'

# Secret Key（用于会话加密）
SECRET_KEY = "8vbj289skc8"
```

**切换到MySQL数据库**（可选）：
```python
# 在config.py中修改
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://user:password@localhost/database_name'
```

## ✨ 功能演示

### 用户流程
1. 注册账号 → 第一个用户自动为管理员
2. 登录系统
3. 上传`.zip`或`.7z`文件
4. 查看、下载、删除文件

### 管理员流程
1. 以管理员身份登录
2. 访问`/admin`进入管理后台
3. 管理用户、查看回收站
4. 恢复或永久删除文件

## 🐛 已知限制

- 仅支持`.7z`和`.zip`文件格式
- 无文件大小限制
- 缺少详细错误日志
- 前端验证不完整

## 🔄 改进方向

- [ ] 添加更多文件格式支持
- [ ] 实现文件大小限制
- [ ] 添加文件搜索功能
- [ ] 完善错误处理和日志
- [ ] 添加密码重置功能
- [ ] 实现文件分享链接
- [ ] 前后端参数验证加强
- [ ] 添加CSRF防护

## ❓ 常见问题

**Q: 数据库文件在哪里？**  
A: 运行 `init_db.py` 后，在项目根目录生成 `app.db` SQLite数据库。

**Q: 如何切换到MySQL？**  
A: 修改 `config.py` 中的 `SQLALCHEMY_DATABASE_URI` 并安装 `mysqlclient`。

**Q: 如何重置管理员？**  
A: 删除 `app.db` 后重新运行 `init_db.py`，重新注册账号即可。

**Q: 上传文件失败？**  
A: 确保上传的是 `.7z` 或 `.zip` 格式的压缩包。

**Q: 删除的文件在哪里？**  
A: 在 `delete/` 目录中，带有版本号前缀。管理员可在回收站恢复。

## 📝 许可证

MIT License

## 🙏 致谢

感谢所有关注和提出建议的开发者！

---

**💬 反馈与建议**

如果您发现任何bug或有改进建议，欢迎通过以下方式反馈：
- 提交Issue
- 提交Pull Request
- 发送邮件反馈

**因为这是初学者作品，您的批评和指正将帮助我不断进步！** 🙏

