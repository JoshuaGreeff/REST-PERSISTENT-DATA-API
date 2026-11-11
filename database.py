"""Set up the SQLite database engine and sessions for the clinical API."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# This defaults to the assignment database file but can be changed during tests.
DATABASE_URL = os.getenv("CLINICAL_DATABASE_URL", "sqlite:///./clinical_data.db")

# check_same_thread is required when Flask and SQLite use the same local database file.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
