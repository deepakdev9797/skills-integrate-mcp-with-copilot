"""Seed the database with initial activities and participants"""
from sqlalchemy.orm import Session
from .db import engine, Base, SessionLocal
from .models import Activity, Participant


def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if db.query(Activity).count() > 0:
            print("Database already seeded")
            return

        activities = [
            {
                "name": "Chess Club",
                "description": "Learn strategies and compete in chess tournaments",
                "schedule": "Fridays, 3:30 PM - 5:00 PM",
                "max_participants": 12,
                "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
            },
            {
                "name": "Programming Class",
                "description": "Learn programming fundamentals and build software projects",
                "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
                "max_participants": 20,
                "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
            },
            {
                "name": "Gym Class",
                "description": "Physical education and sports activities",
                "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
                "max_participants": 30,
                "participants": ["john@mergington.edu", "olivia@mergington.edu"],
            },
        ]

        for a in activities:
            act = Activity(name=a["name"], description=a["description"], schedule=a["schedule"], max_participants=a["max_participants"])
            db.add(act)
            db.flush()
            for email in a["participants"]:
                participant = db.query(Participant).filter_by(email=email).first()
                if not participant:
                    participant = Participant(email=email)
                    db.add(participant)
                    db.flush()
                act.participants.append(participant)
        db.commit()
        print("Seeded database")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
