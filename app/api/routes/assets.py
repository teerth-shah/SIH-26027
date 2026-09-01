from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.asset import Asset


router = APIRouter(
    prefix="/assets",
    tags=["Assets"]
)


@router.post("/")
def create_asset(
    asset_code: str,
    asset_type: str,
    name: str = None,
    location: str = None,
    status: str = "AVAILABLE",
    commissioned_date: str = None,
    last_maintenance_date: str = None,
    next_maintenance_due: str = None,
    db: Session = Depends(get_db)
):
    existing_asset = (
        db.query(Asset)
        .filter(Asset.asset_code == asset_code)
        .first()
    )

    if existing_asset:
        raise HTTPException(
            status_code=400,
            detail="Asset code already exists"
        )

    asset = Asset(
        asset_code=asset_code,
        asset_type=asset_type,
        name=name,
        location=location,
        status=status
    )

    db.add(asset)
    db.commit()
    db.refresh(asset)

    return asset


@router.get("/")
def get_assets(
    db: Session = Depends(get_db)
):
    return db.query(Asset).all()


@router.get("/{asset_id}")
def get_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    return asset


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: int,
    db: Session = Depends(get_db)
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise HTTPException(
            status_code=404,
            detail="Asset not found"
        )

    db.delete(asset)
    db.commit()

    return {
        "message": "Asset deleted successfully"
    }