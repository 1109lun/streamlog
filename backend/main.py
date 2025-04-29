from flask import Flask, render_template, request, redirect, url_for, session
from db.db import db, cursor  # 直接從 db 引入 db 跟 cursor

# Flask app 設定
app = Flask(__name__)
app.secret_key = 'streamlogeight' # ⚡️一定要設，Flask session 需要

# 首頁：如果登入了顯示首頁，否則跳去登入頁
@app.route('/')
def home():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))

# 登入頁：GET 顯示表單，POST 檢查帳密
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and password == user['password']:  # 先簡單比對（之後可以加密）
            session['username'] = user['user_name']
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error="帳號或密碼錯誤")

    return render_template('login.html')

# 註冊頁：GET 顯示表單，POST 寫入資料庫
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_name = request.form['user_name']
        email = request.form['email']
        password = request.form['password']
        age = request.form['age']

        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        if cursor.fetchone():
            return render_template('register.html', error="此 email 已註冊")

        cursor.execute(
            "INSERT INTO User (user_name, email, password, age) VALUES (%s, %s, %s, %s)",
            (user_name, email, password, age)
        )
        db.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# 登出
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
