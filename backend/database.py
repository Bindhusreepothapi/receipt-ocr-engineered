"""
Database Configuration.

Handles the connection to the SQLite database and provides
a session dependency for FastAPI routes.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use a local SQLite file for development
SQLALCHEMY_DATABASE_URL = "sqlite:///./receipts.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """
    Dependency that provides a database session.
    FastAPI will call this function for each request that needs DB access.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        