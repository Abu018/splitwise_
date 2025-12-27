# init_db.py
import os
import sys
from sqlalchemy import create_engine

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.db import Base, engine
from app.models.user import User

def init_db():
    # Create all tables
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    print(f"Database location: {os.path.abspath('splitwise.db')}")

if __name__ == "__main__":
    init_db()