from cerberus import Validator
from datetime import datetime
import re

# Define el esquema Cerberus
user_schema = {
    "email": {
        "type": "string",
        "required": True,
        "regex": r"^[^@]+@[^@]+\.[^@]+$"
    },
    "password": {
        "type": "string",
        "required": True,
        "minlength": 6,
        "check_with": "not_empty"
    },
    "created_at": {
        "type": "datetime",
        "required": False,
        "default_setter": lambda doc: datetime.now()
    }
}

# Agrega una función de validación personalizada
class CustomValidator(Validator):
    def _check_with_not_empty(self, field, value):
        if not value.strip():
            self._error(field, "Password cannot be empty")

# Función para usar la validación
def validate_user(data: dict):
    v = CustomValidator(user_schema)
    if not v.validate(data):
        return False, v.errors
    return True, v.document