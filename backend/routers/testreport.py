from flask import request, render_template
from main import app, db

@app.route('/test')
def index():
    return render_template('report.html')

@app.route('/report')
def report():
    user_id = request.args.get('user_id')
    year = request.args.get('year')

    if not user_id or not year:
        return "請提供 user_id 和 year", 400

    # 假資料
    total_watch_count = 42
    distinct_genres = 8
    total_duration = 1230
    average_rating = 4.3
    monthly_counts = [{"month": 1, "count": 5}]
    genre_distribution = [{"type": "動作", "count": 10}]
    mood_distribution = [{"mood": "開心", "count": 12}]

    return render_template("report.html",
        year=year,
        total_watch_count=total_watch_count,
        distinct_genres=distinct_genres,
        total_duration=total_duration,
        average_rating=average_rating,
        monthly_counts=monthly_counts,
        genre_distribution=genre_distribution,
        mood_distribution=mood_distribution
    )
