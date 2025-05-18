from datetime import datetime

from db.db import cursor

def create_watch_log(data):
    try:
        required_fields = ['user_id', 'movie_id', 'watch_date', 'rating']
        for field in required_fields:
            if field not in data:
                return {'error': f'Lack of required field: {field}'}, 400
        
        try:
            watch_date = datetime.strptime(data['watch_date'], '%Y-%m-%d')
        except ValueError:
            return {'error': 'Date format must be YYYY-MM-DD'}, 400
        
        if not 0 <= float(data['rating']) <= 10:
            return {'error': 'Rating must be between 0 and 10'}, 400
        
        cursor.execute("SELECT movie_id FROM Movie WHERE movie_id = %s", (data['movie_id'],))
        if not cursor.fetchone():
            return {'error': 'Unable to find the movie'}, 404
        
        cursor.execute("SELECT user_id FROM User WHERE user_id = %s", (data['user_id'],))
        if not cursor.fetchone():
            return {'error': 'Unable to find the user'}, 404
        
        cursor.execute("""
            INSERT INTO WatchLog (user_id, movie_id, watch_date, mood, rating)
            VALUES (%s, %s, %s, %s, %s)
        """, (data['user_id'], data['movie_id'], watch_date, data.get('mood'), data['rating']))
        
        watch_id = cursor.lastrowid
        
        return {
            'message': 'Create watch log successfully',
            'watch_id': watch_id
        }, 201
        
    except Exception as e:
        return {'error': str(e)}, 500

def get_watch_log(watch_id):
    cursor.execute("""
        SELECT W.*, M.title, M.genre, M.duration
        FROM WatchLog W
        JOIN Movie M ON W.movie_id = M.movie_id
        WHERE W.watch_id = %s
    """, (watch_id,))
    
    log = cursor.fetchone()
    if not log:
        return {'error': 'Unable to find the watch log'}, 404
    
    return dict(log), 200

def update_watch_log(watch_id, data):
    try:
        cursor.execute("SELECT * FROM WatchLog WHERE watch_id = %s", (watch_id,))
        if not cursor.fetchone():
            return {'error': 'Unable to find the watch log'}, 404
        
        update_fields = []
        params = []
        
        if 'watch_date' in data:
            try:
                watch_date = datetime.strptime(data['watch_date'], '%Y-%m-%d')
                update_fields.append('watch_date = %s')
                params.append(watch_date)
            except ValueError:
                return {'error': 'Date format must be YYYY-MM-DD'}, 400
        
        if 'mood' in data:
            update_fields.append('mood = %s')
            params.append(data['mood'])
            
        if 'rating' in data:
            if not 0 <= float(data['rating']) <= 10:
                return {'error': 'Rating must be between 0 and 10'}, 400
            update_fields.append('rating = %s')
            params.append(data['rating'])
        
        if not update_fields:
            return {'error': 'No fields to update'}, 400
        
        query = f"UPDATE WatchLog SET {', '.join(update_fields)} WHERE watch_id = %s"
        params.append(watch_id)
        cursor.execute(query, tuple(params))
        
        return {'message': 'Watch log updated successfully'}, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

def delete_watch_log(watch_id):
    cursor.execute("SELECT * FROM WatchLog WHERE watch_id = %s", (watch_id,))
    if not cursor.fetchone():
        return {'error': 'Unable to find the watch log'}, 404
    
    cursor.execute("DELETE FROM WatchLog WHERE watch_id = %s", (watch_id,))
    
    return {'message': 'Watch log deleted successfully'}, 200

def get_all_watch_logs():
    try:
        cursor.execute("""
            SELECT W.*, M.title, M.genre, M.duration
            FROM WatchLog W
            JOIN Movie M ON W.movie_id = M.movie_id
            ORDER BY W.watch_date DESC
        """)
        
        logs = cursor.fetchall()

        if not logs:
            return []
            
        result = [dict(log) for log in logs]
        return result
    except Exception as e:
        return {'error': str(e)}, 500

def get_all_movies():
    cursor.execute("SELECT movie_id, title FROM Movie ORDER BY title")
    movies = cursor.fetchall()
    return [dict(movie) for movie in movies] 