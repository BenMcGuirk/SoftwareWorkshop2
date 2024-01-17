"""
Exercise 4:
Create an app that shows values from the App object on one page and values from
the Request object on another page.
"""

from flask import Flask, request

def create_app():
    app = Flask(__name__)

    