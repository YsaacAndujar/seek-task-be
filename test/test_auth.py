import json
from handlers.auth_handler import handler

# def test_register_user_success():
#     event = {
#         "httpMethod": "POST",
#         "path": "/auth/register",
#         "body": json.dumps({
#             "email": "test@example.com",
#             "password": "123456",
#             "confirm_password": "123456"
#         })
#     }

#     context = {}
#     response = handler(event, context)
#     print(response)
#     assert response["statusCode"] == 201
#     assert "User registered successfully" in response["body"]

def test_register_user_success():
    event = {
        "httpMethod": "POST",
        "path": "/auth/login",
        "body": json.dumps({
            "email": "test@example.com",
            "password": "123456",
        })
    }

    context = {}
    response = handler(event, context)
    print(response)
    assert response["statusCode"] == 200
    assert "User registered successfully" in response["body"]