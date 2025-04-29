from flask import Blueprint, request, jsonify
import bcrypt
from db.db import db, cursor

auth_bp = Blueprint('auth', __name__)

# 註冊 API
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    user_name = data["user_name"]
    email = data["email"]
    password = data["password"]
    age = data["age"]

    cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cursor.execute(
        "INSERT INTO User (user_name, email, password, age) VALUES (%s, %s, %s, %s)",
        (user_name, email, hashed_password, age)
    )
    db.commit()

    return jsonify({"message": "User registered successfully"}), 201

# 登入 API
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    cursor.execute("SELECT * FROM User WHERE email = %s", (email,))
    user = cursor.fetchone()

    if user is None:
        return jsonify({"error": "Invalid email or password"}), 400

    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return jsonify({"error": "Invalid email or password"}), 400

    return jsonify({"message": "Login successful", "username": user["user_name"]}), 200

