# db.py
import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

load_dotenv()

db_type = os.getenv('DB_TYPE')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_ip = os.getenv('DB_IP')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
SQLALCHEMY_DATABASE_URL = f"{db_type}://{db_username}:{db_password}@{db_ip}:{db_port}/{db_name}"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a sessionmaker factory, which will be used to create new session instances
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency function to get the DB session
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
