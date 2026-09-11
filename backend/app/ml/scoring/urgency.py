import pandas as pd
import numpy as np

def calculate_urgency_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Combines ML risk, asset criticality, severity, and deadline pressure.
    """
    if df.empty:
        return df
        
    df_out = df.copy()
    
    # Ensure all required columns exist with default 0 if missing
    req_cols = ['risk_probability', 'criticality', 'severity', 'days_until_deadline']
    for col in req_cols:
        if col not in df_out.columns:
            df_out[col] = 0
            
    # Normalize components
    # Risk is already 0-1
    risk_norm = df_out['risk_probability']
    
    # Criticality and severity 1-10
    crit_norm = df_out['criticality'] / 10.0
    sev_norm = df_out['severity'] / 10.0
    
    # Deadline pressure: higher if deadline is close or overdue
    # Assume 30 days is standard horizon. Overdue (>0) gives high pressure
    deadline_pressure = np.clip(1.0 - (df_out['days_until_deadline'] / 30.0), 0.0, 1.0)
    # Give a massive boost if overdue
    overdue_boost = (df_out['days_until_deadline'] < 0).astype(float) * 0.5
    deadline_pressure = np.clip(deadline_pressure + overdue_boost, 0.0, 1.0)
    
    # Weights
    w_risk = 0.4
    w_crit = 0.2
    w_sev = 0.2
    w_dead = 0.2
    
    urgency = (risk_norm * w_risk) + (crit_norm * w_crit) + (sev_norm * w_sev) + (deadline_pressure * w_dead)
    
    df_out['urgency_score'] = np.clip(urgency, 0.0, 1.0)
    
    def get_urgency_level(u):
        if u >= 0.8: return "CRITICAL"
        if u >= 0.6: return "HIGH"
        if u >= 0.3: return "MEDIUM"
        return "LOW"
        
    df_out['urgency_level'] = df_out['urgency_score'].apply(get_urgency_level)
    
    return df_out
