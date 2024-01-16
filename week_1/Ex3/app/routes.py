from flask import Blueprint
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def quote():
    with open('quotes.txt') as file:
        quotes = file.readlines()
    return random.choice(quotes)