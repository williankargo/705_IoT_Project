from flask import Flask
from flask_cors import CORS
from routes import blueprint
import logging


def create_app():
    app = Flask(__name__)
    # app.logger.setLevel(logging.INFO)
    CORS(app)  # CORS setting
    app.register_blueprint(blueprint)
    return app
