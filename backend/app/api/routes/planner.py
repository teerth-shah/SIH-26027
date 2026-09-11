from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
from datetime import datetime

from app.ml.pipeline import generate_block_plan

router = APIRouter(prefix="/api", tags=["Machine Learning & Optimization"])

class PlanRequest(BaseModel):
    num_tasks: int = 50
    objective_weights: Optional[Dict[str, int]] = None

# Global state to mock history and dashboard for prototype
app_state = {
    "active_blocks": 2,
    "conflicts": 0,
    "efficiency": 85.0,
    "hours_saved": 0.0,
    "optimizer_status": "online",
    "history": []
}

@router.post("/planner/generate")
def api_generate_plan(request: PlanRequest):
    """
    Generates an optimized block plan using ML + OR-Tools.
    """
    try:
        result = generate_block_plan(
            num_tasks=request.num_tasks,
            objective_weights=request.objective_weights
        )
        # Update dashboard metrics
        app_state["active_blocks"] = len(result.get("selected_candidates", []))
        app_state["efficiency"] = 94.5  # Example update
        app_state["hours_saved"] += 2.5
        app_state["history"].insert(0, {
            "timestamp": datetime.now().isoformat(),
            "status": result.get("status"),
            "blocks_generated": len(result.get("selected_candidates", []))
        })
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dashboard")
def get_dashboard():
    """
    Returns KPIs for the system.
    """
    return app_state

@router.get("/history")
def get_history():
    return app_state["history"]

class BlockRequest(BaseModel):
    title: str
    section_id: int
    duration_mins: int

@router.post("/block-requests")
def create_block_request(req: BlockRequest):
    return {
        "status": "submitted",
        "request_id": f"REQ-{datetime.now().timestamp()}",
        "message": "Block request submitted successfully"
    }

@router.get("/planner/latest")
def get_latest_plan():
    if not app_state["history"]:
        return {"status": "no_plan"}
    return app_state["history"][0]
