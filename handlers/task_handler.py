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

# Formats standard HTTP response with CORS headers
def base_response(status_code, body=None, headers=None):
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            **(headers or {})
        },
        "body": json.dumps(body) if body else ""
    }

@require_auth  # Ensures the request is authenticated
def handler(event, context):
    path = event.get("path") or ""
    method = event.get("httpMethod")
    body = json.loads(event.get("body") or "{}")
    path_params = event.get("pathParameters") or {}
    query_params = event.get("queryStringParameters") or {}

    # Handle CORS preflight request
    if method == "OPTIONS":
        return base_response(200, headers={
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        })

    try:
        # Task creation
        if path == "/tasks" and method == "POST":
            return add_cors(create_task(body))
        # Retrieve task statistics
        elif path == "/tasks/stats" and method == "GET":
            return add_cors(get_task_stats())
        # Retrieve all tasks
        elif path == "/tasks" and method == "GET":
            return add_cors(get_tasks(query_params))
        # Retrieve a single task by ID
        elif path.startswith("/tasks/") and method == "GET" and "id" in path_params:
            return add_cors(get_task_by_id(path_params["id"]))
        # Update a task by ID
        elif path.startswith("/tasks/") and method == "PUT" and "id" in path_params:
            return add_cors(update_task(path_params["id"], body))
        # Delete a task by ID
        elif path.startswith("/tasks/") and method == "DELETE" and "id" in path_params:
            return add_cors(delete_task(path_params["id"]))
    except Exception as e:
        # Return internal server error with exception message
        return base_response(500, {"error": str(e)})

    # Return not found for unhandled routes
    return base_response(404, {"error": "Route not found"})

# Adds CORS headers to an existing response
def add_cors(response):
    """Adds CORS header to existing function response."""
    if "headers" not in response:
        response["headers"] = {}
    response["headers"]["Access-Control-Allow-Origin"] = "*"
    return response
