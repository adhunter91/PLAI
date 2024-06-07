from flask import Blueprint, request, jsonify, current_app
from app import create_app

bp = Blueprint('routes', __name__)
@bp.route('/')
def test_route():
    return "Test route is working!"


@bp.route('/home')
def home_route():
    return "This is the home page!"


@bp.route('/zohotest', methods=['GET', 'POST'])
def zoho_test():
    if request.method == 'GET':
        curernt_app.logger.info(f"GET request args: {request.args}")
        return jsonify({"message": "Get request received"})
    elif request.method == 'POST':
        data = request.get_json()
        current_app.logger.info(f"POST request data: {request.json}")
        return jsonify({"message": "POST request received", "This is the received data": data})

