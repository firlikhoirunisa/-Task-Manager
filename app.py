from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

class Task:
    def __init__(self, id, title, description, priority='medium', status='pending'):
        self.id = id
        self.title = title
        self.description = description
        self.priority = priority
        self.status = status
        self.created_at = datetime.now().strftime("%Y-%m-%d")

class User:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.task_id_counter = 1

    def add_task(self, title, description, priority):
        task = Task(self.task_id_counter, title, description, priority)
        self.tasks.append(task)
        self.task_id_counter += 1
        return task

    def remove_task(self, id):
        self.tasks = [task for task in self.tasks if task.id != id]

    def get_tasks_by_status(self, status):
        return [task for task in self.tasks if task.status == status]

user = User("User ")

@app.route('/')
def index():
    return render_template('index.html', tasks=user.tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    title = request.form['title']
    description = request.form['description']
    priority = request.form['priority']
    if title:
        user.add_task(title, description, priority)
    return redirect(url_for('index'))

@app.route('/toggle_status/<int:task_id>')
def toggle_status(task_id):
    task = next((t for t in user.tasks if t.id == task_id), None)
    if task:
        task.status = 'completed' if task.status == 'pending' else 'pending'
    return redirect(url_for('index'))

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    user.remove_task(task_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
