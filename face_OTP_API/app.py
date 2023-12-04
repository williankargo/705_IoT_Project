from flask import Flask, g
from flask_cors import CORS
from routes import blueprint
import logging
from database import DatabaseManager  # Import the DatabaseManager class

def create_app():
    app = Flask(__name__)
    # app.logger.setLevel(logging.INFO)
    CORS(app)  # CORS setting
    app.register_blueprint(blueprint)

    # DataBase function
    with app.app_context():
        # g.app = app
        # Initialize the database
        g.db_manager = DatabaseManager()
        g.db_manager.initialize_db()  # Call the initialize_db method

    return app