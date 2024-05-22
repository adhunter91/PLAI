from flask import Flask
from .webhooks import webhook_blueprint

def create_app(config_filename):
    app = Flask(__name__)
    app.config['SECRET_KEY'] ='test_value12345678910'
    #app.config.from_pyfile(config_filename)

    app.register_blueprint(webhook_blueprint, url_prefix='/webhook')

    return app