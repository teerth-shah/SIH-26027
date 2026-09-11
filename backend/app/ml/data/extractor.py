import pandas as pd
from sqlalchemy.orm import Session
from app.models.maintenance_task import MaintenanceTask
from app.models.asset import Asset
from app.models.section import Section
from app.models.train import Train
from app.models.train_schedule import TrainSchedule
from app.models.block import Block

def load_maintenance_tasks(db: Session) -> pd.DataFrame:
    """Extract all maintenance tasks to a DataFrame."""
    query = db.query(MaintenanceTask).statement
    df = pd.read_sql(query, db.bind)
    return df

def load_assets(db: Session) -> pd.DataFrame:
    """Extract all assets to a DataFrame."""
    query = db.query(Asset).statement
    df = pd.read_sql(query, db.bind)
    return df

def load_sections(db: Session) -> pd.DataFrame:
    """Extract all sections to a DataFrame."""
    query = db.query(Section).statement
    df = pd.read_sql(query, db.bind)
    return df

def load_trains(db: Session) -> pd.DataFrame:
    """Extract all trains to a DataFrame."""
    query = db.query(Train).statement
    df = pd.read_sql(query, db.bind)
    return df

def load_train_schedules(db: Session) -> pd.DataFrame:
    """Extract all train schedules to a DataFrame."""
    query = db.query(TrainSchedule).statement
    df = pd.read_sql(query, db.bind)
    return df

def load_blocks(db: Session) -> pd.DataFrame:
    """Extract all blocks to a DataFrame."""
    query = db.query(Block).statement
    df = pd.read_sql(query, db.bind)
    return df
