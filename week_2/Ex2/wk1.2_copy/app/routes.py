from flask import Blueprint, render_template, jsonify
import random

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def quote():
    with open('quotes.txt') as file:
        quotes = file.readlines()
    theQuote = random.choice(quotes)

    return render_template('index.html', quote=jsonify(theQuote).json)