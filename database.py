# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
# For development, we'll use SQLite. For production, you can use PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kpa_forms.db")

# For PostgreSQL, use this format:
# DATABASE_URL = "postgresql://username:password@localhost/dbname"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
