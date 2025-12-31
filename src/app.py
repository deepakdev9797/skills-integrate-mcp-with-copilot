"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

from fastapi import Depends
from sqlalchemy.orm import Session
from .db import engine, Base, get_db
from .models import Activity, Participant


# Ensure tables exist and optionally seed in development
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)


def activity_to_dict(activity: Activity):
    return {
        "name": activity.name,
        "description": activity.description,
        "schedule": activity.schedule,
        "max_participants": activity.max_participants,
        "participants": [p.email for p in activity.participants],
    }


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities(db: Session = Depends(get_db)):
    all_activities = db.query(Activity).all()
    return {a.name: activity_to_dict(a) for a in all_activities}


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Sign up a student for an activity"""
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Check if participant exists, create if necessary
    participant = db.query(Participant).filter(Participant.email == email).first()
    if participant and participant in activity.participants:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    if activity.max_participants is not None and len(activity.participants) >= activity.max_participants:
        raise HTTPException(status_code=400, detail="Activity is already full")

    if not participant:
        participant = Participant(email=email)
        db.add(participant)
        db.flush()

    activity.participants.append(participant)
    db.add(activity)
    db.commit()
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/unregister")
def unregister_from_activity(activity_name: str, email: str, db: Session = Depends(get_db)):
    """Unregister a student from an activity"""
    activity = db.query(Activity).filter(Activity.name == activity_name).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    participant = db.query(Participant).filter(Participant.email == email).first()
    if not participant or participant not in activity.participants:
        raise HTTPException(status_code=400, detail="Student is not signed up for this activity")

    activity.participants.remove(participant)
    db.add(activity)
    db.commit()
    return {"message": f"Unregistered {email} from {activity_name}"}
