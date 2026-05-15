# Web文件下载上传系统

一个基于Flask框架的文件管理系统，支持用户注册、登录、文件上传/下载/删除等功能，并提供管理员后台管理界面。

> **作者声明**：本项目为初学者学习作品，如有任何问题或改进建议，欢迎指出！

## 项目简介

这是一个小型Web应用，主要用于学习Flask框架、SQLAlchemy ORM、用户认证、文件操作等核心Web开发技术。系统提供了完整的用户管理和文件存储功能，并采用了一些基础安全措施（如路径穿越防护）。

## 主要功能

### 用户管理
- ✅ **用户注册**：新用户可创建账号（支持邮箱、用户名、密码）
- ✅ **用户登录**：支持用户名或邮箱登录，提供记住登录状态功能
- ✅ **会话管理**：使用Flask会话机制管理用户登录状态，支持30天持久化登录

### 文件管理
- ✅ **文件上传**：支持上传`.7z`和`.zip`格式的压缩包
- ✅ **文件下载**：已登录用户可下载自己上传的文件
- ✅ **文件删除**：用户可删除自己的文件，删除的文件移至回收站（带版本号）
- ✅ **文件列表**：主页显示当前用户的所有文件

### 后台管理
- ✅ **管理员面板**：仅管理员可访问
- ✅ **用户管理**：查看所有用户、搜索用户、删除用户
- ✅ **系统管理**：清空所有用户数据库功能

### 安全特性
- 🔒 **密码加密**：使用Werkzeug的`generate_password_hash`加密存储密码
- 🔒 **路径穿越防护**：验证文件访问路径，防止恶意访问
- 🔒 **会话保护**：Cookie加密，防止会话伪造
- 🔒 **权限控制**：装饰器验证管理员身份

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Flask** | - | Web框架 |
| **Flask-SQLAlchemy** | - | ORM数据库操作 |
| **Flask-Migrate** | - | 数据库迁移管理 |
| **SQLAlchemy** | - | Python ORM框架 |
| **Werkzeug** | - | 密码加密、HTTP工具 |
| **MySQL/mysqldb** | - | 数据库 |

## 项目结构

```
web_download_upload/
├── app.py                 # 主应用程序
├── config.py              # 配置文件（数据库、密钥等）
├── templates/             # HTML模板目录
│   ├── index.html        # 首页
│   ├── login.html        # 登录页
│   ├── add.html          # 注册页
│   ├── home.html         # 用户主页（文件列表）
│   ├── upload.html       # 文件上传页
│   ├── admin.html        # 管理员后台
│   └── nav.html          # 导航栏模板
├── uploads/              # 文件存储目录
├── delete/               # 回收站目录
└── README.md             # 项目说明文档
```

## 数据库模型

### User表
| 字段 | 类型 | 说明 |
|------|------|------|
| id | Integer | 用户ID（主键） |
| username | String(50) | 用户名（必填） |
| password | String(200) | 密码哈希值（必填） |
| email | String(50) | 邮箱（可选） |
| is_admin | Boolean | 是否为管理员（默认False） |
| remove_number | String(50) | 删除计数（用于生成唯一回收站文件名） |

## 快速开始

### 前置要求
- Python 3.7+
- MySQL数据库
- pip包管理器

### 安装步骤

1. **克隆或下载项目**
```bash
cd web_download_upload
```

2. **安装依赖**
```bash
pip install flask flask-sqlalchemy flask-migrate flask-cors
pip install mysqlclient
```

3. **配置数据库**

编辑 `config.py` 文件，修改数据库连接信息：
```python
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://用户名:密码@主机:端口/数据库名?charset=utf8mb4'
```

4. **初始化数据库**
```bash
flask db init      # 第一次初始化迁移环境
flask db migrate   # 生成迁移脚本
flask db upgrade   # 执行迁移，创建表
```

5. **创建上传目录**
```bash
# 项目会自动创建uploads目录，但如有需要可手动创建
mkdir uploads
mkdir delete
```

6. **运行应用**
```bash
python app.py
```

应用将在 `http://localhost:5000` 运行

## 使用说明

### 普通用户
1. **注册账号**：访问注册页面创建新账号
2. **登录**：用用户名或邮箱登录
3. **上传文件**：仅支持`.7z`和`.zip`格式压缩包
4. **管理文件**：在主页查看、下载或删除文件
5. **注销登出**：点击登出按钮清除会话

### 管理员
1. 登录管理员账号
2. 访问 `/admin` 进入管理后台
3. 查看用户统计、搜索用户、删除用户等

## 关键代码说明

### 密码安全
```python
def set_password(self, password):
    self.password = generate_password_hash(password)

def check_password(self, password):
    return check_password_hash(str(self.password), password)
```

### 路径穿越防护
```python
safe_path = os.path.abspath(target_dir)
file_path = os.path.abspath(os.path.join(target_dir, filename))
if not file_path.startswith(safe_path):
    abort(403)  # 拒绝非法访问
```

### 管理员权限装饰器
```python
@admin_required
def admin_user():
    # 仅管理员可访问
    pass
```

## 已知限制与改进方向

### 当前限制
- 🔴 仅支持`.7z`和`.zip`格式文件
- 🔴 没有实现文件大小限制
- 🔴 缺少详细的错误日志记录
- 🔴 前端验证不完整
- 🔴 没有实现邮件通知功能

### 建议改进
- [ ] 添加文件大小和上传进度限制
- [ ] 实现文件预览功能
- [ ] 添加用户分享链接功能
- [ ] 完善错误处理和日志系统
- [ ] 添加密码重置功能
- [ ] 实现文件搜索功能
- [ ] 添加操作审计日志
- [ ] 前后端参数验证加强
- [ ] 实现CSRF防护
- [ ] 添加邮件验证

## 常见问题

### Q: 数据库连接失败怎么办？
**A**: 检查 `config.py` 中的数据库配置是否正确，确保MySQL服务正在运行。

### Q: 上传文件时提示"仅允许上传压缩包"？
**A**: 当前仅支持`.7z`和`.zip`格式，请使用这两种格式的文件。

### Q: 如何成为管理员？
**A**: 在数据库中直接修改用户的 `is_admin` 字段为 `True`。

### Q: 删除的文件可以恢复吗？
**A**: 可以，删除的文件在 `delete/` 目录中保留，带有版本号后缀。

## 学习资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy文档](https://flask-sqlalchemy.palletsprojects.com/)
- [Werkzeug密码哈希](https://werkzeug.palletsprojects.com/security/#password-hashing)

## 许可证

本项目仅供学习使用。

## 联系方式

如有任何问题、建议或发现bug，欢迎反馈！

---

**最后说明**：这是一个初学者作品，代码可能存在改进空间。如果发现任何问题或有优化建议，**强烈欢迎提出批评和指正**！感谢！🙏
