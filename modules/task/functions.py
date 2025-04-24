from db.db import get_database
from datetime import datetime
from bson.objectid import ObjectId
import json
from collections import defaultdict
from bson import json_util
from modules.task.models import validate_task

def create_task(body: dict):
    valid, result = validate_task(body)
    if not valid:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": result})
        }

    db = get_database()
    tasks = db["tasks"]

    result = tasks.insert_one(result)
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
        if "created_at" in task and isinstance(task["created_at"], datetime):
            task["created_at"] = task["created_at"].isoformat()
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

def get_task_stats():
    db = get_database()
    tasks_collection = db["tasks"]

    status_counts = defaultdict(int)

    for task in tasks_collection.find({}, {"status": 1}):
        status = task.get("status", "todo") 
        status_counts[status] += 1

    stats = [{"status": status, "count": count} for status, count in status_counts.items()]

    return {
        "statusCode": 200,
        "body": json.dumps(stats, default=json_util.default),
        "headers": {
            "Content-Type": "application/json"
        }
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

    task["id"] = str(task["_id"])
    del task["_id"]

    if "created_at" in task and isinstance(task["created_at"], datetime):
        task["created_at"] = task["created_at"].isoformat()

    return {
        "statusCode": 200,
        "body": json.dumps(task)
    }
