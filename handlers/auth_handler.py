import json
from modules.auth.functions import register_user, login_user

def handler(event, context):
    # Extract path, method, and body from the event
    path = event.get("path")
    method = event.get("httpMethod")
    body = json.loads(event.get("body") or "{}")

    # Handle CORS preflight request
    if method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            },
            "body": ""
        }

    # Route requests to appropriate auth function
    if path == "/auth/register" and method == "POST":
        response = register_user(body)
    elif path == "/auth/login" and method == "POST":
        response = login_user(body)
    else:
        # Return 404 for unknown routes
        response = {
            "statusCode": 404,
            "body": json.dumps({"error": "Route not found"})
        }

    # Ensure CORS headers are always included
    if "headers" not in response:
        response["headers"] = {}
    response["headers"]["Access-Control-Allow-Origin"] = "*"

    return response
