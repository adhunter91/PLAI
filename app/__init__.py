import time
from flask import Flask, request, jsonify
from supabase import create_client
from config import Config
from .webhooks import webhook_blueprint
from dotenv import load_dotenv, find_dotenv
import os


def create_app(config_filename=None):
    start_time = time.time()
    print("Start creating app...")
    #dotenv_path = find_dotenv()
    #if dotenv_path:
    #    load_dotenv(dotenv_path)
    #    print(f"PASS: Loaded .env file from {dotenv_path}")
    #else:
    #    print("ERROR: .env file not found")
    basedir = os.path.abspath(os.path.dirname(__file__))
    #print(f'Basedir: {basedir}')
    #print(f'dotenv path: {os.path.join(basedir, '..', '.env')}')
    load_dotenv(os.path.join(basedir, '..', '.env'))
    print(f"Environment loaded in {time.time() - start_time:.3f} seconds.")

    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    #app.config['SECRET_KEY'] ='test_value12345678910'
    #if DEBUG == True:
    #   print(f'SIMPLETEXTING_API_KEY: {os.getenv('SIMPLETEXTING_API_KEY')}')
    #print(f'SUPABASE_KEY: {os.getenv('SUPABASE_KEY')}')
    #print(f'SUPABASE_URL: {os.getenv('SUPABASE_URL')}')

    app = Flask(__name__)
    print(f"Flask app instance created in {time.time() - start_time:.3f} seconds.")

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object(Config)
    print(f"Configuration loaded in {time.time() - start_time:.3f} seconds.")
    #initialize the Supabase Client
    app.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"Supabase Client loaded in {time.time() - start_time:.3f} seconds.")


    app.register_blueprint(webhook_blueprint, url_prefix='/webhook')
    print(f"Webhook blueprint registered in {time.time() - start_time:.3f} seconds.")

    @app.route('/')
    def test_route():
        return "Test route is working!"

    @app.route('/home')
    def home_route():
        return "This is the home page!"

    @app.route('/zohotest', methods=['GET', 'POST'])
    def zoho_test():
        if request.method == 'GET':
            return jsonify({"message": "Get request received"})
        elif request.method == 'POST':
            data = request.get_json()
            return jsonify({"message": "POST request received", "This is the received data": data})



    print(f"Application initialized in {time.time() - start_time:.3f} seconds.")
    #from app.routes import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    return app