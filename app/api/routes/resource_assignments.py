from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.resource_assignment import ResourceAssignment
from app.models.maintenance_task import MaintenanceTask
from app.models.resource import Resource

router = APIRouter(
    prefix="/resource-assignments",
    tags=["Resource Assignments"]
)


@router.post("/")
def create_resource_assignment(
    maintenance_task_id: int,
    resource_id: int,
    assigned_from: datetime = None,
    assigned_until: datetime = None,
    status: str = "ASSIGNED",
    db: Session = Depends(get_db)
):
    # Check maintenance task exists
    task = db.query(MaintenanceTask).filter(
        MaintenanceTask.id == maintenance_task_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Maintenance task not found"
        )

    # Check resource exists
    resource = db.query(Resource).filter(
        Resource.id == resource_id
    ).first()

    if not resource:
        raise HTTPException(
            status_code=404,
            detail="Resource not found"
        )

    assignment = ResourceAssignment(
        maintenance_task_id=maintenance_task_id,
        resource_id=resource_id,
        assigned_from=assigned_from,
        assigned_until=assigned_until,
        status=status
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


@router.get("/")
def get_resource_assignments(
    db: Session = Depends(get_db)
):
    return db.query(ResourceAssignment).all()


@router.get("/{assignment_id}")
def get_resource_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = db.query(ResourceAssignment).filter(
        ResourceAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Resource assignment not found"
        )

    return assignment


@router.delete("/{assignment_id}")
def delete_resource_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = db.query(ResourceAssignment).filter(
        ResourceAssignment.id == assignment_id
    ).first()

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Resource assignment not found"
        )

    db.delete(assignment)
    db.commit()

    return {
        "message": "Resource assignment deleted successfully"
    }