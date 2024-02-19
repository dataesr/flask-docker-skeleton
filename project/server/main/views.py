import os
import requests
import redis

from flask import Blueprint, current_app, jsonify, render_template, request
from rq import Connection, Queue
from project.server.main.tasks import create_task_compute
from mycode.cordis import check_cordis
from project.server.main.logger import get_logger

default_timeout = 4320000

logger = get_logger(__name__)

main_blueprint = Blueprint(
    "main",
    __name__,
)


@main_blueprint.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@main_blueprint.route("/compute", methods=["POST"])
def run_task_compute():
    args = request.get_json(force=True)

    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue(name="sandbox", default_timeout=default_timeout)
        task = q.enqueue(create_task_compute, args)
    response_object = {"status": "success", "data": {"task_id": task.get_id()}}
    return jsonify(response_object), 202

@main_blueprint.route("/check_cordis", methods=["POST"])
def run_task_check_cordus():
    args = request.get_json(force=True)
    projects_ids =args.get('projects')
    assert(isinstance(projects_ids, list))
    suffixes = {}
    for p in projects_ids:
        if isinstance(p, str) and len(p)>0:
            suffix = p[-2:]
            if suffix not in suffixes:
                suffixes[suffix]=[]
            suffixes[suffix].append(p)
    for suffix in suffixes:
        current_args = {"projects": suffixes[suffix], "suffix": suffix}
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue(name="sandbox", default_timeout=default_timeout)
            task = q.enqueue(check_cordis, current_args)
    response_object = {"status": "success", "data": {"task_id": task.get_id()}}
    return jsonify(response_object), 202


@main_blueprint.route("/tasks/<task_id>", methods=["GET"])
def get_status(task_id):
    with Connection(redis.from_url(current_app.config["REDIS_URL"])):
        q = Queue("sandbox")
        task = q.fetch_job(task_id)
    if task:
        response_object = {
            "status": "success",
            "data": {
                "task_id": task.get_id(),
                "task_status": task.get_status(),
                "task_result": task.result,
            },
        }
    else:
        response_object = {"status": "error"}
    return jsonify(response_object)
