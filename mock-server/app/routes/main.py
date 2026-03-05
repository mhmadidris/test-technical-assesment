from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/api/health')
def health_check():
    return {"status": "success", "message": "Service is healthy"}, 200

@main_bp.route('/')
def index():
    return {"status": "success", "message": "Flask API is ready"}
