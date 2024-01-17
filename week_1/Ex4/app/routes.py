from flask import Flask, render_template, request, jsonify
from flask import Blueprint

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return render_template('index.html')

@main_bp.route('/app') #return values of App object
def app_info():
    from app import create_app
    app = create_app()
    info = {
        'url_map': str(app.url_map),
    }
    return render_template('app.html', app_info=jsonify(info).json)

@main_bp.route('/request')
def request_info():
    info = {
        'args': str(request.args),
        'cookies': str(request.cookies),
        'headers': str(request.headers),
        'method': str(request.method),
        'url': str(request.url),
        'url_root': str(request.url_root),
        'user_agent': str(request.user_agent),
    }

    return render_template('request.html', request_info=jsonify(info).json)