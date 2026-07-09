"""
database.py - The Pipe connecting our app to the database file.
This will create a file called 'skin_cancer.db' in your backend folder.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Tell it to use SQLite and name the file
SQLALCHEMY_DATABASE_URL = "sqlite:///./skin_cancer.db"

# Create the engine (the motor that drives the pipe)
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a SessionLocal (every time a user does something, we open a 'session', do the work, and close it)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class (our table blueprints will inherit from this)
Base = declarative_base()