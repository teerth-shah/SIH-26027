import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import numpy as np

MODEL_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(MODEL_DIR, "train_impact_model.joblib")

class TrainImpactModel:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.features = [
            'train_count_in_window', 'passenger_train_count', 'goods_train_count',
            'peak_hour', 'estimated_duration_minutes'
        ]

    def train(self, df: pd.DataFrame):
        """Train the train impact model."""
        X = df[self.features].fillna(0)
        y = df['true_predicted_delay_minutes']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        return metrics

    def save(self):
        joblib.dump(self.model, MODEL_PATH)

    def load(self):
        if os.path.exists(MODEL_PATH):
            self.model = joblib.load(MODEL_PATH)
            return True
        return False

    def predict_train_impact(self, df: pd.DataFrame) -> pd.DataFrame:
        """Predict expected delay minutes."""
        if not hasattr(self.model, "estimators_"):
            self.load()
            
        X = df[self.features].fillna(0)
        preds = self.model.predict(X)
        
        df['predicted_delay_minutes'] = preds
        return df

def predict_train_impact(data: pd.DataFrame) -> pd.DataFrame:
    model = TrainImpactModel()
    model.load()
    return model.predict_train_impact(data)
