import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_tasks=100, num_assets=50, num_sections=10, num_trains=20):
    """
    Generates synthetic dataset for ML training representing railways operations.
    """
    np.random.seed(42)
    random.seed(42)
    
    current_date = pd.Timestamp.now()
    
    # 1. Sections
    sections = []
    for i in range(num_sections):
        sections.append({
            'section_id': i + 1,
            'section_code': f'SEC-{i+1}',
            'capacity': np.random.randint(10, 50),
            'historical_delay_avg': np.random.uniform(5, 30)
        })
    sections_df = pd.DataFrame(sections)
    
    # 2. Assets
    assets = []
    asset_types = ['Track', 'Signal', 'OHE', 'Point Machine']
    for i in range(num_assets):
        age_days = np.random.randint(100, 5000)
        commissioned = current_date - timedelta(days=age_days)
        criticality = np.random.randint(1, 10)
        
        # High criticality and old age -> more failures
        base_failure_prob = (age_days / 5000) * 0.5 + (criticality / 10) * 0.5
        failure_count = np.random.poisson(lam=base_failure_prob * 10)
        
        assets.append({
            'asset_id': i + 1,
            'section_id': np.random.randint(1, num_sections + 1),
            'asset_type': random.choice(asset_types),
            'commissioned_date': commissioned,
            'criticality': criticality,
            'failure_count': failure_count,
            'condition_score': np.clip(100 - (failure_count * 5) - (age_days / 100), 0, 100)
        })
    assets_df = pd.DataFrame(assets)
    
    # 3. Tasks
    tasks = []
    departments = ['ENGINEERING', 'SNT', 'TRACTION']
    for i in range(num_tasks):
        asset = assets[np.random.randint(0, num_assets)]
        asset_id = asset['asset_id']
        
        # Determine risk-related factors
        severity = np.random.randint(1, 10)
        priority = severity
        days_until_deadline = np.random.randint(-10, 30)
        deadline = current_date + timedelta(days=days_until_deadline)
        duration = np.random.randint(30, 180)
        
        # The true "risk score" target for our ML model to predict later, driven by physical features
        true_risk = (asset['criticality'] * 0.3 + 
                     severity * 0.4 + 
                     (asset['failure_count'] / 10) * 0.2 + 
                     (1 if days_until_deadline < 0 else 0) * 0.1) / 10
        true_risk = np.clip(true_risk + np.random.normal(0, 0.05), 0, 1)
        
        tasks.append({
            'task_id': i + 1,
            'asset_id': asset_id,
            'section_id': asset['section_id'],
            'department': random.choice(departments),
            'maintenance_type': 'INSPECTION' if random.random() > 0.5 else 'REPAIR',
            'severity': severity,
            'priority': priority,
            'estimated_duration_minutes': duration,
            'deadline': deadline,
            'true_risk_score': true_risk
        })
    tasks_df = pd.DataFrame(tasks)
    
    # 4. Train Schedules (Blocks / Impact)
    impacts = []
    for i in range(num_tasks):
        task = tasks[i]
        section_id = task['section_id']
        duration = task['estimated_duration_minutes']
        
        # features for train impact model
        train_count = np.random.randint(0, 20)
        passenger_trains = int(train_count * np.random.uniform(0.2, 0.8))
        goods_trains = train_count - passenger_trains
        peak_hour = 1 if random.random() > 0.7 else 0
        
        true_delay = (train_count * 2) + (passenger_trains * 3) + (peak_hour * 15) + (duration * 0.1)
        true_delay = np.clip(true_delay + np.random.normal(0, 5), 0, None)
        
        impacts.append({
            'task_id': task['task_id'],
            'train_count_in_window': train_count,
            'passenger_train_count': passenger_trains,
            'goods_train_count': goods_trains,
            'peak_hour': peak_hour,
            'true_predicted_delay_minutes': true_delay
        })
    impacts_df = pd.DataFrame(impacts)
    
    # Merge for final training dataset
    final_df = pd.merge(tasks_df, assets_df, on=['asset_id', 'section_id'])
    final_df = pd.merge(final_df, sections_df, on='section_id')
    final_df = pd.merge(final_df, impacts_df, on='task_id')
    
    return final_df

if __name__ == "__main__":
    df = generate_synthetic_data()
    df.to_csv("synthetic_ml_dataset.csv", index=False)
    print(f"Generated synthetic dataset with {len(df)} rows and {len(df.columns)} columns.")
