import os

# 数据库配置 - 默认使用SQLite（本地开发），可修改为MySQL
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' 或 'mysql'

if DB_TYPE == 'mysql':
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:root@127.0.0.1:3306/database_learn?charset=utf8mb4'
else:
    # SQLite配置 - 支持开箱即用
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = 'uploads'
DELETE_FOLDER = 'delete'
SECRET_KEY = "8vbj289skc8"