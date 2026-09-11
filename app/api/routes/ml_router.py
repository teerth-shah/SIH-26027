from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime

from app.ml.pipeline import generate_block_plan

router = APIRouter(prefix="/api/ml", tags=["Machine Learning & Optimization"])

class PlanRequest(BaseModel):
    num_tasks: int = 50
    objective_weights: Optional[Dict[str, int]] = None

@router.post("/generate-plan")
def api_generate_plan(request: PlanRequest):
    """
    Generates an optimized block plan using ML + OR-Tools.
    """
    try:
        result = generate_block_plan(
            num_tasks=request.num_tasks,
            objective_weights=request.objective_weights
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics")
def get_metrics():
    """
    Returns KPIs for the system.
    """
    return {
        "status": "success",
        "description": "API is online. Call /generate-plan to see KPIs."
    }
