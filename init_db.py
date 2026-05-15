"""
数据库初始化脚本
首次运行应用前执行此脚本，自动创建数据库和所有表
"""

import os
import sys
from app import app, db

def init_database():
    """初始化数据库"""
    with app.app_context():
        # 检查是否已存在数据库
        db_path = 'app.db'
        is_new_db = not os.path.exists(db_path)
        
        print("🔄 正在初始化数据库...")
        
        # 创建所有表
        db.create_all()
        
        if is_new_db:
            print(f"✅ 数据库创建成功: {db_path}")
        else:
            print("✅ 数据库已存在，表结构已检查")
        
        # 创建必要的目录
        for folder in ['uploads', 'delete']:
            os.makedirs(folder, exist_ok=True)
            print(f"✅ 目录创建/检查完成: {folder}")
        
        print("\n🎉 数据库初始化完成！")
        print("📝 提示：第一个注册的用户将自动成为管理员")
        print("🚀 现在可以运行: python app.py")

if __name__ == '__main__':
    init_database()
