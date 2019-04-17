from flask import Flask
from flask import url_for, jsonify
from worker import celery
import celery.states as states
from itertools import chain
from celery.task.control import inspect
i = inspect()
i.registered_tasks()

app = Flask(__name__)


@app.route('/tasks')
def get_all_taks() -> str:
    return str(set(chain.from_iterable( i.registered_tasks().values() )))


@app.route('/add/<int:param1>/<int:param2>')
def add(param1: int, param2: int) -> str:
    task = celery.send_task('tasks.super_add_task', args=[param1, param2], kwargs={})
    response = f"<a href='{url_for('check_task', task_id=task.id, external=True)}'>check status of {task.id} </a>"
    return response


@app.route('/check/<string:task_id>')
def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)