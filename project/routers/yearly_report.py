from flask import Blueprint, request, render_template
from db.db import cursor

yearly_report_bp = Blueprint('yearly_report', __name__)

@yearly_report_bp.route('/report')
def show_report():
    raw_user_id = request.args.get('user_id')
    year = request.args.get('year')

    if not raw_user_id or not year:
        return "請提供 user_id（或名稱）與 year", 400

    try:
        user_id = int(raw_user_id)
    except ValueError:
        cursor.execute("SELECT user_id FROM User WHERE user_name = %s", (raw_user_id,))
        result = cursor.fetchone()
        if result:
            user_id = result['user_id']
        else:
            return f"找不到使用者名稱：{raw_user_id}", 404

    try:
        year = int(year)
    except ValueError:
        return "year 必須是整數", 400
    cursor.execute("""
        SELECT COUNT(*) AS total_count
        FROM WatchLog
        WHERE user_id = %s AND YEAR(watch_date) = %s
    """, (user_id, year))
    total_count = cursor.fetchone()['total_count'] or 0


    cursor.execute("""
        SELECT COUNT(DISTINCT M.genre) AS genre_count
        FROM WatchLog W
        JOIN Movie M ON W.movie_id = M.movie_id
        WHERE W.user_id = %s AND YEAR(W.watch_date) = %s
    """, (user_id, year))
    genre_count = cursor.fetchone()['genre_count'] or 0

    cursor.execute("""
        SELECT SUM(M.duration) AS total_minutes
        FROM WatchLog W
        JOIN Movie M ON W.movie_id = M.movie_id
        WHERE W.user_id = %s AND YEAR(W.watch_date) = %s
    """, (user_id, year))
    total_minutes = cursor.fetchone()['total_minutes'] or 0


    cursor.execute("""
        SELECT ROUND(AVG(rating), 1) AS average_rating
        FROM WatchLog
        WHERE user_id = %s AND YEAR(watch_date) = %s
    """, (user_id, year))
    avg_rating = cursor.fetchone()['average_rating'] or 0

    return render_template('yearly_report.html',
                           user_id=user_id,
                           year=year,
                           total_watched=total_count,
                           distinct_genres=genre_count,
                           total_minutes=total_minutes,
                           average_rating=avg_rating)
