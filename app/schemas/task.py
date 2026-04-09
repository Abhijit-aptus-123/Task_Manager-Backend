from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    status: str = "todo"
    assigned_user_id: int | None = None

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None