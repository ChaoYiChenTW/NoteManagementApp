import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_db_connection():
    try:
        # Connect to the database
        with engine.connect() as connection:
            # Execute a simple query, such as checking the current time
            result = connection.execute(text("SELECT 1")).fetchone()
            print("Connection successful, result:", result)
    except Exception as e:
        print("Connection failed:", str(e))


if __name__ == "__main__":
    test_db_connection()
