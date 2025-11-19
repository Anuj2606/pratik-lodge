"""
Recommendation Service
Service layer to handle recommendation logic and database interactions
"""

from typing import Dict, List, Optional
from recommendation_system.hybrid_recommender import HybridRecommender
from recommendation_system.utils import (
    get_season_from_date,
    format_recommendation_response,
    validate_user_inputs
)
from recommendation_system.room_data import ROOM_DATA


class RecommendationService:
    """
    Service class for handling room recommendations
    """
    
    def __init__(self, booking_history: List[Dict] = None):
        """
        Initialize recommendation service
        
        Args:
            booking_history: List of booking records from database
        """
        self.recommender = HybridRecommender(booking_history)
    
    def get_recommendations(self,
                           budget: int,
                           people: int,
                           days: int,
                           season: str,
                           ac: int,
                           purpose: str,
                           user_email: Optional[str] = None,
                           check_in_date: Optional[str] = None) -> Dict:
        """
        Get room recommendations based on user inputs
        
        Args:
            budget: Total budget for stay
            people: Number of people
            days: Number of days
            season: Season type (peak/moderate/low)
            ac: AC requirement (0/1)
            purpose: Purpose of visit (business/leisure/family/solo)
            user_email: User email for personalized recommendations
            check_in_date: Check-in date (optional, for season detection)
            
        Returns:
            Dictionary with recommendations
        """
        # Auto-detect season from date if provided
        if check_in_date and not season:
            season = get_season_from_date(check_in_date)
        
        # Validate inputs
        is_valid, error_msg = validate_user_inputs(
            budget, people, days, season, ac, purpose
        )
        
        if not is_valid:
            return {
                "error": error_msg,
                "recommendations": []
            }
        
        # Get recommendations
        recommendations = self.recommender.recommend(
            budget=budget,
            people=people,
            days=days,
            season=season.lower(),
            ac=ac,
            purpose=purpose.lower(),
            user_email=user_email
        )
        
        # Format response
        return format_recommendation_response(recommendations, top_n=3)
    
    def get_room_details(self, room_slug: str) -> Optional[Dict]:
        """
        Get detailed information about a room
        
        Args:
            room_slug: Room identifier
            
        Returns:
            Room details dictionary or None
        """
        return ROOM_DATA.get(room_slug)
    
    def update_booking_history(self, booking: Dict):
        """
        Update booking history for collaborative filtering
        
        Args:
            booking: New booking record
        """
        self.recommender.update_booking_history(booking)

