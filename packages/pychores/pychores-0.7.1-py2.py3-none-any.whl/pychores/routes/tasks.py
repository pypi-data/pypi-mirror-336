from flask import Blueprint, current_app, jsonify, request, session, url_for
from flask_cors import CORS

from pychores.adapter.repository.sqla.task import TaskRepo
from pychores.domain.use_cases.delete_task import DeleteTask
from pychores.domain.use_cases.get_task import GetTask
from pychores.routes.auth import require_auth

from .. import respond_success

bp = Blueprint("tasks", __name__, url_prefix="/api")

CORS(bp, resources={r"/*": {"origins": "*"}})


def serialize_task(task):
    return {
        "id": task.id,
        "chore_id": task.chore.id,
        "chore_name": task.chore.name,
        "execution_date": task.execution_date,
    }


def respond_task(task):
    response = jsonify(serialize_task(task))
    response.headers["Location"] = url_for("tasks.task", task_id=task.id)
    return response


@bp.route("/task/<int:task_id>", methods=["GET", "DELETE"])
@require_auth(None)
def task(task_id):
    username = session.get("username")
    if request.method == "DELETE":
        uc = DeleteTask(TaskRepo(current_app.db_session))
        uc.execute(username, task_id)
        return "", 204
    # get
    uc = GetTask(TaskRepo(current_app.db_session))
    task = uc.execute(username=username, task_id=task_id)
    return respond_success("task", serialize_task(task))
