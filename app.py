from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(os.getcwd(), 'test.db')

db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    warning = None  # initialize the warning message variable to None
    if request.method == 'POST':
        task_content = request.form['content'].title()
        new_task = Todo(content=task_content)
        # print(task_content)
        # return warning in the same page if the task is empty
        if task_content == '':
            warning = 'Please enter a task'
            # print("emty masssage")
        else:
            try:
                db.session.add(new_task)
                db.session.commit()
                return redirect('/')
            except:
                return 'There was an issue adding your task'

    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks, warning=warning)


@app.route('/delete/<int:id>')
def delete(id):
    warning = None
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        warning = 'Task deleted successfully'
        return redirect('/')
    except:
        return 'There was a problem deleting the task'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):

    warning = None  # initialize the warning message variable to None

    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content'].title()
        try:
            db.session.commit()

            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        warning = 'Task updated successfully'
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
