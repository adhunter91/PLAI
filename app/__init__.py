import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from supabase import create_client
from config import Config
import logging
from .webhooks import webhook_blueprint
from dotenv import load_dotenv, find_dotenv
import os


def create_app(config_filename=None):
    start_time = time.time()
    print("Start creating app...")
    basedir = os.path.abspath(os.path.dirname(__file__))
    load_dotenv(os.path.join(basedir, '..', '.env'))
    print(f"Environment loaded in {time.time() - start_time:.3f} seconds.")

    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    app = Flask(__name__)
    print(f"Flask app instance created in {time.time() - start_time:.3f} seconds.")
    CORS(app)

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object(Config)
    print(f"Configuration loaded in {time.time() - start_time:.3f} seconds.")

    # Initialize the Supabase Client
    app.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print(f"Supabase Client loaded in {time.time() - start_time:.3f} seconds.")


    # Import Routes
    from app.routes import routes
    app.register_blueprint(routes.bp)


    print(f"Application initialized in {time.time() - start_time:.3f} seconds.")
    #from app.routes import main as main_blueprint
    #app.register_blueprint(main_blueprint)

    return app