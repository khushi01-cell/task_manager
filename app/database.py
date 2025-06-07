# database.py
"""
Database connection and session management.

This module handles:
- Database engine creation
- Session management
- Connection pooling
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine with connection pooling
engine = create_engine(DATABASE_URL)

# Session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative model definitions
Base = declarative_base()

def get_db():
    """
    Provide a database session for dependency injection.
    
    Yields:
        SQLAlchemy database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()