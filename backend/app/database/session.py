import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

# Always create engine first (important for Alembic)
engine = create_engine(DATABASE_URL)

# Optional: retry connection when running app container
for i in range(10):
    try:
        connection = engine.connect()
        connection.close()
        print("Database connected successfully")
        break
    except Exception:
        print("Database not ready, retrying...")
        time.sleep(3)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# FastAPI dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
