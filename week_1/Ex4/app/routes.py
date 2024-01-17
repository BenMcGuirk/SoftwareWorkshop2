from flask import Flask, render_template, request
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template('index.html')

@main_bp.route('/app')
def app():
    return render_template('app.html')

@main_bp.route('/request')
def request():
    return render_template('request.html')