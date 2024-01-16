from flask import Blueprint
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    day = datetime.now().strftime("%d-%m-%Y")
    time = datetime.now().strftime("%H:%M:%S")
    return f"<h1>Hello, Flask! It's {time} on the {day}</h1>"