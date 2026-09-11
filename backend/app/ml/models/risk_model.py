import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score, average_precision_score, confusion_matrix
import joblib
import os

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "maintenance_risk_model.joblib")

class MaintenanceRiskModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.features = [
            'criticality', 'severity', 'priority', 'failure_count', 
            'condition_score', 'estimated_duration_minutes'
        ]

    def train(self, df: pd.DataFrame):
        """Train the maintenance risk model."""
        # Convert continuous true risk score to binary classification for risk model
        # Assuming > 0.6 is high risk
        df['is_high_risk'] = (df['true_risk_score'] > 0.6).astype(int)
        
        X = df[self.features].fillna(0)
        y = df['is_high_risk']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        y_prob = self.model.predict_proba(X_test)[:, 1]
        
        metrics = {
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'roc_auc': roc_auc_score(y_test, y_prob),
            'pr_auc': average_precision_score(y_test, y_prob),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        return metrics

    def save(self):
        joblib.dump(self.model, MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            return True
        return False

    def predict_maintenance_risk(self, df: pd.DataFrame) -> pd.DataFrame:
        """Predict risk on new data."""
        if not hasattr(self.model, "estimators_"):
            self.load()
            
        X = df[self.features].fillna(0)
        probs = self.model.predict_proba(X)[:, 1]
        
        df['risk_probability'] = probs
        
        def get_level(p):
            if p >= 0.8: return "CRITICAL"
            if p >= 0.6: return "HIGH"
            if p >= 0.3: return "MEDIUM"
            return "LOW"
            
        df['risk_level'] = df['risk_probability'].apply(get_level)
        return df

def predict_maintenance_risk(data: pd.DataFrame) -> pd.DataFrame:
    model = MaintenanceRiskModel()
    model.load()
    return model.predict_maintenance_risk(data)
