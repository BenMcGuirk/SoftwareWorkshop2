from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    # Create columns
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create a string
    def __repr__(self):
        return '<Task %r>' % self.id
    
# flask shell context setup
@app.shell_context_processor
def make_shell_context():
    return {'app': app, 'db': db, 'Todo': Todo}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content'] # get the content from the form
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) # add the new task to the database
            db.session.commit() # commit the new task to the database
            return redirect('/') # redirect to the index page
        except:
            return 'There was an issue adding your task'
    else:  
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete) # delete the task
        db.session.commit() # commit the deletion
        return redirect('/') # redirect to the index page
    except:
        return 'There was a problem deleting that task'
    
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task_to_update.content = request.form['content']

        try:
            db.session.commit() # commit the update
            return redirect('/') # redirect to the index page
        except:
            return 'There was an issue updating your task'
        
    else: 
        return render_template('update.html', task=task_to_update or None)

if __name__ == '__main__':
    app.run(debug=True)