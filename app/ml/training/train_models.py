import os
from app.ml.data.synthetic_generator import generate_synthetic_data
from app.ml.models.risk_model import MaintenanceRiskModel
from app.ml.models.impact_model import TrainImpactModel

def main():
    print("Generating synthetic data...")
    df = generate_synthetic_data(num_tasks=500, num_assets=200, num_sections=20, num_trains=100)
    
    print(f"Dataset generated with {len(df)} rows.")
    
    # Train risk model
    print("\nTraining Maintenance Risk Model...")
    risk_model = MaintenanceRiskModel()
    risk_metrics = risk_model.train(df)
    risk_model.save()
    print("Risk Model Metrics:")
    for k, v in risk_metrics.items():
        print(f"  {k}: {v}")
        
    # Train impact model
    print("\nTraining Train Impact Model...")
    impact_model = TrainImpactModel()
    impact_metrics = impact_model.train(df)
    impact_model.save()
    print("Impact Model Metrics:")
    for k, v in impact_metrics.items():
        print(f"  {k}: {v}")
        
    print("\nTraining complete and models saved.")

if __name__ == "__main__":
    main()
