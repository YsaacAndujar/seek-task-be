import json
import jwt
import os
from datetime import datetime, timedelta
from http import HTTPStatus

JWT_ALGORITHM = "HS256"

# Generates a JWT access token with a 30-day expiration
def create_access_token(data: dict) -> str:
    JWT_SECRET = os.environ.get("JWT_SECRET")
    payload = data.copy()
    expire = datetime.now() + timedelta(days=30)
    payload["exp"] = expire
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# Decodes and verifies a JWT access token
def decode_access_token(token: str) -> dict:
    JWT_SECRET = os.environ.get("JWT_SECRET")
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

# Decorator to enforce authentication via JWT in handler functions
def require_auth(func):
    def wrapper(event, context):
        method = event.get("httpMethod")

        # Allow CORS preflight through
        if method == "OPTIONS":
            return func(event, context)

        headers = event.get("headers") or {}
        auth_header = headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "statusCode": 401,
                "headers": {
                    "Access-Control-Allow-Origin": "*",
                },
                "body": json.dumps({"message": "Unauthorized: No token provided"})
            }

        token = auth_header.split(" ")[1]

        try:
            # Validate token and attach user data to event
            user = decode_access_token(token)
            event["user"] = user 
        except Exception as e:
            return {
                "statusCode": HTTPStatus.UNAUTHORIZED,
                "body": f"Invalid token: {str(e)}"
            }

        return func(event, context)

    return wrapper
