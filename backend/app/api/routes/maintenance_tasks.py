from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.maintenance_task import MaintenanceTask


router = APIRouter(
    prefix="/maintenance-tasks",
    tags=["Maintenance Tasks"]
)


# CREATE MAINTENANCE TASK
@router.post("/")
def create_maintenance_task(
    asset_id: int,
    maintenance_type: str,
    required_duration_minutes: int,
    description: str = None,
    priority: int = 1,
    earliest_start: datetime = None,
    latest_finish: datetime = None,
    deadline: datetime = None,
    required_crew_type: str = None,
    status: str = "PENDING",
    safety_clearance_required: bool = False,
    db: Session = Depends(get_db)
):
    maintenance_task = MaintenanceTask(
        asset_id=asset_id,
        maintenance_type=maintenance_type,
        description=description,
        priority=priority,
        required_duration_minutes=required_duration_minutes,
        earliest_start=earliest_start,
        latest_finish=latest_finish,
        deadline=deadline,
        required_crew_type=required_crew_type,
        status=status,
        safety_clearance_required=safety_clearance_required
    )

    db.add(maintenance_task)
    db.commit()
    db.refresh(maintenance_task)

    return maintenance_task


# GET ALL MAINTENANCE TASKS
@router.get("/")
def get_maintenance_tasks(
    db: Session = Depends(get_db)
):
    return db.query(MaintenanceTask).all()


# GET ONE MAINTENANCE TASK
@router.get("/{task_id}")
def get_maintenance_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    maintenance_task = (
        db.query(MaintenanceTask)
        .filter(MaintenanceTask.id == task_id)
        .first()
    )

    if not maintenance_task:
        raise HTTPException(
            status_code=404,
            detail="Maintenance task not found"
        )

    return maintenance_task


# DELETE MAINTENANCE TASK
@router.delete("/{task_id}")
def delete_maintenance_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    maintenance_task = (
        db.query(MaintenanceTask)
        .filter(MaintenanceTask.id == task_id)
        .first()
    )

    if not maintenance_task:
        raise HTTPException(
            status_code=404,
            detail="Maintenance task not found"
        )

    db.delete(maintenance_task)
    db.commit()

    return {
        "message": "Maintenance task deleted successfully"
    }