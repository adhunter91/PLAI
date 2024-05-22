from flask import Blueprint, request, jsonify

# Create a Blueprint for handling webhooks
webhook_blueprint = Blueprint('webhook', __name__)


# Define a route to handle webhook requests
@webhook_blueprint.route('/event', methods=['POST'])
def handle_webhook():
    try:
        data = request.json
        # Assuming a function process_data() processes the received data
        process_data(data)
        return jsonify({'status': 'success', 'data_received': data}), 200
    except KeyError as e:
        return jsonify({'error': 'Data formatting error', 'details': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

def process_data(data):
    # Example processing function
    print("Processing data:", data)
    # Imagine we expect a 'name' key which is mandatory
    if 'name' not in data:
        raise KeyError("Missing 'name' key in the provided data")

# Error handler for 404 Not Found
@webhook_blueprint.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Resource not found', 'details': str(error)}), 404

# Error handler for 500 Internal Server Error
@webhook_blueprint.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'details': str(error)}), 500