from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

class TaskModel(BaseModel):
    title: str
    description: Optional[str]
    status: Literal["todo", "in_progress", "done"] = "todo"
    created_at: datetime = Field(default_factory=datetime.now)