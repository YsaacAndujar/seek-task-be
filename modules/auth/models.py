from pydantic import EmailStr, BaseModel, field_validator
from datetime import datetime

class UserModel(BaseModel):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

    @field_validator("password")
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password is required")
        if len(value) < 6:
            raise ValueError("Password should have at least ")
        return value