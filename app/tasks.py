# tasks.py
"""
Additional task route for filtered task retrieval.

Note: This module appears to have a location filter that isn't
implemented in the main Task model. Would need to add a 'location'
field to the Task model for this to work.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .models import Task
from .database import get_db

router = APIRouter()

@router.get("/tasks")
def get_tasks(
        local_kw: str = Query(..., description="Keyword to filter task location"),
        db: Session = Depends(get_db)
):
    """
    Get tasks filtered by location keyword.
    
    Note: Currently won't work as Task model lacks 'location' field.
    
    Args:
        local_kw: The keyword to filter tasks by location.
    
    Returns:
        List of matching tasks.
    """
    tasks = db.query(Task).filter(Task.location.contains(local_kw)).all()
    return tasks