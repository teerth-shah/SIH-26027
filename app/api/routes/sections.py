from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.section import Section


router = APIRouter(
    prefix="/sections",
    tags=["Sections"]
)


@router.post("/")
def create_section(
    section_code: str,
    name: str,
    from_station_id: int,
    to_station_id: int,
    distance_km: float = None,
    number_of_tracks: int = 1,
    electrified: bool = True,
    maximum_speed: float = None,
    capacity: int = None,
    db: Session = Depends(get_db)
):
    existing_section = (
        db.query(Section)
        .filter(Section.section_code == section_code)
        .first()
    )

    if existing_section:
        raise HTTPException(
            status_code=400,
            detail="Section code already exists"
        )

    section = Section(
        section_code=section_code,
        name=name,
        from_station_id=from_station_id,
        to_station_id=to_station_id,
        distance_km=distance_km,
        number_of_tracks=number_of_tracks,
        electrified=electrified,
        maximum_speed=maximum_speed,
        capacity=capacity
    )

    db.add(section)
    db.commit()
    db.refresh(section)

    return section


@router.get("/")
def get_sections(
    db: Session = Depends(get_db)
):
    return db.query(Section).all()


@router.get("/{section_id}")
def get_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    section = (
        db.query(Section)
        .filter(Section.id == section_id)
        .first()
    )

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    return section


@router.delete("/{section_id}")
def delete_section(
    section_id: int,
    db: Session = Depends(get_db)
):
    section = (
        db.query(Section)
        .filter(Section.id == section_id)
        .first()
    )

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    db.delete(section)
    db.commit()

    return {
        "message": "Section deleted successfully"
    }