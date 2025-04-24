import json
from handlers.auth_handler import handler as auth_handler
from handlers.task_handler import handler as task_handler

def handler(event, context):
    path = event.get("path", "")
    
    if path.startswith("/auth"):
        return auth_handler(event, context)
    elif path.startswith("/tasks"):
        return task_handler(event, context)

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Route not found"})
    }