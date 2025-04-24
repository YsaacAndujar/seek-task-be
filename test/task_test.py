import json
from handlers.auth_handler import handler as auth_handler
from handlers.task_handler import handler as task_handler

def test_task_crud_flow_authenticated():
    context = {}

    # Step 1: Login and get token
    login_event = {
        "httpMethod": "POST",
        "path": "/auth/login",
        "body": json.dumps({
            "email": "a@gmail.com",
            "password": "123456"
        })
    }
    login_response = auth_handler(login_event, context)
    assert login_response["statusCode"] == 200
    token = json.loads(login_response["body"])["token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 2: Create a new task
    create_event = {
        "httpMethod": "POST",
        "path": "/tasks",
        "body": json.dumps({
            "title": "Test CRUD Task",
            "description": "Task created during test",
            "status": "todo"
        }),
        "headers": headers
    }
    create_response = task_handler(create_event, context)
    assert create_response["statusCode"] == 201
    task_id = json.loads(create_response["body"])["task_id"]

    # Step 3: Get task by ID
    get_by_id_event = {
        "httpMethod": "GET",
        "path": f"/tasks/{task_id}",
        "pathParameters": {"id": task_id},
        "headers": headers
    }
    get_response = task_handler(get_by_id_event, context)
    assert get_response["statusCode"] == 200

    # Step 4: Update task
    update_event = {
        "httpMethod": "PUT",
        "path": f"/tasks/{task_id}",
        "pathParameters": {"id": task_id},
        "body": json.dumps({
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "in_progress"
        }),
        "headers": headers
    }
    update_response = task_handler(update_event, context)
    assert update_response["statusCode"] == 200

    # Step 5: Verify task was updated
    get_updated_response = task_handler(get_by_id_event, context)
    updated_data = json.loads(get_updated_response["body"])
    assert updated_data["title"] == "Updated Task Title"

    # Step 6: Get all tasks with pagination
    get_all_event = {
        "httpMethod": "GET",
        "path": "/tasks",
        "queryStringParameters": {"page": "1", "limit": "5"},
        "headers": headers
    }
    get_all_response = task_handler(get_all_event, context)
    assert get_all_response["statusCode"] == 200

    # Step 7: Get task stats
    stats_event = {
        "httpMethod": "GET",
        "path": "/tasks/stats",
        "headers": headers
    }
    stats_response = task_handler(stats_event, context)
    assert stats_response["statusCode"] == 200

    # Step 8: Delete the task
    delete_event = {
        "httpMethod": "DELETE",
        "path": f"/tasks/{task_id}",
        "pathParameters": {"id": task_id},
        "headers": headers
    }
    delete_response = task_handler(delete_event, context)
    assert delete_response["statusCode"] == 200

    # Step 9: Confirm deletion
    get_deleted = task_handler(get_by_id_event, context)
    assert get_deleted["statusCode"] == 404
