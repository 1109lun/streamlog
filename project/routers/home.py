from flask import Blueprint, render_template, redirect, url_for, session, jsonify, request
from db.db import cursor
from datetime import datetime, timedelta

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    if 'user_name' not in session:
        return redirect(url_for('auth.login'))
    return render_template('index.html', user_name=session['user_name'])

@home_bp.route('/api/top_notes')
def api_top_notes():
    range_type = request.args.get('range', 'today')

    if range_type == 'today':
        time_filter = "AND nl.created_at >= CURDATE()"
    elif range_type == 'week':
        time_filter = "AND nl.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)"
    elif range_type == 'total':
        time_filter = ""  # 不加任何時間條件
    else:
        return jsonify({'error': 'Invalid range'}), 400

    cursor.execute(f"""
        SELECT u.user_name, m.title, n.content, COUNT(nl.user_id) AS like_count
        FROM NoteLike nl
        JOIN UserNote n ON nl.note_id = n.note_id
        JOIN User u ON n.user_id = u.user_id
        JOIN Movie m ON n.movie_id = m.movie_id
        WHERE 1=1 {time_filter}
        GROUP BY nl.note_id
        ORDER BY like_count DESC
        LIMIT 10;
    """)
    results = cursor.fetchall()

    return jsonify(results)

@home_bp.route('/search')
def search():
    if 'user_name' not in session:
        return redirect(url_for('auth.login'))  # 強制導向登入

    keyword = request.args.get('q', '').strip()

    if not keyword:
        return render_template('search_results.html', results=[], keyword=keyword, user_name=session['user_name'])

    query = """
        SELECT movie_id, title, genre, duration, release_year, rating
        FROM Movie
        WHERE title LIKE %s
    """
    like_pattern = f"%{keyword}%"
    cursor.execute(query, (like_pattern,))
    results = cursor.fetchall()

    return render_template('search_results.html', results=results, keyword=keyword, user_name=session['user_name'])


@home_bp.route('/api/autocomplete')
def autocomplete():
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify([])

    query = """
        SELECT title
        FROM Movie
        WHERE title LIKE %s
        LIMIT 10
    """
    like_pattern = f"%{keyword}%"
    cursor.execute(query, (like_pattern,))
    results = cursor.fetchall()

    movies = [{"title": row['title']} for row in results]
    return jsonify(movies)

@home_bp.route('/api/movie_notes/<int:movie_id>')
def movie_notes(movie_id):
    cursor.execute("""
        SELECT u.user_name, n.content, n.created_at
        FROM UserNote n
        JOIN User u ON n.user_id = u.user_id
        WHERE n.movie_id = %s
        ORDER BY n.created_at DESC
        LIMIT 10
    """, (movie_id,))
    
    notes = cursor.fetchall()

    return jsonify([
        {
            "user_name": row["user_name"],
            "content": row["content"],
            "created_at": row["created_at"].strftime("%Y-%m-%d %H:%M")
        } for row in notes
    ])






