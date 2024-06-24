from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class MyDb(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(80), nullable=False)
    complete = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    def __repr__(self):
        return f'Task {self.id}'
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            task_content = request.form['task']
            new_task = MyDb(content=task_content)

            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except Exception as e:
            error_msg = f'Error adding task: {e}'
            print(error_msg)
            return error_msg, 500
    else:
        try:
            tasks = MyDb.query.order_by(MyDb.created.desc()).all()
            return render_template('index.html', tasks=tasks)
        except Exception as e:
            error_msg = f'Error retrieving tasks: {e}'
            print(error_msg)
            return error_msg, 500

@app.route("/delete/<int:id>")
def delete(id:int):
    try:
        delete_task = MyDb.query.get_or_404(id)
        db.session.delete(delete_task)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        return f'Error deleting task: {e}'

@app.route("/update/<int:id>", methods=['GET', 'POST'])  # Corrected 'method' to 'methods'
def update(id:int):
    task = MyDb.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['task']
        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return f"Error updating task: {e}"
    else:
        return render_template('edit.html', task=task)  # Corrected 'edit.htm' to 'edit.html'

if __name__ =='__main__':
    app.run(debug=True)
    
