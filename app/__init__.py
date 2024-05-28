from flask import Flask
from supabase import create_client
from config import Config
from .webhooks import webhook_blueprint
from dotenv import load_dotenv, find_dotenv
import os


def create_app(config_filename=None):

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

    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    #app.config['SECRET_KEY'] ='test_value12345678910'
    #if DEBUG == True:
    #   print(f'SIMPLETEXTING_API_KEY: {os.getenv('SIMPLETEXTING_API_KEY')}')
    #print(f'SUPABASE_KEY: {os.getenv('SUPABASE_KEY')}')
    #print(f'SUPABASE_URL: {os.getenv('SUPABASE_URL')}')

    app = Flask(__name__)

    if config_filename:
        app.config.from_pyfile(config_filename)
    else:
        app.config.from_object(Config)

    #initialize the Supabase Client
    app.supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    app.register_blueprint(webhook_blueprint, url_prefix='/webhook')

    return app