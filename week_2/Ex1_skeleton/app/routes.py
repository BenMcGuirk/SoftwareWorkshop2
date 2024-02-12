from flask import Flask, render_template
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template('index.html')