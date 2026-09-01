from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.station import Station


router = APIRouter(
    prefix="/stations",
    tags=["Stations"]
)


@router.post("/")
def create_station(
    station_code: str,
    station_name: str,
    zone: str = None,
    division: str = None,
    latitude: float = None,
    longitude: float = None,
    db: Session = Depends(get_db)
):
    existing_station = (
        db.query(Station)
        .filter(Station.station_code == station_code)
        .first()
    )

    if existing_station:
        raise HTTPException(
            status_code=400,
            detail="Station code already exists"
        )

    station = Station(
        station_code=station_code,
        station_name=station_name,
        zone=zone,
        division=division,
        latitude=latitude,
        longitude=longitude
    )

    db.add(station)
    db.commit()
    db.refresh(station)

    return station


@router.get("/")
def get_stations(
    db: Session = Depends(get_db)
):
    return db.query(Station).all()


@router.get("/{station_id}")
def get_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    station = (
        db.query(Station)
        .filter(Station.id == station_id)
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    return station


@router.delete("/{station_id}")
def delete_station(
    station_id: int,
    db: Session = Depends(get_db)
):
    station = (
        db.query(Station)
        .filter(Station.id == station_id)
        .first()
    )

    if not station:
        raise HTTPException(
            status_code=404,
            detail="Station not found"
        )

    db.delete(station)
    db.commit()

    return {
        "message": "Station deleted successfully"
    }