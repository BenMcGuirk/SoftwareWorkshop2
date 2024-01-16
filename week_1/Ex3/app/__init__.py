"""
Write an app that uses a dynamic route ending with a positive integer and generates a 
page that shows the prime divisors of the integer (which may be just 1 and the integer 
itself if it is prime). You can use code from the web for primality testing.
"""
from flask import Flask
from .routes import main_bp

def create_app():
    app = Flask(__name__)

    app.register_blueprint(main_bp)

    return app