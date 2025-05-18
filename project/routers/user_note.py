from flask import Blueprint, request, jsonify, render_template, session

from crud.user_note import (
    create_user_note, get_user_note, update_user_note,
    delete_user_note, get_all_user_notes,
    get_user_notes_by_movie, get_user_notes_by_user,
    toggle_note_like
)

user_note_bp = Blueprint('user_note', __name__)

@user_note_bp.route('/notes', methods=['GET'])
def list():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    return render_template('notes.html', user_name=user_name, user_id=user_id)

@user_note_bp.route('/api/notes', methods=['GET'])
def get_all():
    try:
        notes = get_all_user_notes()
        return jsonify(notes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_note_bp.route('/api/notes', methods=['POST'])
def create():
    try:
        data = request.get_json()
        result = create_user_note(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_note_bp.route('/api/notes/<int:note_id>', methods=['GET'])
def get(note_id):
    try:
        note = get_user_note(note_id)
        if note:
            return jsonify(note)
        return jsonify({'error': 'Cannot find the note'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_note_bp.route('/api/notes/<int:note_id>', methods=['PUT'])
def update(note_id):
    try:
        data = request.get_json()
        result = update_user_note(note_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_note_bp.route('/api/notes/<int:note_id>', methods=['DELETE'])
def delete(note_id):
    try:
        result = delete_user_note(note_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_note_bp.route('/api/notes/movie/<int:movie_id>', methods=['GET'])
def get_by_movie(movie_id):
    try:
        notes = get_user_notes_by_movie(movie_id)
        return jsonify(notes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_note_bp.route('/api/notes/user/<int:user_id>', methods=['GET'])
def get_by_user(user_id):
    try:
        notes = get_user_notes_by_user(user_id)
        return jsonify(notes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_note_bp.route('/api/notes/<int:note_id>/like', methods=['POST'])
def like_note(note_id):
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    result, status_code = toggle_note_like(note_id, user_id)
    return jsonify(result), status_code 