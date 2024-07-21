from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import os

# SQLite configuration
db_path = os.getenv("DB_PATH", "/code/db.sqlite")

# Connection string for SQLite
connectionString = f"sqlite:///{db_path}"

# SQLAlchemy setup
engine = create_engine(connectionString, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
