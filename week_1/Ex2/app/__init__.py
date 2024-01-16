"""
Exercise 2:
Show a random quote from a list of quotes.
"""
from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)

    return app