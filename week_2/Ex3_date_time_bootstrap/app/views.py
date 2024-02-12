from flask import render_template
from app import app
from datetime import datetime

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', now=now)

