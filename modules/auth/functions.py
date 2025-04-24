import json
from db.db import get_database
from modules.auth.models import validate_user
from utils.hash import hash_password, verify_password
from datetime import datetime
from utils.token import create_access_token

def register_user(body: dict):
    # Validate user input using Pydantic or custom schema
    valid, result = validate_user(body)

    if not valid:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": result})
        }

    db = get_database()
    users = db["users"]

    # Check for duplicate email
    if users.find_one({"email": result["email"]}):
        return {
            "statusCode": 400,
            "body": json.dumps({'message':"Email is already registered"})
        }

    # Hash the password before storing
    hashed_password = hash_password(result["password"])
    insert_result = users.insert_one({
        "email": result["email"],
        "password": hashed_password,
        "created_at": result.get("created_at", datetime.utcnow())
    })

    user_id = str(insert_result.inserted_id)
    # Generate JWT token for the new user
    token = create_access_token({"user_id": user_id})

    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "User registered successfully",
            "token": token
        })
    }

def login_user(body: dict):
    db = get_database()
    users = db["users"]

    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return {"statusCode": 400, "body": json.dumps({"message": "Email and password are required"})}

    # Attempt to find user and verify credentials
    user = users.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return {"statusCode": 400, "body": json.dumps({"message": "Invalid credentials"})}

    # Generate token on successful login
    token = create_access_token({"user_id": str(user["_id"])})

    return {
        "statusCode": 200,
        "body": json.dumps({"token": token})
    }
