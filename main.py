# main.py
from fastapi import FastAPI
from app import routes, models, database
from app.database import engine

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(routes.router)