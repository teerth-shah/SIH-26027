from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.train import Train
from app.models.station import Station
from app.models.rake import Rake
from app.models.locomotive import Locomotive


router = APIRouter(
    prefix="/trains",
    tags=["Trains"]
)


# CREATE TRAIN
@router.post("/")
def create_train(
    train_number: str,
    origin_station_id: int,
    destination_station_id: int,
    train_name: str = None,
    train_type: str = None,
    priority: int = 1,
    rake_id: int = None,
    locomotive_id: int = None,
    status: str = "SCHEDULED",
    delay_minutes: int = 0,
    db: Session = Depends(get_db)
):

    # Check if train number already exists
    existing_train = (
        db.query(Train)
        .filter(Train.train_number == train_number)
        .first()
    )

    if existing_train:
        raise HTTPException(
            status_code=400,
            detail="Train number already exists"
        )

    # Check origin station
    origin_station = (
        db.query(Station)
        .filter(Station.id == origin_station_id)
        .first()
    )

    if not origin_station:
        raise HTTPException(
            status_code=404,
            detail=f"Origin station with ID {origin_station_id} not found"
        )

    # Check destination station
    destination_station = (
        db.query(Station)
        .filter(Station.id == destination_station_id)
        .first()
    )

    if not destination_station:
        raise HTTPException(
            status_code=404,
            detail=f"Destination station with ID {destination_station_id} not found"
        )

    # Check rake if provided
    if rake_id is not None:
        rake = (
            db.query(Rake)
            .filter(Rake.id == rake_id)
            .first()
        )

        if not rake:
            raise HTTPException(
                status_code=404,
                detail=f"Rake with ID {rake_id} not found"
            )

    # Check locomotive if provided
    if locomotive_id is not None:
        locomotive = (
            db.query(Locomotive)
            .filter(Locomotive.id == locomotive_id)
            .first()
        )

        if not locomotive:
            raise HTTPException(
                status_code=404,
                detail=f"Locomotive with ID {locomotive_id} not found"
            )

    # Create train
    train = Train(
        train_number=train_number,
        train_name=train_name,
        train_type=train_type,
        priority=priority,
        origin_station_id=origin_station_id,
        destination_station_id=destination_station_id,
        rake_id=rake_id,
        locomotive_id=locomotive_id,
        status=status,
        delay_minutes=delay_minutes
    )

    db.add(train)
    db.commit()
    db.refresh(train)

    return train


# GET ALL TRAINS
@router.get("/")
def get_trains(
    db: Session = Depends(get_db)
):
    return db.query(Train).all()


# GET ONE TRAIN
@router.get("/{train_id}")
def get_train(
    train_id: int,
    db: Session = Depends(get_db)
):
    train = (
        db.query(Train)
        .filter(Train.id == train_id)
        .first()
    )

    if not train:
        raise HTTPException(
            status_code=404,
            detail="Train not found"
        )

    return train


# DELETE TRAIN
@router.delete("/{train_id}")
def delete_train(
    train_id: int,
    db: Session = Depends(get_db)
):
    train = (
        db.query(Train)
        .filter(Train.id == train_id)
        .first()
    )

    if not train:
        raise HTTPException(
            status_code=404,
            detail="Train not found"
        )

    db.delete(train)
    db.commit()

    return {
        "message": "Train deleted successfully"
    }