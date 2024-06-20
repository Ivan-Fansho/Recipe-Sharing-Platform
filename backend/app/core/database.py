import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import psycopg2  # for reqs file
from sqlalchemy.sql import text

# Database configuration from environment variables
db_username = os.getenv("DB_USERNAME", "postgres")
db_password = os.getenv("DB_PASSWORD", "master")
db_url = os.getenv("DB_URL", "127.0.0.1:5432")
db_name = os.getenv("DB_NAME", "recipe_db")

def create_database_if_not_exists():
    conn = psycopg2.connect(
        dbname='postgres',
        user=db_username,
        password=db_password,
        host=db_url.split(':')[0],
        port=db_url.split(':')[1]
    )
    conn.autocommit = True  # Ensure autocommit is enabled
    cursor = conn.cursor()
    cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {db_name}")
    cursor.close()
    conn.close()
        
create_database_if_not_exists()

# Connection string for the actual database
connectionString = f"postgresql+psycopg2://{db_username}:{db_password}@{db_url}/{db_name}"

# SQLAlchemy setup
engine = create_engine(connectionString, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
