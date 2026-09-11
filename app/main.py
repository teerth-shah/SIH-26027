from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import Base, engine
from app.api.routes.stations import router as stations_router
from app.api.routes.sections import router as sections_router
from app.api.routes.assets import router as assets_router
from app.api.routes.rakes import router as rakes_router
from app.api.routes.locomotives import router as locomotives_router
from app.api.routes.trains import router as trains_router
from app.api.routes.train_schedules import router as train_schedules_router
from app.api.routes.maintenance_tasks import router as maintenance_tasks_router
from app.api.routes.resources import router as resources_router
from app.api.routes.resource_assignments import router as resource_assignments_router
from app.api.routes.blocks import router as blocks_router
from app.api.routes.blocks import router as conflicts_router
from app.api.routes.ml_router import router as ml_router

import app.models

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Railway Maintenance Block Planner",
    description="Backend API for railway maintenance block planning and resource management",
    version="1.0.0"
)

app.include_router(stations_router)
app.include_router(sections_router)
app.include_router(assets_router)
app.include_router(rakes_router)
app.include_router(locomotives_router)
app.include_router(trains_router)
app.include_router(train_schedules_router)
app.include_router(maintenance_tasks_router)
app.include_router(resources_router)
app.include_router(resource_assignments_router)
app.include_router(blocks_router)
app.include_router(conflicts_router)
app.include_router(ml_router)


@app.get("/")
def root():
    return {
        "message": "Railway Maintenance Block Planner Backend is running"
    }

@app.get("/database-test")
def database_test():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "success",
            "message": "Database connection is working"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }