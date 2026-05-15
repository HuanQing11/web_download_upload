import os
import shutil
from functools import wraps
from flask import Flask, render_template, request, redirect, session, abort, send_from_directory
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Integer, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

import config

"""
Flask-SQLAlchemy	Flask 专用 ORM 扩展，简化数据库操作	核心：将 Python 类映射到数据库表，提供优雅的 CRUD 接口
SQLAlchemy	Python 生态最强 ORM 框架，底层支持	基石：提供数据库抽象层，支持 MySQL/PostgreSQL/SQLite 等，是 Flask-SQLAlchemy 的底层依赖
Flask-Migrate	数据库版本管理工具	辅助 封装 Alembic 实现数据库结构变更的自动化与版本控制
Alembic	独立的数据库迁移工具	引擎 Flask-Migrate 的底层，负责生成迁移脚本、执行升级/回滚
mysqlclient	MySQL 官方驱动 C 扩展 	驱动：高性能连接 MySQL 是 Django 默认驱动，也兼容 SQLAlchemy
"""

"""
数据库操作指令
flask db init
flask db migrate
flask db upgrade
"""




app = Flask(__name__)
app.config.from_object(config)
class Base(DeclarativeBase):
    meta = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": 'ck_%(table_name)s_%(column_0_name)s',
        "fk": 'fk_%(table_name)s_%(column_0_name)s',
        "pk": 'pk_%(table_name)s',
    })
db = SQLAlchemy(app=app,model_class=Base)
migrate = Migrate(app=app,db=db)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config.get('DELETE_FOLDER', 'delete'), exist_ok=True)

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(Integer, primary_key=True,autoincrement=True)
    username: Mapped[str] = mapped_column(db.String(50), nullable=False)
    password: Mapped[str] = mapped_column(db.String(200), nullable=False)
    email: Mapped[str] = mapped_column(db.String(50), nullable=True)
    is_admin: Mapped[bool] = mapped_column(db.Boolean, default=False)
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(str(self.password),password)
    remove_number:Mapped[int] = mapped_column(db.String(50), nullable=True)



@app.route('/')
def index():
    # 对外宣传首页
    return render_template('index.html')

@app.route('/home')
def home():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    if request.method == 'GET':
        if db.session.scalar(db.select(User).where(User.id == user_id)) is None:
            return redirect('/logout')
    user_id = session.get('user_id')
    user = db.session.scalar(db.select(User).where(User.id == user_id))
    upload_folder = app.config['UPLOAD_FOLDER']
    user_folder = os.path.join(upload_folder, f'{user_id}_{user.username}')
    files=[]
    if os.path.exists(user_folder):
        for filename in os.listdir(user_folder):
            files.append({
                'name': filename,
                'username': user.username,
            })
    return render_template('home.html',files=files)



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        if username:
            user = db.session.scalar(db.select(User).where(User.username == username))
        else:
            user = db.session.scalar(db.select(User).where(User.email == email))
        if user and user.check_password(password):
            session['user_id'] = user.id
            #设置True会在31天后过期
            if remember:
                session.permanent = True
            return redirect('/home')
        else:
            tips='邮箱或者密码错误'
            print('邮箱或者密码错误')
            return redirect(f'/login?tips={tips}')





#注册
def user_find(find_username, find_email):
    find_email = db.session.scalar(db.select(User).where(User.email == find_email))
    find_username = db.session.scalar(db.select(User).where(User.username == find_username))
    if find_username is None and find_email is None:
        return True
    elif find_username is not None:
        return '用户名已被占用'
    elif find_email is not None:
        return '邮箱已被占用'
    else:
        return None

def is_first_user():
    """检查是否为首个用户"""
    count = db.session.query(User).count()
    return count == 0

@app.route('/register', methods=['GET',"POST"])
def register():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        tips = user_find(username, email)
        if tips is True:
            user = User(username=username, email=email)
            user.set_password(password)
            # 第一个注册的用户自动成为管理员
            if is_first_user():
                user.is_admin = True
                admin_tip = '（已设置为管理员）'
            else:
                admin_tip = ''
            db.session.add(user)
            db.session.commit()
            tips=f'注册成功{admin_tip}'
            return redirect(f'/login?tips={tips}')
        else:
            return render_template('add.html', tips=tips,email=email,username=username,password=password,)










#下载接口
@app.route('/download/<username>/<filename>')
def download(username,filename):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    if db.session.scalar(db.select(User).where(User.id == user_id))  is None:
        return redirect('/logout')
    target_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_{username}')

    #安全路径校验（防止路径穿越攻击）
    safe_path = os.path.abspath(target_dir)
    file_path = os.path.abspath(os.path.join(target_dir, filename))
    if not file_path.startswith(safe_path):
        abort(403)  # 非法访问，直接拒绝


    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(target_dir, filename, as_attachment=True)
    return "文件不存在", 404



#上传文件
def get_file_extension(file_path):
    return os.path.splitext(file_path)[1].lower()
@app.route('/upload',methods=['POST','GET'])
def upload():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.scalar(db.select(User).where(User.id == user_id))
    if request.method == 'GET':
        if user is None:
            return redirect('/logout')
        return render_template('upload.html')
    else:
        if user is None:
            return redirect('/logout')
        file = request.files['file']
        if get_file_extension(file.filename) not in ['.7z','.zip']:
            return render_template('upload.html',tips = '仅允许上传压缩包')
        else:
            user_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'{user.id}_{user.username}')
            os.makedirs(user_dir, exist_ok=True)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'],f'{user.id}_{user.username}',file.filename)
            if os.path.exists(save_path):
                return render_template('upload.html', tips=f'文件 {file.filename} 已存在，请勿重复上传！')
            file.save(str(save_path))
            return render_template('upload.html',tips=f'文件\'{file.filename}\'上传成功')


#查询删除文件数量,防止文件名重复
def remove_number(username):
    user = db.session.scalar(db.select(User).where(User.username == username))
    number = user.remove_number
    if number is None:
        number = int(1)
        user.remove_number = number
        db.session.add(user)
        db.session.commit()
        return number
    number =  int(number)
    number += 1
    user.remove_number = number
    db.session.add(user)
    db.session.commit()
    return number
#删除文件
@app.route('/delete_file/<username>/<filename>')
def delete_file(username,filename):
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    user = db.session.scalar(db.select(User).where(User.id == user_id))
    if user is None:
        return redirect('/logout')
    if user.username != username:
        return redirect('/logout')
    target_dir = os.path.join(app.config['UPLOAD_FOLDER'], f'{user_id}_{username}')
    #安全路径校验（防止路径穿越攻击）
    safe_path = os.path.abspath(target_dir)# 1. 把目标文件夹转成 绝对路径（安全基准目录）
    file_path = os.path.abspath(os.path.join(target_dir, filename))# 2. 把文件名和目标目录拼接，再转成绝对路径
    if not file_path.startswith(safe_path):# 3. 检查最终文件路径 是否以安全目录开头   如果不是直接拒绝访问（403 禁止）
        abort(403)  # 非法访问，直接拒绝
    #如果安全则创建用户删除文件夹,文件加上编号移动到回收站,加编号防止文件重复
    if os.path.exists(file_path) and os.path.isfile(file_path):
        user_dir = os.path.join('delete', f'{user_id}_{username}')
        os.makedirs(user_dir, exist_ok=True)
        file_move = os.path.abspath(user_dir)
        lisr_number = remove_number(username)
        file_move_end = os.path.join(file_move, f'{lisr_number}_{filename}')
        if os.listdir(file_move):
            os.rename(file_path, file_move_end)
        else:
            os.makedirs(user_dir, exist_ok=True)
            os.rename(file_path, file_move_end)


        # os.remove(file_path)
        return redirect(f'/home')

    return "文件不存在", 404



#后台管理
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. 判断是否登录
        user_id = session.get('user_id')
        if not user_id:
            return redirect('/login')
        # 2. 查询用户是否是管理员
        user = db.session.get(User, user_id)
        if not user or not user.is_admin:
        # 不是管理员禁止访问（403无权限）
            abort(404)
        return f(*args, **kwargs)
    return decorated_function
@app.route('/admin')
def admin():
    with app.app_context():
        count = User.query.count()
        return render_template('admin.html',count=count)


@app.route('/admin_user')
@admin_required
def admin_user():
    users = db.session.scalars(db.select(User))
    return render_template('admin.html',users=users)
@app.route('/admin/delete_all')
@admin_required
def delete_all():
    with app.app_context():
        db.session.query(User).delete()
        db.session.execute(text('TRUNCATE TABLE user'))
        db.session.commit()
        return redirect('/')

@app.route('/admin/delete_user', methods=['POST'])
@admin_required
def delete_user():
    user = db.session.scalar(db.select(User).where(User.id == request.form.get('delete_user')))
    db.session.delete(user)
    db.session.commit()
    return redirect('/admin')



# ========== 回收站管理 ==========

@app.route('/admin/trash')
@admin_required
def admin_trash():
    """管理员查看回收站"""
    trash_items = []
    delete_folder = app.config.get('DELETE_FOLDER', 'delete')
    
    if os.path.exists(delete_folder):
        for user_folder in os.listdir(delete_folder):
            user_path = os.path.join(delete_folder, user_folder)
            if os.path.isdir(user_path):
                for filename in os.listdir(user_path):
                    file_path = os.path.join(user_path, filename)
                    if os.path.isfile(file_path):
                        trash_items.append({
                            'user_folder': user_folder,
                            'filename': filename,
                            'delete_time': os.path.getmtime(file_path),
                            'file_size': os.path.getsize(file_path)
                        })
    
    return render_template('admin.html', trash_items=trash_items)


@app.route('/admin/trash/restore', methods=['POST'])
@admin_required
def admin_restore_file():
    """管理员恢复回收站文件"""
    user_folder = request.form.get('user_folder')
    filename = request.form.get('filename')
    
    if not user_folder or not filename:
        return redirect('/admin/trash')
    
    delete_folder = app.config.get('DELETE_FOLDER', 'delete')
    trash_path = os.path.join(delete_folder, user_folder, filename)
    
    # 安全检查
    safe_path = os.path.abspath(delete_folder)
    trash_file = os.path.abspath(trash_path)
    if not trash_file.startswith(safe_path):
        abort(403)
    
    if os.path.exists(trash_file) and os.path.isfile(trash_file):
        # 提取原始文件名（移除开头的编号）
        original_filename = '_'.join(filename.split('_')[1:]) if '_' in filename else filename
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], user_folder, original_filename)
        
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        os.rename(trash_file, upload_path)
    
    return redirect('/admin/trash')


@app.route('/admin/trash/delete', methods=['POST'])
@admin_required
def admin_delete_trash():
    """管理员永久删除回收站文件"""
    user_folder = request.form.get('user_folder')
    filename = request.form.get('filename')
    
    if not user_folder or not filename:
        return redirect('/admin/trash')
    
    delete_folder = app.config.get('DELETE_FOLDER', 'delete')
    trash_path = os.path.join(delete_folder, user_folder, filename)
    
    # 安全检查
    safe_path = os.path.abspath(delete_folder)
    trash_file = os.path.abspath(trash_path)
    if not trash_file.startswith(safe_path):
        abort(403)
    
    if os.path.exists(trash_file) and os.path.isfile(trash_file):
        os.remove(trash_file)
    
    return redirect('/admin/trash')


@app.route('/admin/trash/clear', methods=['POST'])
@admin_required
def admin_clear_trash():
    """管理员清空所有回收站"""
    delete_folder = app.config.get('DELETE_FOLDER', 'delete')
    
    if os.path.exists(delete_folder):
        shutil.rmtree(delete_folder)
        os.makedirs(delete_folder, exist_ok=True)
    
    return redirect('/admin/trash')


@app.route('/admin/find')
@admin_required
def find():
    find_username = request.args.get('find_username')
    db_find = db.session.scalar(db.select(User).where(User.username == find_username))
    users = User.query.all()
    if db_find is not None:
        user_id = db_find.id

        user_email = db_find.email
        tips = f'''查询成功!\nid为:{user_id}\n用户名:{find_username}\n邮箱为:{user_email}'''
        return render_template('admin.html', tips=tips,users=users)
    else:
        tips = '此用户名无效'
        return render_template('admin.html', tips=tips,users=users)













if __name__ == '__main__':
    app.run()

