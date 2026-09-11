import pandas as pd
from datetime import datetime

def compute_temporal_features(df: pd.DataFrame, current_date: datetime = None) -> pd.DataFrame:
    """
    Compute temporal and age-related features.
    """
    if current_date is None:
        current_date = pd.Timestamp.now()

    if 'deadline' in df.columns:
        df['deadline'] = pd.to_datetime(df['deadline'])
        df['days_until_deadline'] = (df['deadline'] - current_date).dt.days
        df['days_overdue'] = df['days_until_deadline'].apply(lambda x: abs(x) if x < 0 else 0)
        
    if 'commissioned_date' in df.columns:
        df['commissioned_date'] = pd.to_datetime(df['commissioned_date'])
        df['asset_age_days'] = (current_date - df['commissioned_date']).dt.days

    if 'last_maintenance_date' in df.columns:
        df['last_maintenance_date'] = pd.to_datetime(df['last_maintenance_date'])
        df['days_since_last_maintenance'] = (current_date - df['last_maintenance_date']).dt.days

    return df

def build_ml_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Main feature engineering pipeline.
    """
    if df.empty:
        return df
        
    df = compute_temporal_features(df)
    
    # Placeholder for categorical encoding or other feature transformations
    
    return df
