import jwt
import os
from datetime import datetime, timedelta

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
