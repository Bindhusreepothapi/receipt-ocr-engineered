"""
Database Models.

Defines the structure of our data using SQLAlchemy ORM.
This allows us to interact with the database using Python objects
instead of writing raw SQL queries.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Receipt(Base):
    """Represents a single processed receipt in the database."""
    
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, index=True)
    merchant = Column(String, index=True)
    date = Column(String)
    total = Column(Float)
    items = Column(String)  # Storing as JSON string for simplicity in this milestone
    uploaded_at = Column(DateTime, default=datetime.utcnow)