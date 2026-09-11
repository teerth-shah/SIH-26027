from sqlalchemy.orm import Session
import pandas as pd

from app.ml.data.extractor import (
    load_maintenance_tasks,
    load_assets,
    load_sections,
    load_trains,
    load_train_schedules,
    load_blocks
)
from app.ml.data.validator import (
    validate_maintenance_tasks,
    validate_assets,
    validate_relationships
)
from app.ml.data.transformer import transform_to_ml_dataset
from app.ml.features.engineering import build_ml_features

def build_ml_dataset(db: Session) -> pd.DataFrame:
    """
    Main pipeline to build the ML dataset from the operational backend.
    """
    # 1. Extraction
    tasks_df = load_maintenance_tasks(db)
    assets_df = load_assets(db)
    sections_df = load_sections(db)
    # trains_df = load_trains(db)
    # schedules_df = load_train_schedules(db)
    # blocks_df = load_blocks(db)

    # 2. Validation
    tasks_df = validate_maintenance_tasks(tasks_df)
    assets_df = validate_assets(assets_df)
    tasks_df = validate_relationships(tasks_df, assets_df)

    # 3. Transformation / Joins
    data = {
        'tasks': tasks_df,
        'assets': assets_df,
        'sections': sections_df
    }
    
    ml_dataset = transform_to_ml_dataset(data)

    # 4. Feature Engineering
    ml_dataset = build_ml_features(ml_dataset)

    return ml_dataset
