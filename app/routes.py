from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import schemas, crud, auth, database, models
from app.database import get_db

router = APIRouter()

@router.post("/signup", response_model=schemas.UserOut)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(auth.models.User).filter(auth.models.User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")
        return crud.create_user(db, user)
    except Exception as e:
        print(f"Error during signup: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Signup endpoint called")

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = crud.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        token = auth.create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print(f"Error during login: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Login endpoint called")

@router.post("/tasks", response_model=schemas.TaskOut)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    try:
        return crud.create_task(db, task, current_user.id)
    except Exception as e:
        print(f"Error creating task: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Create task endpoint called")

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int = Path(..., description="ID of the task to update"), task_update: schemas.TaskUpdate = Depends(), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    try:
        task = crud.get_task_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")
        return crud.update_task(db, task, task_update)
    except Exception as e:
        print(f"Error updating task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Update task endpoint called")

@router.delete("/tasks/{task_id}", response_model=dict)
def delete_task(task_id: int = Path(..., description="ID of the task to delete"), db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    try:
        task = crud.get_task_by_id(db, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.owner_id != current_user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")
        crud.delete_task(db, task)
        return {"detail": "Task deleted successfully"}
    except Exception as e:
        print(f"Error deleting task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Delete task endpoint called")

@router.get("/tasks/all", response_model=list[schemas.TaskOut])
def get_all_tasks(db: Session = Depends(get_db)):
    try:
        return crud.get_all_tasks(db)
    except Exception as e:
        print(f"Error fetching all tasks: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    finally:
        print("Get all tasks endpoint called")
