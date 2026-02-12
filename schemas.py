from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TodoPostSchema(BaseModel):
    title: str
    description: str = ""

    model_config = ConfigDict(extra="forbid")


class TodoGetSchema(TodoPostSchema):
    id: int
    created_at: datetime
    is_completed: bool = False


class TodoUpdateSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    is_completed: bool = False

    model_config = ConfigDict(extra="forbid")
