from fastapi import FastAPI
from sqlalchemy import text
from app.core.database import Base, engine
from app.api.routes.stations import router as stations_router
from app.api.routes.sections import router as sections_router
from app.api.routes.assets import router as assets_router
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