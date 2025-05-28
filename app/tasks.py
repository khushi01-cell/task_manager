from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .models import Task  # ensure correct import
from .database import get_db  # your get_db from earlier

router = APIRouter()

@router.get("/tasks")
def get_tasks(
    local_kw: str = Query(..., description="Keyword to filter task location"),
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).filter(Task.location.contains(local_kw)).all()
    return tasks
