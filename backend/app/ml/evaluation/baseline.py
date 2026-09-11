import pandas as pd

def run_baseline_planner(candidates: list) -> dict:
    """
    Simple earliest-feasible-window planner to compare against optimized ML planner.
    Selects the first candidate block for each task without global optimization.
    """
    selected = []
    assigned_tasks = set()
    selected_blocks_by_section = {}
    
    # Sort purely by start_time (earliest feasible window)
    sorted_cands = sorted(candidates, key=lambda x: x['start_time'])
    
    for c in sorted_cands:
        if c['task_id'] in assigned_tasks:
            continue
            
        sec_id = c['section_id']
        overlap = False
        
        if sec_id in selected_blocks_by_section:
            for existing in selected_blocks_by_section[sec_id]:
                if (c['start_time'] < existing['end_time'] and existing['start_time'] < c['end_time']):
                    overlap = True
                    break
        
        if not overlap:
            selected.append(c)
            assigned_tasks.add(c['task_id'])
            if sec_id not in selected_blocks_by_section:
                selected_blocks_by_section[sec_id] = []
            selected_blocks_by_section[sec_id].append(c)
            
    return {
        'status': 'FEASIBLE',
        'selected_candidates': selected
    }
