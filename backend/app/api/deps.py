from typing import Generator
from app.core.database import SessionLocal

def get_db() -> Generator:
    """
    Dependency that yields a database session per request and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

