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

@require_auth
def handler(event, context):
    path = event.get("path") or ""
    method = event.get("httpMethod")
    body = json.loads(event.get("body") or "{}")
    path_params = event.get("pathParameters") or {}
    query_params = event.get("queryStringParameters") or {}

    if path == "/tasks" and method == "POST":
        return create_task(body)
    elif path == "/tasks/stats" and method == "GET":
        return get_task_stats()
    
    elif path == "/tasks" and method == "GET":
        return get_tasks(query_params)

    elif path.startswith("/tasks/") and method == "GET" and "id" in path_params:
        return get_task_by_id(path_params["id"])

    elif path.startswith("/tasks/") and method == "PUT" and "id" in path_params:
        return update_task(path_params["id"], body)

    elif path.startswith("/tasks/") and method == "DELETE" and "id" in path_params:
        return delete_task(path_params["id"])

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Route not found"})
    }
