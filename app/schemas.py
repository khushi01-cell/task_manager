# schemas.py
"""
Pydantic schemas for request and response validation.

These schemas define:
- The structure of request/response bodies
- Data validation rules
- Serialization/deserialization behavior
"""

from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    """Base schema for task-related operations."""
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass

class TaskUpdate(BaseModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = None
    description: Optional[str] = None

class TaskOut(TaskBase):
    """Schema for returning task data (includes ID and owner)."""
    id: int
    owner_id: int
    
    class Config:
        # Enable ORM mode to work with SQLAlchemy models
        from_attributes = True

class UserCreate(BaseModel):
    """Schema for user signup (username and password)."""
    username: str
    password: str

class UserOut(BaseModel):
    """Schema for returning user data (excludes password)."""
    id: int
    username: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str