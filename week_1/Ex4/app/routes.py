from flask import Blueprint, render_template
from flask import request
import flask

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    # Get values from the app object
    app_name = flask.current_app.config['APP_NAME']
    # Pass values to the template
    return render_template('home.html', app_name=app_name)

@main_bp.route('/show_request', methods=['GET', 'POST'])
def show_request():
    # Get values from the request object
    method = request.method
    user_agent = request.headers.get('User-Agent')
    form_data = request.form.to_dict()
    query_params = request.args.to_dict()
    # Pass values to the template
    return render_template('show_request.html', method=method, user_agent=user_agent, form_data=form_data, query_params=query_params)