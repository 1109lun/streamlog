from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from db.db import db, cursor
from routers.auth import auth_bp
from routers.home import home_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = 'streamlogeight'
CORS(app)

# 註冊路由
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

if __name__ == "__main__":
    app.run(debug=True)
