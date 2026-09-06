from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.conflict import Conflict
from app.models.block import Block

router = APIRouter(
    prefix="/conflicts",
    tags=["Conflicts"]
)


@router.post("/")
def create_conflict(
    block_1_id: int,
    block_2_id: int,
    conflict_type: str,
    severity: str = "MEDIUM",
    detected_at: datetime = None,
    resolved: bool = False,
    resolution: str = None,
    db: Session = Depends(get_db)
):
    # Check first block exists
    block_1 = db.query(Block).filter(
        Block.id == block_1_id
    ).first()

    if not block_1:
        raise HTTPException(
            status_code=404,
            detail="Block 1 not found"
        )

    # Check second block exists
    block_2 = db.query(Block).filter(
        Block.id == block_2_id
    ).first()

    if not block_2:
        raise HTTPException(
            status_code=404,
            detail="Block 2 not found"
        )

    # Prevent comparing a block with itself
    if block_1_id == block_2_id:
        raise HTTPException(
            status_code=400,
            detail="A block cannot conflict with itself"
        )

    conflict = Conflict(
        block_1_id=block_1_id,
        block_2_id=block_2_id,
        conflict_type=conflict_type,
        severity=severity,
        detected_at=detected_at,
        resolved=resolved,
        resolution=resolution
    )

    db.add(conflict)
    db.commit()
    db.refresh(conflict)

    return conflict


@router.get("/")
def get_conflicts(
    db: Session = Depends(get_db)
):
    return db.query(Conflict).all()


@router.get("/{conflict_id}")
def get_conflict(
    conflict_id: int,
    db: Session = Depends(get_db)
):
    conflict = db.query(Conflict).filter(
        Conflict.id == conflict_id
    ).first()

    if not conflict:
        raise HTTPException(
            status_code=404,
            detail="Conflict not found"
        )

    return conflict


@router.delete("/{conflict_id}")
def delete_conflict(
    conflict_id: int,
    db: Session = Depends(get_db)
):
    conflict = db.query(Conflict).filter(
        Conflict.id == conflict_id
    ).first()

    if not conflict:
        raise HTTPException(
            status_code=404,
            detail="Conflict not found"
        )

    db.delete(conflict)
    db.commit()

    return {
        "message": "Conflict deleted successfully"
    }