from db.db import get_database
from datetime import datetime
from bson.objectid import ObjectId
import json

from modules.task.models import TaskModel

def create_task(body: dict):
    try:
        task = TaskModel(**body)
    except Exception as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Validation error: {str(e)}"})
        }

    db = get_database()
    tasks = db["tasks"]

    result = tasks.insert_one(task.dict())
    return {
        "statusCode": 201,
        "body": json.dumps({
            "message": "Task created successfully",
            "task_id": str(result.inserted_id)
        })
    }

def get_tasks(query_params: dict):
    db = get_database()
    tasks_collection = db["tasks"]

    try:
        page = int(query_params.get("page", 1))
        limit = int(query_params.get("limit", 10))
        skip = (page - 1) * limit
    except ValueError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid pagination parameters"})
        }

    total = tasks_collection.count_documents({})
    cursor = tasks_collection.find().skip(skip).limit(limit)

    tasks = []
    for task in cursor:
        task["_id"] = str(task["_id"])
        tasks.append(task)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "data": tasks,
            "pagination": {
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": (total + limit - 1) // limit
            }
        })
    }

def delete_task(task_id: str):
    db = get_database()
    tasks = db["tasks"]

    try:
        obj_id = ObjectId(task_id)
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid task ID"})
        }

    result = tasks.delete_one({"_id": obj_id})

    if result.deleted_count == 0:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Task not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Task deleted successfully"})
    }

def update_task(task_id: str, body: dict):
    db = get_database()
    tasks = db["tasks"]

    try:
        obj_id = ObjectId(task_id)
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid task ID"})
        }

    result = tasks.update_one({"_id": obj_id}, {"$set": body})

    if result.matched_count == 0:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Task not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Task updated successfully"})
    }

def get_task_by_id(task_id: str):
    db = get_database()
    tasks = db["tasks"]

    try:
        obj_id = ObjectId(task_id)
    except Exception:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Invalid task ID"})
        }

    task = tasks.find_one({"_id": obj_id})
    if not task:
        return {
            "statusCode": 404,
            "body": json.dumps({"error": "Task not found"})
        }

    task["_id"] = str(task["_id"])  # Convertir ObjectId a string
    return {
        "statusCode": 200,
        "body": json.dumps(task)
    }
