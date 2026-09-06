from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.rake import Rake
from app.models.asset import Asset


router = APIRouter(
    prefix="/rakes",
    tags=["Rakes"]
)


@router.post("/")
def create_rake(
    asset_id: int,
    rake_number: str,
    rake_type: str,
    coach_count: int,
    capacity: int,
    status: str = "AVAILABLE",
    home_depot: str = None,
    db: Session = Depends(get_db)
):
    # Check whether the Asset exists
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail=f"Asset with ID {asset_id} not found"
        )

    # Check whether rake number already exists
    existing_rake = (
        db.query(Rake)
        .filter(Rake.rake_number == rake_number)
        .first()
    )

    if existing_rake:
        raise HTTPException(
            status_code=400,
            detail="Rake number already exists"
        )

    # Create the rake
    rake = Rake(
        asset_id=asset_id,
        rake_number=rake_number,
        rake_type=rake_type,
        coach_count=coach_count,
        capacity=capacity,
        status=status,
        home_depot=home_depot
    )

    db.add(rake)
    db.commit()
    db.refresh(rake)

    return rake


@router.get("/")
def get_rakes(
    db: Session = Depends(get_db)
):
    return db.query(Rake).all()


@router.get("/{rake_id}")
def get_rake(
    rake_id: int,
    db: Session = Depends(get_db)
):
    rake = (
        db.query(Rake)
        .filter(Rake.id == rake_id)
        .first()
    )

    if not rake:
        raise HTTPException(
            status_code=404,
            detail="Rake not found"
        )

    return rake


@router.delete("/{rake_id}")
def delete_rake(
    rake_id: int,
    db: Session = Depends(get_db)
):
    rake = (
        db.query(Rake)
        .filter(Rake.id == rake_id)
        .first()
    )

    if not rake:
        raise HTTPException(
            status_code=404,
            detail="Rake not found"
        )

    db.delete(rake)
    db.commit()

    return {
        "message": "Rake deleted successfully"
    }