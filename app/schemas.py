from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str

class UserCreate(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass

class TaskOut(TaskBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True
