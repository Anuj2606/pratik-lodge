"""
Hybrid Recommendation System
Combines content-based, collaborative filtering, and ML models
"""

from typing import Dict, List, Tuple
from .content_based import ContentBasedRecommender
from .collaborative_filtering import CollaborativeFilteringRecommender
from .ml_recommender import MLRecommender


class HybridRecommender:
    """
    Hybrid recommendation system combining multiple algorithms
    Now includes Machine Learning (Random Forest)
    """
    
    def __init__(self, booking_history: List[Dict] = None):
        """
        Initialize hybrid recommender
        
        Args:
            booking_history: Booking history for collaborative filtering
        """
        self.content_based = ContentBasedRecommender()
        self.collaborative = CollaborativeFilteringRecommender(booking_history)
        self.ml_recommender = MLRecommender()
        
        # Try to load pre-trained ML model
        self.ml_recommender.load_model()
    
    def recommend(self,
                  budget: int,
                  people: int,
                  days: int,
                  season: str,
                  ac: int,
                  purpose: str,
                  user_id: str = None,
                  user_email: str = None,
                  content_weight: float = 0.4,
                  collaborative_weight: float = 0.2,
                  ml_weight: float = 0.4) -> List[Tuple[str, float, Dict]]:
        """
        Generate hybrid recommendations using content-based, collaborative, and ML
        
        Args:
            budget: Total budget
            people: Number of people
            days: Number of days
            season: Season type
            ac: AC requirement
            purpose: Purpose of visit
            user_id: User ID for collaborative filtering
            user_email: User email for collaborative filtering
            content_weight: Weight for content-based (default: 0.4)
            collaborative_weight: Weight for collaborative (default: 0.2)
            ml_weight: Weight for ML model (default: 0.4)
            
        Returns:
            List of (room_slug, score, details) tuples sorted by score
        """
        from .room_data import ROOM_DATA
        
        user_data = {
            "budget": budget,
            "people": people,
            "days": days,
            "season": season,
            "ac": ac,
            "purpose": purpose
        }
        
        # Get content-based recommendations
        content_recs = self.content_based.recommend(
            budget, people, days, season, ac, purpose
        )
        
        # Get collaborative filtering recommendations
        user_id_for_cf = user_id or user_email or "anonymous"
        collab_recs = self.collaborative.recommend(user_id=user_id_for_cf)
        
        # Normalize weights
        total_weight = content_weight + collaborative_weight + ml_weight
        if total_weight > 0:
            content_weight /= total_weight
            collaborative_weight /= total_weight
            ml_weight /= total_weight
        
        # Combine all recommendations
        combined_scores = {}
        combined_details = {}
        
        # Add content-based scores
        for room_slug, score, details in content_recs:
            combined_scores[room_slug] = score * content_weight
            combined_details[room_slug] = {
                **details,
                "content_score": score,
                "collaborative_score": 0.0,
                "ml_score": 0.0
            }
        
        # Add collaborative filtering scores
        for room_slug, score, details in collab_recs:
            if room_slug in combined_scores:
                combined_scores[room_slug] += score * collaborative_weight
                combined_details[room_slug]["collaborative_score"] = score
            else:
                combined_scores[room_slug] = score * collaborative_weight
                combined_details[room_slug] = {
                    **details,
                    "content_score": 0.0,
                    "collaborative_score": score,
                    "ml_score": 0.0
                }
        
        # Add ML model scores for all rooms
        for room_slug, room_info in ROOM_DATA.items():
            ml_score = self.ml_recommender.predict_score(user_data, room_info)
            
            if room_slug in combined_scores:
                combined_scores[room_slug] += ml_score * ml_weight
                combined_details[room_slug]["ml_score"] = ml_score
            else:
                combined_scores[room_slug] = ml_score * ml_weight
                combined_details[room_slug] = {
                    "room_name": room_info["name"],
                    "price_per_night": room_info["price_per_night"],
                    "capacity": room_info["capacity"],
                    "content_score": 0.0,
                    "collaborative_score": 0.0,
                    "ml_score": ml_score
                }
        
        # Convert to list and sort
        recommendations = [
            (room_slug, combined_scores[room_slug], combined_details[room_slug])
            for room_slug in combined_scores
        ]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations
    
    def update_booking_history(self, new_booking: Dict):
        """
        Update booking history in collaborative filter
        
        Args:
            new_booking: New booking record
        """
        self.collaborative.update_history(new_booking)

