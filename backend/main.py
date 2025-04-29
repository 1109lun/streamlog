from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routers.auth import auth_bp
from db.db import db, cursor  # 正確引入共用的 db, cursor

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return "Streamlog backend is running!"

if __name__ == "__main__":
    app.run(debug=True)
