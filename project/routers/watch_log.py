from flask import Blueprint, request, jsonify, render_template, session

from crud.watch_log import (
    create_watch_log, get_watch_log, update_watch_log, 
    delete_watch_log, get_all_watch_logs
)

watch_log_bp = Blueprint('watch_log', __name__)

@watch_log_bp.route('/watch-logs', methods=['GET'])
def list():
    user_name = session.get('user_name')
    user_id = session.get('user_id')
    return render_template('list.html', user_name=user_name, user_id=user_id)

@watch_log_bp.route('/api/watch-logs', methods=['GET'])
def get_all():
    try:
        logs = get_all_watch_logs()
        return jsonify(logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@watch_log_bp.route('/api/watch-logs', methods=['POST'])
def create():
    try:
        data = request.get_json()
        result = create_watch_log(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@watch_log_bp.route('/api/watch-logs/<int:watch_id>', methods=['GET'])
def get(watch_id):
    try:
        log = get_watch_log(watch_id)
        if log:
            return jsonify(log)
        return jsonify({'error': 'Watch log not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@watch_log_bp.route('/api/watch-logs/<int:watch_id>', methods=['PUT'])
def update(watch_id):
    try:
        data = request.get_json()
        result = update_watch_log(watch_id, data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@watch_log_bp.route('/api/watch-logs/<int:watch_id>', methods=['DELETE'])
def delete(watch_id):
    try:
        delete_watch_log(watch_id)
        return jsonify({'message': 'Watch log deleted'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400 