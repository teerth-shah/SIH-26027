import pandas as pd
from typing import Dict

def transform_to_ml_dataset(data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Join entities into a unified dataset for ML.
    Expects data dict with 'tasks', 'assets', 'sections' DataFrames.
    """
    tasks_df = data.get('tasks', pd.DataFrame())
    assets_df = data.get('assets', pd.DataFrame())
    
    if tasks_df.empty:
        return pd.DataFrame()

    # Rename ID columns before merge to avoid conflicts
    if 'id' in tasks_df.columns:
        tasks_df = tasks_df.rename(columns={'id': 'task_id', 'status': 'task_status'})
    
    if not assets_df.empty:
        if 'id' in assets_df.columns:
            assets_df = assets_df.rename(columns={'id': 'asset_id_join', 'status': 'asset_status', 'name': 'asset_name'})
        elif 'asset_id' in assets_df.columns:
            assets_df = assets_df.rename(columns={'asset_id': 'asset_id_join', 'status': 'asset_status', 'name': 'asset_name'})
        # Merge Task with Asset
        unified_df = pd.merge(
            tasks_df,
            assets_df,
            left_on='asset_id',
            right_on='asset_id_join',
            how='left'
        ).drop(columns=['asset_id_join'])
    else:
        unified_df = tasks_df
        
    # Note: Currently the Asset model doesn't have a section_id. 
    # If it is added later, we can merge with sections_df here.

    return unified_df
