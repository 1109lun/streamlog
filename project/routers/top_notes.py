from flask import Blueprint, jsonify, request
from db.db import cursor

note_like_bp = Blueprint('note_like', __name__)

@note_like_bp.route("/api/top_notes", methods=["GET"])
def top_liked_notes():
    range_type = request.args.get('range', 'total').strip()  # 預設為 total

    print("range_type =", range_type)
    
    if range_type == 'today':
        query = """
            SELECT 
                ul.note_id, 
                un.content,
                COUNT(*) AS like_count
            FROM NoteLike ul
            JOIN UserNote un ON ul.note_id = un.note_id
            WHERE DATE(ul.created_at) = CURDATE()
            GROUP BY ul.note_id
            ORDER BY like_count DESC
            LIMIT 10
        """
    elif range_type == 'total':
        query = """
            SELECT 
                ul.note_id, 
                un.content,
                COUNT(*) AS like_count
            FROM NoteLike ul
            JOIN UserNote un ON ul.note_id = un.note_id
            GROUP BY ul.note_id
            ORDER BY like_count DESC
            LIMIT 10
        """
    else:
        return jsonify({'error': 'Invalid range'}), 400

    cursor.execute(query)
    results = cursor.fetchall()
    return jsonify(results)
