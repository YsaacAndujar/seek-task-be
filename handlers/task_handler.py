import json
from modules.task.functions import (
    create_task,
    get_task_stats,
    get_tasks,
    get_task_by_id,
    update_task,
    delete_task
)
from utils.token import require_auth

def base_response(status_code, body=None, headers=None):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            **(headers or {})
        },
        "body": json.dumps(body) if body else ""
    }

@require_auth
def handler(event, context):
    path = event.get("path") or ""
    method = event.get("httpMethod")
    body = json.loads(event.get("body") or "{}")
    path_params = event.get("pathParameters") or {}
    query_params = event.get("queryStringParameters") or {}

    if method == "OPTIONS":
        return base_response(200, headers={
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        })

    try:
        if path == "/tasks" and method == "POST":
            return add_cors(create_task(body))
        elif path == "/tasks/stats" and method == "GET":
            return add_cors(get_task_stats())
        elif path == "/tasks" and method == "GET":
            return add_cors(get_tasks(query_params))
        elif path.startswith("/tasks/") and method == "GET" and "id" in path_params:
            return add_cors(get_task_by_id(path_params["id"]))
        elif path.startswith("/tasks/") and method == "PUT" and "id" in path_params:
            return add_cors(update_task(path_params["id"], body))
        elif path.startswith("/tasks/") and method == "DELETE" and "id" in path_params:
            return add_cors(delete_task(path_params["id"]))
    except Exception as e:
        return base_response(500, {"error": str(e)})

    return base_response(404, {"error": "Route not found"})

def add_cors(response):
    """Agrega encabezado CORS a respuestas de funciones existentes."""
    if "headers" not in response:
        response["headers"] = {}
    response["headers"]["Access-Control-Allow-Origin"] = "*"
    return response
