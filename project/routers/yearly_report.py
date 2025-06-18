from flask import Blueprint, request, render_template , session, jsonify
from db.db import cursor

yearly_report_bp = Blueprint('yearly_report', __name__)

@yearly_report_bp.route("/form")
def query_form():
    user_name = session.get("user_name")  
    return render_template("yearly_query_form.html", user_name=user_name)

@yearly_report_bp.route('/report')
def show_report():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    year = request.args.get('year')

    if not user_id:
        return "請先登入", 401
    if not year:
        return "請提供年份", 400
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
                           user_name=user_name,
                           year=year,
                           total_watched=total_count,
                           distinct_genres=genre_count,
                           total_minutes=total_minutes,
                           average_rating=avg_rating)



@yearly_report_bp.route('/api/report-data')
def report_data_api():
    user_id = session.get('user_id')
    year = request.args.get('year', type=int)

    if not user_id or not year:
        return jsonify({'error': '缺少 user_id 或 year'}), 400

    # 類型分佈資料（圓餅圖）
    cursor.execute("""
        SELECT M.genre, COUNT(*) AS count
        FROM WatchLog W
        JOIN Movie M ON W.movie_id = M.movie_id
        WHERE W.user_id = %s AND YEAR(W.watch_date) = %s
        GROUP BY M.genre
    """, (user_id, year))
    genre_rows = cursor.fetchall()
    genre_data = {
        "labels": [row['genre'] for row in genre_rows],
        "data": [row['count'] for row in genre_rows]
    }

    # 每月觀影次數（長條圖）
    cursor.execute("""
        SELECT MONTH(watch_date) AS month, COUNT(*) AS count
        FROM WatchLog
        WHERE user_id = %s AND YEAR(watch_date) = %s
        GROUP BY MONTH(watch_date)
        ORDER BY month
    """, (user_id, year))
    month_rows = cursor.fetchall()
    month_data = {
        "labels": [f"{row['month']}月" for row in month_rows],
        "data": [row['count'] for row in month_rows]
    }

    # 情緒資料（雷達圖）
    mood_translation = {
        'excited': '興奮',
        'thoughtful': '放鬆',
        'sad': '難過',
        'happy': '開心',
        'relaxed': '放鬆'
    }
    all_moods = ['開心', '難過', '興奮', '放鬆']

    cursor.execute("""
        SELECT mood, COUNT(*) AS count
        FROM WatchLog
        WHERE user_id = %s AND YEAR(watch_date) = %s
        GROUP BY mood
    """, (user_id, year))
    mood_rows = cursor.fetchall()

    mood_count_map = {}
    total_count = 0
    for row in mood_rows:
        mood_eng = row['mood']
        count = row['count']
        mood_chi = mood_translation.get(mood_eng)
        if mood_chi:
            mood_count_map[mood_chi] = mood_count_map.get(mood_chi, 0) + count
            total_count += count

    emotion_data = {
        "labels": all_moods,
        "data": [
            round((mood_count_map.get(mood, 0) / total_count) * 100, 1) if total_count > 0 else 0
            for mood in all_moods
        ]
    }

    # 找出使用者最常看的 genre
    cursor.execute("""
        SELECT M.genre
        FROM WatchLog W
        JOIN Movie M ON W.movie_id = M.movie_id
        WHERE W.user_id = %s
        GROUP BY M.genre
        ORDER BY COUNT(*) DESC
        LIMIT 1
    """, (user_id,))
    genre_row = cursor.fetchone()
    favorite_genre = genre_row['genre'] if genre_row else None

    recommended_movies = []
    if favorite_genre: # 在該類型中找出使用者沒看過的電影
        cursor.execute("""
            SELECT M.movie_id, M.title, M.genre, M.rating, M.image_url
            FROM Movie M
            WHERE M.genre = %s
              AND M.movie_id NOT IN (
                  SELECT movie_id
                  FROM WatchLog
                  WHERE user_id = %s
              )
            ORDER BY M.rating DESC
            LIMIT 5
        """, (favorite_genre, user_id))
        recommended_movies = cursor.fetchall()

    return jsonify({
        "genre": genre_data,
        "monthly": month_data,
        "emotion": emotion_data,
        "recommendations": recommended_movies
    })
