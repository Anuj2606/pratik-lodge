"""
Simple script to train the ML recommendation model
Run this once to train the model, or when you have new booking data
"""

import numpy as np
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from recommendation_system.ml_recommender import MLRecommender
from recommendation_system.room_data import ROOM_DATA


def generate_training_data(num_samples: int = 1000):
    """
    Generate training data based on logical rules
    In production, replace this with real booking data from MongoDB
    """
    X = []
    y = []
    
    print(f"Generating {num_samples} training samples...")
    
    for _ in range(num_samples):
        # Random user preferences
        budget = np.random.randint(2000, 15000)
        people = np.random.randint(1, 6)
        days = np.random.randint(1, 7)
        season = np.random.choice(["peak", "moderate", "low"])
        ac = np.random.choice([0, 1])
        purpose = np.random.choice(["business", "leisure", "family", "solo"])
        
        user_data = {
            "budget": budget,
            "people": people,
            "days": days,
            "season": season,
            "ac": ac,
            "purpose": purpose
        }
        
        # For each room, determine if it's a good match
        for room_slug, room_info in ROOM_DATA.items():
            # Prepare features
            ml_recommender = MLRecommender()
            features = ml_recommender.prepare_features(user_data, room_info)
            X.append(features[0])
            
            # Label: 1 if good match, 0 otherwise
            # Good match criteria:
            # 1. Room capacity >= people
            # 2. Total cost fits budget (with season multiplier)
            # 3. AC requirement matches (if user needs AC)
            # 4. Purpose matches room features
            
            season_multipliers = {"peak": 1.3, "moderate": 1.0, "low": 0.8}
            multiplier = season_multipliers.get(season, 1.0)
            total_cost = room_info["price_per_night"] * days * multiplier
            
            capacity_ok = room_info["capacity"] >= people
            budget_ok = total_cost <= budget * 1.1  # Allow 10% over budget
            ac_ok = (ac == 0) or room_info["features"].get("ac", False)
            
            # Purpose matching
            purpose_ok = True
            if purpose == "family" and room_info["capacity"] < 4:
                purpose_ok = False
            elif purpose == "business" and not room_info["features"].get("wifi", False):
                purpose_ok = False
            
            label = 1 if (capacity_ok and budget_ok and ac_ok and purpose_ok) else 0
            y.append(label)
    
    return np.array(X), np.array(y)


def train_model():
    """Train the ML recommendation model"""
    print("=" * 50)
    print("Training ML Recommendation Model")
    print("=" * 50)
    
    # Generate training data
    X, y = generate_training_data(num_samples=2000)
    
    print(f"\nTraining data shape: {X.shape}")
    print(f"Positive samples: {np.sum(y)} ({np.sum(y)/len(y)*100:.1f}%)")
    print(f"Negative samples: {len(y) - np.sum(y)} ({(len(y)-np.sum(y))/len(y)*100:.1f}%)")
    
    # Create and train model
    ml_recommender = MLRecommender()
    
    print("\nTraining Random Forest model...")
    ml_recommender.train(X, y)
    
    print("\n[SUCCESS] Model trained successfully!")
    print(f"Model saved to: {ml_recommender.model_path}")
    
    # Test the model
    print("\nTesting model with sample data...")
    test_user = {
        "budget": 5000,
        "people": 2,
        "days": 3,
        "season": "moderate",
        "ac": 1,
        "purpose": "leisure"
    }
    
    for room_slug, room_info in ROOM_DATA.items():
        score = ml_recommender.predict_score(test_user, room_info)
        print(f"  {room_info['name']}: {score:.3f}")
    
    print("\n" + "=" * 50)
    print("Training complete! The model is ready to use.")
    print("=" * 50)


if __name__ == "__main__":
    train_model()

