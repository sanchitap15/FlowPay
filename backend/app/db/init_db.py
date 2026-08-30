"""
Run this once to create tables:
    python -m app.db.init_db
"""
from app.core.database import Base, engine
from app.models import domain  # noqa: F401 — import registers models with Base.metadata


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    print("FlowPay tables created (or already existed).")


if __name__ == "__main__":
    init_db()
