"""
Simple Machine Learning Recommender using Random Forest
A straightforward ML model for room recommendations
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple, Optional
import joblib
import os
from .room_data import ROOM_DATA


class MLRecommender:
    """
    Simple Random Forest based recommender
    Uses machine learning to predict room recommendations
    """
    
    def __init__(self, model_path: str = "models/ml_model.pkl"):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.is_trained = False
        
    def prepare_features(self, user_data: Dict, room_data: Dict) -> np.ndarray:
        """
        Convert user and room data into feature vector
        
        Features (18 total):
        - User: budget, people, days, season, ac, purpose
        - Room: price, capacity, amenities, comfort, value scores
        - Room features: wifi, ac, tv, balcony, luxury, room_service
        """
        features = []
        
        # User features
        features.append(user_data.get("budget", 0))
        features.append(user_data.get("people", 1))
        features.append(user_data.get("days", 1))
        
        # Encode season: peak=2, moderate=1, low=0
        season_map = {"peak": 2, "moderate": 1, "low": 0}
        features.append(season_map.get(user_data.get("season", "moderate"), 1))
        
        features.append(user_data.get("ac", 0))
        
        # Encode purpose: business=0, leisure=1, family=2, solo=3
        purpose_map = {"business": 0, "leisure": 1, "family": 2, "solo": 3}
        features.append(purpose_map.get(user_data.get("purpose", "leisure"), 1))
        
        # Room features
        features.append(room_data.get("price_per_night", 0))
        features.append(room_data.get("capacity", 1))
        features.append(room_data.get("amenities_score", 0))
        features.append(room_data.get("comfort_score", 0))
        features.append(room_data.get("value_score", 0))
        
        # Room feature flags (0 or 1)
        room_features = room_data.get("features", {})
        features.append(1 if room_features.get("wifi", False) else 0)
        features.append(1 if room_features.get("ac", False) else 0)
        features.append(1 if room_features.get("tv", False) else 0)
        features.append(1 if room_features.get("balcony", False) else 0)
        features.append(1 if room_features.get("luxury", False) else 0)
        features.append(1 if room_features.get("room_service", False) else 0)
        
        return np.array(features).reshape(1, -1)
    
    def predict_score(self, user_data: Dict, room_data: Dict) -> float:
        """
        Predict recommendation score for a room (0-1)
        
        Returns:
            Score between 0 and 1, or 0.5 if model not trained
        """
        if not self.is_trained or self.model is None:
            return 0.5  # Neutral score if model not trained
        
        try:
            features = self.prepare_features(user_data, room_data)
            features_scaled = self.scaler.transform(features)
            
            # Get probability of positive recommendation
            proba = self.model.predict_proba(features_scaled)[0]
            return float(np.max(proba))  # Return max probability
        except:
            return 0.5  # Fallback to neutral score
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the Random Forest model
        
        Args:
            X_train: Feature matrix (n_samples, n_features)
            y_train: Target labels (0 or 1)
        """
        # Scale features
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Create and train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_scaled, y_train)
        self.is_trained = True
        
        # Save model
        self.save_model()
    
    def save_model(self):
        """Save trained model to file"""
        if self.model is not None:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            joblib.dump({
                "model": self.model,
                "scaler": self.scaler
            }, self.model_path)
    
    def load_model(self):
        """Load pre-trained model from file"""
        if os.path.exists(self.model_path):
            try:
                data = joblib.load(self.model_path)
                self.model = data["model"]
                self.scaler = data["scaler"]
                self.is_trained = True
                return True
            except:
                pass
        return False

