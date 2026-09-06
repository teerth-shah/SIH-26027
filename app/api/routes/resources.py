from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.resource import Resource


router = APIRouter(
    prefix="/resources",
    tags=["Resources"]
)


# CREATE RESOURCE
@router.post("/")
def create_resource(
    resource_code: str,
    resource_type: str,
    name: str = None,
    status: str = "AVAILABLE",
    location: str = None,
    availability_start: datetime = None,
    availability_end: datetime = None,
    capacity: int = 1,
    cost_per_hour: float = 0,
    db: Session = Depends(get_db)
):
    # Check if resource code already exists
    existing_resource = (
        db.query(Resource)
        .filter(Resource.resource_code == resource_code)
        .first()
    )

    if existing_resource:
        raise HTTPException(
            status_code=400,
            detail="Resource code already exists"
        )

    resource = Resource(
        resource_code=resource_code,
        resource_type=resource_type,
        name=name,
        status=status,
        location=location,
        availability_start=availability_start,
        availability_end=availability_end,
        capacity=capacity,
        cost_per_hour=cost_per_hour
    )

    db.add(resource)
    db.commit()
    db.refresh(resource)

    return resource


# GET ALL RESOURCES
@router.get("/")
def get_resources(
    db: Session = Depends(get_db)
):
    return db.query(Resource).all()


# GET ONE RESOURCE
@router.get("/{resource_id}")
def get_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    return resource


# DELETE RESOURCE
@router.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    db: Session = Depends(get_db)
):
    resource = (
        db.query(Resource)
        .filter(Resource.id == resource_id)
        .first()
    )

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    db.delete(resource)
    db.commit()

    return {
        "message": "Resource deleted successfully"
    }