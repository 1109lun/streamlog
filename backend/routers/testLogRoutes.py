from flask import jsonify, request

from main import app, db
from models.testLogModel import Log

@app.route('/')
def hello_world():
    return {'message': 'Hello, World!'}

@app.route('/api/v1/logs', methods=['GET'])
def get_logs():
    logs = Log.query.all()
    return jsonify([log.to_dict() for log in logs])

@app.route('/api/v1/logs', methods=['POST'])
def create_log():
    data = request.get_json()
    
    new_log = Log(
        level=data['level'],
        message=data['message'],
        source=data.get('source')
    )
    
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify(new_log.to_dict()), 201

@app.route('/api/v1/logs/<int:log_id>', methods=['GET'])
def get_log(log_id):
    log = Log.query.get_or_404(log_id)
    return jsonify(log.to_dict()) 