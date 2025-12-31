import os
from src import seed
from src.db import engine, Base
from sqlalchemy.orm import Session
from src.models import Activity


def test_seed_creates_activities(tmp_path, monkeypatch):
    # Use a temporary SQLite database
    db_file = tmp_path / "test.db"
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{db_file}")

    # create DB and seed
    Base.metadata.create_all(bind=engine)
    seed.seed()

    # simple assertion: there should be at least one activity
    db = Session(bind=engine)
    try:
        activities = db.query(Activity).all()
        assert len(activities) > 0
    finally:
        db.close()
