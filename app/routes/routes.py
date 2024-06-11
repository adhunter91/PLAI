import json

from flask import Blueprint, request, jsonify, current_app
from app import create_app
from ..services.screener_processing import filter_data_by_skill, find_total_skills

bp = Blueprint('routes', __name__)
@bp.route('/')
def test_route():
    return "Test route is working!"


@bp.route('/home')
def home_route():
    return "This is the home page!"

def zoho_test():
    if request.method == 'GET':
        current_app.logger.info(f"GET request args: {request.args}")
        data = request.args
        return jsonify({"message": "Get request received"})
    elif request.method == 'POST':
        data = request.get_json()
        #print(f"This is how data variable appears: {data}")
        current_app.logger.info(f"POST request data: {request.json}")
        return jsonify({"message": "POST request received", "This is the received data": data})
@bp.route('/zoho_calculate_score', methods=['GET', 'POST'])
def zoho_calculate_score():
    if request.method == 'GET':
        current_app.logger.info(f"GET request args: {request.args}")
        data = request.args
        return jsonify({"message": "Get request received"})
    elif request.method == 'POST':
        data = request.get_json()
        #print(f"This is how data variable appears: {data}")
        filtered_data = filter_data_by_skill(data)

        current_app.logger.info(f"POST request data: {request.json}")
        current_app.logger.info(f"Filtered Data {filtered_data}")

        skills_score = find_total_skills(filtered_data)

        current_app.logger.info(f"Filtered Skills {skills_score}")
        #current_app.logger.info(f"Converted Data: {converted_data}")
        return jsonify({"message": "POST request received", "This is the received data": skills_score})

#Receive results
# Convert to format
# Loop through Dictionary and assign to new dict based on matches
# Count Score, all Yeses, count total entries
# Send to Database with Scores: Table " DB"
# Extract email, Add user profile contents, add as last question
# Create user_ID

# Error Handling and configuring

@bp.route('/trigger-400', methods=['POST'])
def trigger_400():
    if not request.json:
        from flask import abort
        abort(400)
    return 'Valid request received'

@bp.route('/trigger-403', methods=['GET'])
def trigger_403():
    from flask import abort
    abort(403)

@bp.route('/trigger-500', methods=['GET'])
def trigger_500():
    raise Exception("This is a test exception to trigger a 500 error")
@bp.errorhandler(404)
def not_found_error(error):
    current_app.logger.error(f"404 error at {request.url}: {error}")
    return {
        "error": "Not Found",
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers)
    }, 404

@bp.errorhandler(500)
def internal_error(error):
    trace = traceback.format_exc()
    current_app.logger.error(f"500 error at {request.url}: {error}\n{trace}")
    return {
        "error": "Internal Server Error",
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers),
        "trace": trace
    }, 500

@bp.errorhandler(403)
def forbidden_error(error):
    current_app.logger.error(f"403 error at {request.url}: {error}")
    return {
        "error": "Forbidden",
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers)
    }, 403

@bp.errorhandler(400)
def bad_request_error(error):
    current_app.logger.error(f"400 error at {request.url}: {error}")
    return {
        "error": "Bad Request",
        "url": request.url,
        "method": request.method,
        "headers": dict(request.headers)
    }, 400