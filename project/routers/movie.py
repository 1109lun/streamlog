from flask import Blueprint, request, jsonify, render_template, session

from crud.movie import get_all_movies

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/api/movies', methods=['GET'])
def get_movies():
    try:
        movies = get_all_movies()
        return jsonify(movies)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
