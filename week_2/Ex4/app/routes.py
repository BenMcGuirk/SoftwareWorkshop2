from flask import Blueprint, render_template, request

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template('index.html')

@main_bp.route('/header')
def header():
    lines = []
    with open('en-abbreviations.txt') as file:
        for line in file:
            if not line.startswith('#'):
                lines.append(line.strip().replace('\t', ' '))
    first10 = lines[:10]
    return render_template('header.html', lines=first10)

@main_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search.html')
    with open('en-abbreviations.txt') as file:
        abbreviations = [line.strip() for line in file if not line.startswith('#')]
    query = request.form['query']  # Convert input to uppercase for case-insensitive search
    # Filter abbreviations that start with the query (case-insensitive)
    results = [abbr for abbr in abbreviations if abbr.upper().startswith(query.upper())]
    # Limit results to maximum 10
    #results = results[:10]
    return render_template('results.html', results=results)