from flask import Blueprint, render_template, redirect, url_for, session

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if 'user_name' in session:
        return render_template('index.html', user_name=session['user_name'])
    else:
        return redirect(url_for('auth.login'))
