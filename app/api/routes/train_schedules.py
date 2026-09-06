from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime

from app.core.database import get_db
from app.models.train_schedule import TrainSchedule


router = APIRouter(
    prefix="/train-schedules",
    tags=["Train Schedules"]
)


# CREATE TRAIN SCHEDULE
@router.post("/")
def create_train_schedule(
    train_id: int,
    service_date: date,
    scheduled_departure: datetime = None,
    scheduled_arrival: datetime = None,
    actual_departure: datetime = None,
    actual_arrival: datetime = None,
    status: str = "SCHEDULED",
    delay_minutes: int = 0,
    db: Session = Depends(get_db)
):
    schedule = TrainSchedule(
        train_id=train_id,
        service_date=service_date,
        scheduled_departure=scheduled_departure,
        scheduled_arrival=scheduled_arrival,
        actual_departure=actual_departure,
        actual_arrival=actual_arrival,
        status=status,
        delay_minutes=delay_minutes
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


# GET ALL TRAIN SCHEDULES
@router.get("/")
def get_train_schedules(
    db: Session = Depends(get_db)
):
    return db.query(TrainSchedule).all()


# GET ONE TRAIN SCHEDULE
@router.get("/{schedule_id}")
def get_train_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    schedule = (
        db.query(TrainSchedule)
        .filter(TrainSchedule.id == schedule_id)
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Train schedule not found"
        )

    return schedule


# DELETE TRAIN SCHEDULE
@router.delete("/{schedule_id}")
def delete_train_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    schedule = (
        db.query(TrainSchedule)
        .filter(TrainSchedule.id == schedule_id)
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Train schedule not found"
        )

    db.delete(schedule)
    db.commit()

    return {
        "message": "Train schedule deleted successfully"
    }