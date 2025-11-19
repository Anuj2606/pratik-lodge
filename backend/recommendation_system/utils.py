"""
Utility functions for recommendation system
"""

from typing import Dict, List, Tuple
from datetime import datetime


def get_season_from_date(date_str: str) -> str:
    """
    Determine season from date string
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        Season type: 'peak', 'moderate', or 'low'
    """
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        month = date_obj.month
        
        # Peak season: May-August (summer), December (holidays)
        if month in [5, 6, 7, 8, 12]:
            return "peak"
        # Low season: January-March (winter)
        elif month in [1, 2, 3]:
            return "low"
        # Moderate season: April, September-November
        else:
            return "moderate"
    except:
        return "moderate"


def format_recommendation_response(recommendations: List, top_n: int = 3) -> Dict:
    """
    Format recommendations for API response
    
    Args:
        recommendations: List of recommendation tuples
        top_n: Number of top recommendations to return
        
    Returns:
        Formatted response dictionary
    """
    from .room_data import ROOM_DATA
    
    top_recommendations = recommendations[:top_n]
    
    formatted_recs = []
    for room_slug, score, details in top_recommendations:
        room_info = ROOM_DATA.get(room_slug, {})
        formatted_recs.append({
            "room_slug": room_slug,
            "room_name": details.get("room_name", room_info.get("name", "")),
            "recommendation_score": round(score, 3),
            "price_per_night": details.get("price_per_night", room_info.get("price_per_night", 0)),
            "capacity": details.get("capacity", room_info.get("capacity", 0)),
            "details": {
                "feature_score": round(details.get("feature_score", 0), 3),
                "budget_score": round(details.get("budget_score", 0), 3),
                "purpose_score": round(details.get("purpose_score", 0), 3),
                "capacity_fit": round(details.get("capacity_fit", 0), 3)
            }
        })
    
    return {
        "recommendations": formatted_recs,
        "total_recommendations": len(formatted_recs),
        "top_recommendation": formatted_recs[0] if formatted_recs else None
    }


def validate_user_inputs(budget: int, people: int, days: int, 
                         season: str, ac: int, purpose: str) -> Tuple[bool, str]:
    """
    Validate user inputs for recommendation
    
    Args:
        budget: Budget value
        people: Number of people
        days: Number of days
        season: Season string
        ac: AC requirement
        purpose: Purpose string
        
    Returns:
        (is_valid, error_message)
    """
    if budget <= 0:
        return False, "Budget must be greater than 0"
    
    if people <= 0 or people > 10:
        return False, "Number of people must be between 1 and 10"
    
    if days <= 0 or days > 30:
        return False, "Number of days must be between 1 and 30"
    
    valid_seasons = ["peak", "moderate", "low"]
    if season.lower() not in valid_seasons:
        return False, f"Season must be one of: {', '.join(valid_seasons)}"
    
    if ac not in [0, 1]:
        return False, "AC requirement must be 0 or 1"
    
    valid_purposes = ["business", "leisure", "family", "solo"]
    if purpose.lower() not in valid_purposes:
        return False, f"Purpose must be one of: {', '.join(valid_purposes)}"
    
    return True, ""

