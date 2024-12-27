from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd
import numpy as np

class LakersPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.feature_importance = None
        
    def train(self, X: pd.DataFrame, y: pd.Series):
        """Train the model and store feature importance"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Calculate feature importance
        self.feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        # Calculate metrics
        y_pred = self.model.predict(X_test)
        metrics = {
            'r2_score': r2_score(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred))
        }
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Make predictions using the trained model"""
        return self.model.predict(X)
    
    def get_feature_importance(self) -> pd.DataFrame:
        """Return feature importance DataFrame"""
        return self.feature_importance
