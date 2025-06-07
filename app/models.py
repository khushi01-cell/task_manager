# models.py
"""
SQLAlchemy models for user and task tables.

Defines the database schema and relationships between tables.
"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """User model with one-to-many relationship to tasks."""
    __tablename__ = "users1"  # Table name
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)  # Unique username
    hashed_password = Column(String)  # Hashed password storage
    
    # Relationship to tasks (one user can have many tasks)
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    """Task model belonging to a user."""
    __tablename__ = "tasks"  # Table name
    
    # Columns
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)  # Task title
    description = Column(String)  # Task description
    owner_id = Column(Integer, ForeignKey("users1.id"))  # Foreign key to user
    
    # Relationship to user (many tasks can belong to one user)
    owner = relationship("User", back_populates="tasks")