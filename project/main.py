from flask import Flask

from flask_cors import CORS
from dotenv import load_dotenv

from db.db import db, cursor
from routers.auth import auth_bp
from routers.home import home_bp
from routers.yearly_report import yearly_report_bp
from routers.watch_log import watch_log_bp
from routers.user_note import user_note_bp
from routers.movie import movie_bp
from routers.favorite import favorite_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = 'streamlogeight'
CORS(app)

# Register routers
app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)
app.register_blueprint(yearly_report_bp)
app.register_blueprint(watch_log_bp)
app.register_blueprint(user_note_bp)
app.register_blueprint(movie_bp)
app.register_blueprint(favorite_bp)

if __name__ == "__main__":
    app.run(debug=True)
