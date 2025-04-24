import jwt
import os
from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus

JWT_ALGORITHM = "HS256"

def create_access_token(data: dict) -> str:
    JWT_SECRET = os.environ.get("JWT_SECRET")
    payload = data.copy()
    expire = datetime.now() + timedelta(days=30)
    payload["exp"] = expire
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def decode_access_token(token: str) -> dict:
    JWT_SECRET = os.environ.get("JWT_SECRET")
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])

def require_auth(func):
    @wraps(func)
    def wrapper(event, context):
        headers = event.get("headers", {})
        auth_header = headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return {
                "statusCode": HTTPStatus.UNAUTHORIZED,
                "body": "Missing or invalid Authorization header"
            }

        token = auth_header.split(" ")[1]
        try:
            user = decode_access_token(token)
            event["user"] = user  # Pasamos el usuario decodificado al handler
        except Exception as e:
            return {
                "statusCode": HTTPStatus.UNAUTHORIZED,
                "body": f"Invalid token: {str(e)}"
            }

        return func(event, context)
    return wrapper