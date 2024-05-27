from flask import Blueprint, current_app, jsonify

main = Blueprint('main', __name__)

@main.route('/')
def index():
    #Use the Supabase client from the current app context
    supabase = current_app.supabase
    data = supabase.table('Test').select('*').execute()
    return jsonify(data.data) # or potentially data.json() if metadata is needed