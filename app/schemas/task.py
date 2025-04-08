from pydantic import BaseModel, Field, field_validator
from enum import Enum
from typing import Optional

class TaskStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TaskStatus = Field(default=TaskStatus.TODO)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value):
        if "  " in value:
            raise ValueError("Title cannot contain double spaces")
        return value.strip()

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: Optional[TaskStatus] = None

class Task(TaskBase):
    id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Initial setup",
                "description": "Project configuration",
                "status": "todo"
            }
        }
