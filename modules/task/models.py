from cerberus import Validator
from datetime import datetime

task_schema = {
    "title": {"type": "string", "required": True},
    "description": {"type": "string", "required": False, "nullable": True},
    "status": {
        "type": "string",
        "allowed": ["todo", "in_progress", "done"],
        "default": "todo"
    },
    "created_at": {
        "type": "datetime",
        "required": False,
        "default_setter": lambda doc: datetime.now()
    }
}

def validate_task(data: dict):
    v = Validator(task_schema)
    if not v.validate(data):
        return False, v.errors
    return True, v.document
