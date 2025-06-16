from db.db import cursor

def add_favorite(user_id: int, movie_id: int) -> bool:
    try:
        cursor.execute(
            "INSERT INTO MovieFavorite (user_id, movie_id) VALUES (%s, %s)",
            (user_id, movie_id)
        )
        return True
    except Exception as e:
        print(f"Error adding favorite: {e}")
        return False

def remove_favorite(user_id: int, movie_id: int) -> bool:
    try:
        cursor.execute(
            "DELETE FROM MovieFavorite WHERE user_id = %s AND movie_id = %s",
            (user_id, movie_id)
        )
        return True
    except Exception as e:
        print(f"Error removing favorite: {e}")
        return False

def get_favorites(user_id):
    cursor.execute("""
        SELECT m.movie_id, m.title, m.genre, m.release_year, m.rating, m.image_url
        FROM Movie m
        JOIN MovieFavorite f ON m.movie_id = f.movie_id
        WHERE f.user_id = %s
        ORDER BY f.created_at DESC
    """, (user_id,))
    favorites = cursor.fetchall()
    return [dict(movie) for movie in favorites]

def is_favorite(user_id: int, movie_id: int) -> bool:
    cursor.execute(
        "SELECT COUNT(*) as count FROM MovieFavorite WHERE user_id = %s AND movie_id = %s",
        (user_id, movie_id)
    )
    result = cursor.fetchone()
    return result['count'] > 0 