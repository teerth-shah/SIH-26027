import pandas as pd

def run_optimization(candidates: list, objective_weights: dict):
    """
    Run optimization to select best block candidates.
    Attempts to use OR-Tools CP-SAT, falls back to greedy heuristic if DLL fails.
    """
    try:
        from ortools.sat.python import cp_model
        return _run_cp_sat(candidates, objective_weights)
    except Exception as e:
        print(f"Warning: OR-Tools failed to load ({e}). Using heuristic fallback.")
        return _run_heuristic(candidates, objective_weights)

def _run_heuristic(candidates: list, objective_weights: dict):
    """Fallback greedy optimizer matching the same constraints and objectives."""
    w_delay = objective_weights.get("train_delay", -1)
    w_risk = objective_weights.get("maintenance_risk", 100)
    w_urgency = objective_weights.get("urgency", 50)
    w_duration = objective_weights.get("block_duration", -1)

    # Score all candidates
    for c in candidates:
        c['_score'] = (
            w_delay * c['predicted_delay'] +
            w_risk * c['risk_covered'] +
            w_urgency * c['urgency'] +
            w_duration * c['duration_minutes']
        )
    
    # Sort by score descending
    sorted_cands = sorted(candidates, key=lambda x: x['_score'], reverse=True)
    
    selected = []
    assigned_tasks = set()
    selected_blocks_by_section = {}
    
    for c in sorted_cands:
        if c['task_id'] in assigned_tasks:
            continue # Task already assigned
            
        sec_id = c['section_id']
        overlap = False
        
        # Check section overlaps
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
            
    # Clean up temp score
    for c in candidates:
        c.pop('_score', None)
        
    return {
        'status': 'FEASIBLE (Heuristic Fallback)',
        'selected_candidates': selected
    }

def _run_cp_sat(candidates: list, objective_weights: dict):
    from ortools.sat.python import cp_model
    model = cp_model.CpModel()
    
    # 1. Variables
    x = {}
    for c in candidates:
        x[c['candidate_id']] = model.NewBoolVar(f"x_{c['candidate_id']}")
        
    task_to_candidates = {}
    for c in candidates:
        task_id = c['task_id']
        if task_id not in task_to_candidates:
            task_to_candidates[task_id] = []
        task_to_candidates[task_id].append(c['candidate_id'])

    # 2. Constraints
    for task_id, cand_ids in task_to_candidates.items():
        model.AddAtMostOne([x[c_id] for c_id in cand_ids])

    section_to_candidates = {}
    for c in candidates:
        sec_id = c['section_id']
        if sec_id not in section_to_candidates:
            section_to_candidates[sec_id] = []
        section_to_candidates[sec_id].append(c)
        
    for sec_id, sec_cands in section_to_candidates.items():
        n = len(sec_cands)
        for i in range(n):
            for j in range(i + 1, n):
                c1 = sec_cands[i]
                c2 = sec_cands[j]
                if (c1['start_time'] < c2['end_time'] and c2['start_time'] < c1['end_time']):
                    model.AddImplication(x[c1['candidate_id']], x[c2['candidate_id']].Not())

    # 3. Objective Function
    w_delay = objective_weights.get("train_delay", -1)
    w_risk = objective_weights.get("maintenance_risk", 100)
    w_urgency = objective_weights.get("urgency", 50)
    w_duration = objective_weights.get("block_duration", -1)
    
    objective_terms = []
    for c in candidates:
        term = (
            w_delay * int(c['predicted_delay']) +
            w_risk * int(c['risk_covered'] * 100) +
            w_urgency * int(c['urgency'] * 100) +
            w_duration * int(c['duration_minutes'])
        )
        objective_terms.append(x[c['candidate_id']] * term)
        
    model.Maximize(sum(objective_terms))
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.Solve(model)
    
    result = {
        'status': solver.StatusName(status),
        'selected_candidates': []
    }
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for c in candidates:
            if solver.Value(x[c['candidate_id']]):
                result['selected_candidates'].append(c)
                
    return result
