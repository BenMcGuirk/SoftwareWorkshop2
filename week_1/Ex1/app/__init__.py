"""
Exercise 1: 
create app displaying date and time to the user. (use proposed structure)
"""
from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)

    return app