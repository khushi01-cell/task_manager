# crud.py
"""
CRUD operations for users and tasks.

This module contains all database operations following the
Create, Read, Update, Delete (CRUD) pattern.
"""

from sqlalchemy.orm import Session
from app import models, schemas, auth

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user with hashed password."""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """Authenticate a user by verifying credentials."""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        return None
    return user

def create_task(db: Session, task: schemas.TaskCreate, user_id: int):
    """Create a task for the given user."""
    db_task = models.Task(**task.dict(), owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task_by_id(db: Session, task_id: int):
    """Fetch a task by its ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, db_task: models.Task, task_update: schemas.TaskUpdate):
    """Update the fields of an existing task."""
    for key, value in task_update.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, db_task: models.Task):
    """Delete a task from the database."""
    db.delete(db_task)
    db.commit()

def get_tasks(db: Session, user_id: int):
    """Retrieve all tasks for a specific user."""
    return db.query(models.Task).filter(models.Task.owner_id == user_id).all()

def get_all_tasks(db: Session):
    """Retrieve all tasks from the database (admin/debugging use)."""
    return db.query(models.Task).all()