from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.locomotive import Locomotive


router = APIRouter(
    prefix="/locomotives",
    tags=["Locomotives"]
)


# CREATE LOCOMOTIVE
@router.post("/")
def create_locomotive(
    asset_id: int,
    loco_number: str,
    loco_type: str = None,
    home_shed: str = None,
    status: str = "AVAILABLE",
    db: Session = Depends(get_db)
):
    # Check if locomotive number already exists
    existing_loco = (
        db.query(Locomotive)
        .filter(Locomotive.loco_number == loco_number)
        .first()
    )

    if existing_loco:
        raise HTTPException(
            status_code=400,
            detail="Locomotive number already exists"
        )

    locomotive = Locomotive(
        asset_id=asset_id,
        loco_number=loco_number,
        loco_type=loco_type,
        home_shed=home_shed,
        status=status
    )

    db.add(locomotive)
    db.commit()
    db.refresh(locomotive)

    return locomotive


# GET ALL LOCOMOTIVES
@router.get("/")
def get_locomotives(
    db: Session = Depends(get_db)
):
    return db.query(Locomotive).all()


# GET ONE LOCOMOTIVE
@router.get("/{locomotive_id}")
def get_locomotive(
    locomotive_id: int,
    db: Session = Depends(get_db)
):
    locomotive = (
        db.query(Locomotive)
        .filter(Locomotive.id == locomotive_id)
        .first()
    )

    if not locomotive:
        raise HTTPException(
            status_code=404,
            detail="Locomotive not found"
        )

    return locomotive


# DELETE LOCOMOTIVE
@router.delete("/{locomotive_id}")
def delete_locomotive(
    locomotive_id: int,
    db: Session = Depends(get_db)
):
    locomotive = (
        db.query(Locomotive)
        .filter(Locomotive.id == locomotive_id)
        .first()
    )

    if not locomotive:
        raise HTTPException(
            status_code=404,
            detail="Locomotive not found"
        )

    db.delete(locomotive)
    db.commit()

    return {
        "message": "Locomotive deleted successfully"
    }