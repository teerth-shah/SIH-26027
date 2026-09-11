import pandas as pd
import logging

logger = logging.getLogger(__name__)

def validate_maintenance_tasks(df: pd.DataFrame) -> pd.DataFrame:
    """Validate maintenance tasks dataset."""
    if df.empty:
        logger.warning("Maintenance tasks dataframe is empty.")
        return df

    # Check for duplicate IDs
    id_col = 'id' if 'id' in df.columns else 'task_id'
    if id_col in df.columns and df[id_col].duplicated().any():
        logger.error("Duplicate task IDs found.")
        df = df.drop_duplicates(subset=[id_col])

    # Validate priority/severity (assuming 1-10 range)
    invalid_priority = df[(df['priority'] < 1) | (df['priority'] > 10)]
    if not invalid_priority.empty:
        logger.warning(f"Found {len(invalid_priority)} tasks with invalid priority.")
    
    # Invalid duration
    dur_col = 'required_duration_minutes' if 'required_duration_minutes' in df.columns else 'estimated_duration_minutes'
    if dur_col in df.columns:
        invalid_duration = df[df[dur_col] <= 0]
        if not invalid_duration.empty:
            logger.warning(f"Found {len(invalid_duration)} tasks with duration <= 0.")
    
    # Invalid time windows
    if 'latest_finish' in df.columns and 'earliest_start' in df.columns:
        invalid_windows = df[df['latest_finish'] <= df['earliest_start']]
        if not invalid_windows.empty:
            logger.warning(f"Found {len(invalid_windows)} tasks with latest_finish <= earliest_start.")

    return df

def validate_assets(df: pd.DataFrame) -> pd.DataFrame:
    """Validate assets dataset."""
    if df.empty:
        return df
    
    id_col = 'id' if 'id' in df.columns else 'asset_id'
    if id_col in df.columns and df[id_col].duplicated().any():
        logger.error("Duplicate asset IDs found.")
        df = df.drop_duplicates(subset=[id_col])

    return df

def validate_relationships(tasks_df: pd.DataFrame, assets_df: pd.DataFrame) -> pd.DataFrame:
    """Check for broken relationships between tasks and assets."""
    if tasks_df.empty or assets_df.empty:
        return tasks_df

    asset_id_col = 'id' if 'id' in assets_df.columns else 'asset_id'
    missing_assets = tasks_df[~tasks_df['asset_id'].isin(assets_df[asset_id_col])]
    if not missing_assets.empty:
        logger.error(f"Found {len(missing_assets)} tasks referencing nonexistent assets.")
    
    return tasks_df
