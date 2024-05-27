from flask import Flask
from supabase import create_client, Client
from config import Config
from .webhooks import webhook_blueprint

def create_app(config_filename):
    app = Flask(__name__)
    #app.config['SECRET_KEY'] ='test_value12345678910'
    #app.config.from_pyfile(config_filename)
    app.config.from_object(Config)

    #initialize the Supabase Client
    app.supabase = create_client(app.config['SUPABASE_URL'], app.config['SUPABASE_KEY'])

    app.register_blueprint(webhook_blueprint, url_prefix='/webhook')

    return app