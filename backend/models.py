"""
models.py - The Blueprints for our Database Tables.
Think of this like defining the columns in an Excel spreadsheet.
"""
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users" # Name of the table in the database

    id = Column(String, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False) # unique means no two users can have same email
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False) # We NEVER save plain text passwords
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    scans_count = Column(Integer, default=0)


class Analysis(Base):
    __tablename__ = "analysis_history" # Name of the table for scans

    id = Column(String, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.email"), nullable=False) # Connects this scan to the user who did it
    prediction = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    image_filename = Column(String, nullable=False)
    analyzed_at = Column(DateTime(timezone=True), server_default=func.now())