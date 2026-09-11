import pandas as pd
from datetime import timedelta

def generate_candidates(df: pd.DataFrame) -> list:
    """
    Generates candidate block windows from tasks.
    In a real system, this would evaluate free windows between train schedules.
    For now, it generates 1-3 candidate blocks per task based on its deadline.
    """
    candidates = []
    candidate_id = 1
    
    # Iterate through unique tasks
    for _, task in df.iterrows():
        # Baseline candidate: Exactly at deadline minus duration
        duration_mins = int(task.get('estimated_duration_minutes', 60))
        deadline = task['deadline']
        
        # Candidate 1: 1 day before deadline
        c1_start = deadline - timedelta(days=1)
        c1_end = c1_start + timedelta(minutes=duration_mins)
        
        candidates.append({
            'candidate_id': f"C-{candidate_id}",
            'task_id': task['task_id'],
            'section_id': task['section_id'],
            'start_time': c1_start,
            'end_time': c1_end,
            'duration_minutes': duration_mins,
            'predicted_delay': task.get('predicted_delay_minutes', 0),
            'risk_covered': task.get('risk_probability', 0),
            'urgency': task.get('urgency_score', 0)
        })
        candidate_id += 1
        
        # Candidate 2: 3 days before deadline (if possible)
        c2_start = deadline - timedelta(days=3)
        c2_end = c2_start + timedelta(minutes=duration_mins)
        candidates.append({
            'candidate_id': f"C-{candidate_id}",
            'task_id': task['task_id'],
            'section_id': task['section_id'],
            'start_time': c2_start,
            'end_time': c2_end,
            'duration_minutes': duration_mins,
            'predicted_delay': max(0, task.get('predicted_delay_minutes', 0) - 5), # assume slightly less delay
            'risk_covered': task.get('risk_probability', 0),
            'urgency': task.get('urgency_score', 0)
        })
        candidate_id += 1

    return candidates
