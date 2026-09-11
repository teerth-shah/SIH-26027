from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.block import Block
from app.models.maintenance_task import MaintenanceTask
from app.models.section import Section

router = APIRouter(
    prefix="/blocks",
    tags=["Blocks"]
)


@router.post("/")
def create_block(
    maintenance_task_id: int,
    section_id: int,
    planned_start: datetime,
    planned_end: datetime,
    actual_start: datetime = None,
    actual_end: datetime = None,
    status: str = "PLANNED",
    priority: int = 1,
    reason: str = None,
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

    # Check section exists
    section = db.query(Section).filter(
        Section.id == section_id
    ).first()

    if not section:
        raise HTTPException(
            status_code=404,
            detail="Section not found"
        )

    # Check time validity
    if planned_end <= planned_start:
        raise HTTPException(
            status_code=400,
            detail="planned_end must be after planned_start"
        )

    block = Block(
        maintenance_task_id=maintenance_task_id,
        section_id=section_id,
        planned_start=planned_start,
        planned_end=planned_end,
        actual_start=actual_start,
        actual_end=actual_end,
        status=status,
        priority=priority,
        reason=reason
    )

    db.add(block)
    db.commit()
    db.refresh(block)

    return block


@router.get("/")
def get_blocks(
    db: Session = Depends(get_db)
):
    return db.query(Block).all()


@router.get("/{block_id}")
def get_block(
    block_id: int,
    db: Session = Depends(get_db)
):
    block = db.query(Block).filter(
        Block.id == block_id
    ).first()

    if not block:
        raise HTTPException(
            status_code=404,
            detail="Block not found"
        )

    return block


@router.delete("/{block_id}")
def delete_block(
    block_id: int,
    db: Session = Depends(get_db)
):
    block = db.query(Block).filter(
        Block.id == block_id
    ).first()

    if not block:
        raise HTTPException(
            status_code=404,
            detail="Block not found"
        )

    db.delete(block)
    db.commit()

    return {
        "message": "Block deleted successfully"
    }