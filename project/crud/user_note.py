from db.db import cursor

def create_user_note(data):
    try:
        required_fields = ['user_id', 'movie_id', 'content']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, 400
        
        cursor.execute("SELECT movie_id FROM Movie WHERE movie_id = %s", (data['movie_id'],))
        if not cursor.fetchone():
            return {'error': 'Movie not found'}, 404
        
        cursor.execute("SELECT user_id FROM User WHERE user_id = %s", (data['user_id'],))
        if not cursor.fetchone():
            return {'error': f'User {data["user_id"]} not found'}, 404
        
        cursor.execute("""
            INSERT INTO UserNote (user_id, movie_id, content)
            VALUES (%s, %s, %s)
        """, (data['user_id'], data['movie_id'], data['content']))
        
        note_id = cursor.lastrowid
        
        return {
            'message': 'User note created successfully',
            'note_id': note_id,
            'user_id': data['user_id'],
            'movie_id': data['movie_id'],
            'content': data['content']
        }, 201
        
    except Exception as e:
        return {'error': str(e)}, 500

def get_user_note(note_id):
    cursor.execute("""
        SELECT N.*, U.user_name, M.title,
               (SELECT COUNT(*) FROM NoteLike WHERE note_id = N.note_id) as like_count,
               (SELECT GROUP_CONCAT(user_id) FROM NoteLike WHERE note_id = N.note_id) as liked_by
        FROM UserNote N
        JOIN User U ON N.user_id = U.user_id
        JOIN Movie M ON N.movie_id = M.movie_id
        WHERE N.note_id = %s
    """, (note_id,))
    
    note = cursor.fetchone()
    if not note:
        return {'error': f'Cannot find the note {note_id}'}, 404
    
    note = dict(note)
    if note['liked_by']:
        note['liked_by'] = [int(x) for x in note['liked_by'].split(',')]
    else:
        note['liked_by'] = []
    
    return note, 200

def update_user_note(note_id, data):
    try:
        cursor.execute("SELECT * FROM UserNote WHERE note_id = %s", (note_id,))
        if not cursor.fetchone():
            return {'error': f'Cannot find the note {note_id}'}, 404
        
        if 'content' not in data:
            return {'error': 'No content to update'}, 400
        
        cursor.execute("""
            UPDATE UserNote 
            SET content = %s
            WHERE note_id = %s
        """, (data['content'], note_id))
        
        return {'message': 'User note updated successfully'}, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

def delete_user_note(note_id):
    cursor.execute("SELECT * FROM UserNote WHERE note_id = %s", (note_id,))
    if not cursor.fetchone():
        return {'error': f'Cannot find the note {note_id}'}, 404
    
    cursor.execute("DELETE FROM UserNote WHERE note_id = %s", (note_id,))
    
    return {'message': 'Delete successfully'}, 200

def get_all_user_notes():
    try:
        cursor.execute("""
            SELECT N.*, U.user_name, M.title,
                   (SELECT COUNT(*) FROM NoteLike WHERE note_id = N.note_id) as like_count,
                   (SELECT GROUP_CONCAT(user_id) FROM NoteLike WHERE note_id = N.note_id) as liked_by
            FROM UserNote N
            JOIN User U ON N.user_id = U.user_id
            JOIN Movie M ON N.movie_id = M.movie_id
            ORDER BY N.created_at DESC
        """)
        
        notes = cursor.fetchall()
        
        if not notes:
            return []
        
        result = []
        for note in notes:
            note = dict(note)
            if note['liked_by']:
                note['liked_by'] = [int(x) for x in note['liked_by'].split(',')]
            else:
                note['liked_by'] = []
            result.append(note)
            
        return result
    except Exception as e:
        return {'error': str(e)}, 500

def get_user_notes_by_movie(movie_id):
    try:
        cursor.execute("""
            SELECT N.*, U.user_name,
                   (SELECT COUNT(*) FROM NoteLike WHERE note_id = N.note_id) as like_count,
                   (SELECT GROUP_CONCAT(user_id) FROM NoteLike WHERE note_id = N.note_id) as liked_by
            FROM UserNote N
            JOIN User U ON N.user_id = U.user_id
            WHERE N.movie_id = %s
            ORDER BY N.created_at DESC
        """, (movie_id,))
        
        notes = cursor.fetchall()
        
        if not notes:
            return []
        
        result = []
        for note in notes:
            note = dict(note)
            if note['liked_by']:
                note['liked_by'] = [int(x) for x in note['liked_by'].split(',')]
            else:
                note['liked_by'] = []
            result.append(note)
            
        return result
    except Exception as e:
        return {'error': str(e)}, 500

def get_user_notes_by_user(user_id):
    try:
        cursor.execute("""
            SELECT N.*, M.title,
                   (SELECT COUNT(*) FROM NoteLike WHERE note_id = N.note_id) as like_count,
                   (SELECT GROUP_CONCAT(user_id) FROM NoteLike WHERE note_id = N.note_id) as liked_by
            FROM UserNote N
            JOIN Movie M ON N.movie_id = M.movie_id
            WHERE N.user_id = %s
            ORDER BY N.created_at DESC
        """, (user_id,))
        
        notes = cursor.fetchall()
        
        if not notes:
            return []
        
        result = []
        for note in notes:
            note = dict(note)
            if note['liked_by']:
                note['liked_by'] = [int(x) for x in note['liked_by'].split(',')]
            else:
                note['liked_by'] = []
            result.append(note)
            
        return result
    except Exception as e:
        return {'error': str(e)}, 500

def toggle_note_like(note_id, user_id):
    try:
        cursor.execute("SELECT * FROM UserNote WHERE note_id = %s", (note_id,))
        if not cursor.fetchone():
            return {'error': f'Cannot find the note {note_id}'}, 404
        
        cursor.execute("SELECT * FROM User WHERE user_id = %s", (user_id,))
        if not cursor.fetchone():
            return {'error': f'User {user_id} not found'}, 404
        
        cursor.execute("SELECT * FROM NoteLike WHERE note_id = %s AND user_id = %s", (note_id, user_id))
        existing_like = cursor.fetchone()
        
        if existing_like:
            cursor.execute("DELETE FROM NoteLike WHERE note_id = %s AND user_id = %s", (note_id, user_id))
        else:
            cursor.execute("INSERT INTO NoteLike (note_id, user_id) VALUES (%s, %s)", (note_id, user_id))
        
        # Access the updated like count and liked_by
        cursor.execute("""
            SELECT 
                (SELECT COUNT(*) FROM NoteLike WHERE note_id = %s) as like_count,
                (SELECT GROUP_CONCAT(user_id) FROM NoteLike WHERE note_id = %s) as liked_by
        """, (note_id, note_id))
        
        result = cursor.fetchone()
        result = dict(result)
        
        if result['liked_by']:
            result['liked_by'] = [int(x) for x in result['liked_by'].split(',')]
        else:
            result['liked_by'] = []
        
        return result, 200
        
    except Exception as e:
        return {'error': str(e)}, 500 