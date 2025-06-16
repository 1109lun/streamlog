from flask import Blueprint, jsonify, session, render_template
from crud.favorite import add_favorite, remove_favorite, get_favorites, is_favorite

favorite_bp = Blueprint('favorite', __name__)

@favorite_bp.route('/favorites', methods=['GET'])
def list_favorites():
    if 'user_id' not in session:
        return render_template('login.html')
    return render_template('favorites.html', user_name=session.get('user_name'))

@favorite_bp.route('/api/favorites', methods=['GET'])
def get_favorites_api():
    try:
        if 'user_id' not in session:
            return jsonify({'error': '請先登入'}), 401
        
        user_id = session['user_id']
        favorites = get_favorites(user_id)
        return jsonify(favorites)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorite_bp.route('/api/favorites/<int:movie_id>', methods=['POST'])
def add_movie_favorite(movie_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': '請先登入'}), 401
        
        user_id = session['user_id']
        if is_favorite(user_id, movie_id):
            return jsonify({'error': '電影已經在收藏清單中'}), 400
        
        success = add_favorite(user_id, movie_id)
        if success:
            return jsonify({'message': '成功加入收藏'}), 201
        else:
            return jsonify({'error': '加入收藏失敗'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorite_bp.route('/api/favorites/<int:movie_id>', methods=['DELETE'])
def remove_movie_favorite(movie_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': '請先登入'}), 401
        
        user_id = session['user_id']
        if not is_favorite(user_id, movie_id):
            return jsonify({'error': '電影不在收藏清單中'}), 400
        
        success = remove_favorite(user_id, movie_id)
        if success:
            return jsonify({'message': '成功取消收藏'}), 200
        else:
            return jsonify({'error': '取消收藏失敗'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@favorite_bp.route('/api/favorites/<int:movie_id>/status', methods=['GET'])
def check_favorite_status(movie_id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': '請先登入'}), 401
        
        user_id = session['user_id']
        is_fav = is_favorite(user_id, movie_id)
        return jsonify({'is_favorite': is_fav})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 