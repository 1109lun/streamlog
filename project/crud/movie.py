from db.db import cursor

def get_all_movies():
    cursor.execute("SELECT movie_id, title FROM Movie ORDER BY title")
    movies = cursor.fetchall()
    return [dict(movie) for movie in movies] 