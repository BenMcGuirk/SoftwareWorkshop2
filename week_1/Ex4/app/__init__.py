"""
Exercise 4:
Write an app that shows values from the App object on one page and the Request object 
on another. Extend this app by adding a navigation bar using template inheritance to 
simplify switching between pages.
"""
from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)

    return app