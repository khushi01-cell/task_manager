# main.py
"""
FastAPI app entry point.

Initializes database models and includes all routes.
"""

from fastapi import FastAPI
from app import routes, models, database
from app.database import engine

# Create database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

# Create FastAPI application instance
app = FastAPI()

# Register routers
app.include_router(routes.router)