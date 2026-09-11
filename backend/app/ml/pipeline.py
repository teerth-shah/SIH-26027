import pandas as pd
from app.ml.data.synthetic_generator import generate_synthetic_data
from app.ml.data.validator import validate_maintenance_tasks
from app.ml.features.engineering import build_ml_features
from app.ml.scoring.urgency import calculate_urgency_score
from app.ml.models.risk_model import predict_maintenance_risk
from app.ml.models.impact_model import predict_train_impact
from app.ml.optimization.candidate_generator import generate_candidates
from app.ml.optimization.optimizer import run_optimization
import json

def generate_block_plan(num_tasks=50, objective_weights=None):
    """
    Master function that runs the complete end-to-end pipeline.
    """
    if objective_weights is None:
        objective_weights = {
            "train_delay": -1,
            "maintenance_risk": 100,
            "urgency": 50,
            "block_duration": -1,
            "coordination_gain": 20
        }

    print("1. Loading Data...")
    # In a real scenario, this would call build_ml_dataset()
    df = generate_synthetic_data(num_tasks=num_tasks)
    
    print("2. Validating Data...")
    df = validate_maintenance_tasks(df)
    
    print("3. Building Features...")
    df = build_ml_features(df)
    
    print("4. Predicting Maintenance Risk...")
    df = predict_maintenance_risk(df)
    
    print("5. Calculating Urgency...")
    df = calculate_urgency_score(df)
    
    print("6. Predicting Train Impact...")
    df = predict_train_impact(df)
    
    print("7. Generating Candidate Blocks...")
    candidates = generate_candidates(df)
    print(f"   Generated {len(candidates)} candidates.")
    
    print("8. Running Optimization (OR-Tools CP-SAT)...")
    optimization_result = run_optimization(candidates, objective_weights)
    
    status = optimization_result['status']
    print(f"\nOptimization successful. Status: {status}")
    
    if 'OPTIMAL' in status or 'FEASIBLE' in status:
        selected = optimization_result['selected_candidates']
        print(f"\nRecommended Maintenance Plan")
        print("-" * 30)
        
        # Group selected by section to show combined tasks
        blocks_by_section = {}
        for c in selected:
            sec = c['section_id']
            if sec not in blocks_by_section:
                blocks_by_section[sec] = []
            blocks_by_section[sec].append(c)
            
        block_idx = 1
        total_tasks_completed = len(selected)
        total_risk_covered = sum([c['risk_covered'] for c in selected])
        
        for sec, cands in blocks_by_section.items():
            print(f"\nBlock: B-{block_idx:03d}")
            print(f"Section: {sec}")
            # The actual start/end would be a unified block covering all tasks in this section if they overlap.
            # For this simple prototype, they are disjoint because we forbid overlap in the constraints.
            # So each candidate is essentially its own block.
            for c in cands:
                print(f"Time: {c['start_time'].strftime('%Y-%m-%d %H:%M')} - {c['end_time'].strftime('%Y-%m-%d %H:%M')}")
                print(f"Task ID: {c['task_id']}")
                print(f"Predicted train impact: {c['predicted_delay']:.2f} mins")
                print(f"Risk covered: {c['risk_covered']:.2f}")
                print(f"Reason: High urgency task ({c['urgency']:.2f}) scheduled before deadline.")
                block_idx += 1

        metrics = {
            "total_blocks": block_idx - 1,
            "tasks_completed": total_tasks_completed,
            "total_risk_covered": total_risk_covered
        }
        
        return {
            "status": status,
            "plan": selected,
            "metrics": metrics
        }
    else:
        print("NO_FEASIBLE_PLAN")
        return {"status": "NO_FEASIBLE_PLAN"}

if __name__ == "__main__":
    generate_block_plan()
