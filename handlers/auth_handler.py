import json
from modules.auth.functions import register_user, login_user

def handler(event, context):
    path = event.get("path")
    method = event.get("httpMethod")
    body = json.loads(event.get("body") or "{}")

    if path == "/auth/register" and method == "POST":
        return register_user(body)
    elif path == "/auth/login" and method == "POST":
        return login_user(body)

    return {
        "statusCode": 404,
        "body": json.dumps({"error": "Route not found"})
    }
