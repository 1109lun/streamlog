from flask import Blueprint, render_template, request, redirect, url_for, session
from db.db import db, cursor
import bcrypt

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            session['username'] = user['user_name']
            return redirect(url_for('home.home'))
        else:
            return render_template("login.html", error="帳號或密碼錯誤")

    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        user_name = request.form["user_name"]
        email = request.form["email"]
        password = request.form["password"]
        age = request.form["age"]

        cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
        if cursor.fetchone():
            return render_template("register.html", error="此 email 已註冊")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        cursor.execute(
            "INSERT INTO User (user_name, email, password, age) VALUES (%s, %s, %s, %s)",
            (user_name, email, hashed_password, age)
        )
        db.commit()
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth_bp.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("auth.login"))
