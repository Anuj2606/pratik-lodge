"""
Content-Based Recommendation Algorithm
Recommends rooms based on user preferences and room features
"""

import math
from typing import Dict, List, Tuple
from .room_data import ROOM_DATA, PURPOSE_PREFERENCES


class ContentBasedRecommender:
    """
    Content-based filtering recommendation system
    Matches user preferences with room features
    """
    
    def __init__(self):
        self.room_data = ROOM_DATA
        self.purpose_prefs = PURPOSE_PREFERENCES
    
    def calculate_feature_similarity(self, user_prefs: Dict, room_features: Dict) -> float:
        """
        Calculate similarity score between user preferences and room features
        
        Args:
            user_prefs: User preference dictionary
            room_features: Room features dictionary
            
        Returns:
            Similarity score (0-1)
        """
        score = 0.0
        total_weight = 0.0
        
        # Feature matching
        feature_weights = {
            "ac": 0.2,
            "wifi": 0.15,
            "tv": 0.1,
            "balcony": 0.15,
            "luxury": 0.2,
            "room_service": 0.1,
            "capacity": 0.1
        }
        
        # Check AC requirement
        if user_prefs.get("ac", 0) == 1:
            if room_features.get("ac", False):
                score += feature_weights["ac"]
            total_weight += feature_weights["ac"]
        else:
            total_weight += feature_weights["ac"] * 0.5
        
        # Check other features
        for feature in ["wifi", "tv", "balcony", "luxury", "room_service"]:
            if room_features.get(feature, False):
                score += feature_weights[feature]
            total_weight += feature_weights[feature]
        
        # Capacity matching
        required_capacity = user_prefs.get("people", 1)
        room_capacity = room_features.get("capacity", 1)
        if room_capacity >= required_capacity:
            capacity_score = min(1.0, room_capacity / max(required_capacity, 1))
            score += feature_weights["capacity"] * capacity_score
        total_weight += feature_weights["capacity"]
        
        return score / total_weight if total_weight > 0 else 0.0
    
    def calculate_budget_fit(self, user_budget: int, room_price: int, days: int, season: str) -> float:
        """
        Calculate how well room fits user budget
        
        Args:
            user_budget: Total budget for stay
            room_price: Price per night
            days: Number of days
            season: Season type
            
        Returns:
            Budget fit score (0-1)
        """
        from .room_data import SEASON_MULTIPLIERS
        
        multiplier = SEASON_MULTIPLIERS.get(season.lower(), 1.0)
        total_cost = room_price * days * multiplier
        
        if total_cost <= user_budget:
            # Budget fits perfectly or under budget
            if total_cost == 0:
                return 0.0
            budget_ratio = user_budget / total_cost
            # Reward being close to budget but not over
            return min(1.0, budget_ratio)
        else:
            # Over budget - penalize
            overage_ratio = total_cost / user_budget
            return max(0.0, 1.0 - (overage_ratio - 1.0) * 0.5)
    
    def calculate_purpose_match(self, purpose: str, room_slug: str) -> float:
        """
        Calculate how well room matches user's purpose
        
        Args:
            purpose: User's purpose (business, leisure, family, solo)
            room_slug: Room identifier
            
        Returns:
            Purpose match score (0-1)
        """
        if purpose.lower() not in self.purpose_prefs:
            return 0.5  # Neutral score for unknown purposes
        
        purpose_pref = self.purpose_prefs[purpose.lower()]
        room = self.room_data[room_slug]
        score = 0.0
        
        # Check preferred features
        preferred_features = purpose_pref["preferred_features"]
        feature_count = 0
        matched_features = 0
        
        for pref_feature in preferred_features:
            if pref_feature == "capacity":
                # Check if room capacity is suitable
                if purpose.lower() == "family":
                    if room["capacity"] >= 4:
                        matched_features += 1
                feature_count += 1
            elif pref_feature in room["features"]:
                if room["features"][pref_feature]:
                    matched_features += 1
                feature_count += 1
            elif pref_feature == "value_score":
                # Value score check
                if room["value_score"] >= 7:
                    matched_features += 1
                feature_count += 1
        
        if feature_count > 0:
            score = matched_features / feature_count
        
        # Comfort priority check
        comfort_priority = purpose_pref["comfort_priority"]
        if comfort_priority == "high":
            score += room["comfort_score"] / 20  # Add up to 0.5
        elif comfort_priority == "medium":
            score += room["comfort_score"] / 30  # Add up to 0.33
        
        return min(1.0, score)
    
    def recommend(self, 
                  budget: int,
                  people: int,
                  days: int,
                  season: str,
                  ac: int,
                  purpose: str) -> List[Tuple[str, float, Dict]]:
        """
        Generate room recommendations based on user inputs
        
        Args:
            budget: Total budget
            people: Number of people
            days: Number of days
            season: Season (peak, moderate, low)
            ac: AC requirement (0 or 1)
            purpose: Purpose of visit
            
        Returns:
            List of tuples (room_slug, score, details) sorted by score
        """
        user_prefs = {
            "ac": ac,
            "people": people,
            "budget": budget,
            "days": days,
            "season": season,
            "purpose": purpose
        }
        
        recommendations = []
        
        for room_slug, room_info in self.room_data.items():
            # Calculate feature similarity
            feature_score = self.calculate_feature_similarity(user_prefs, room_info["features"])
            
            # Calculate budget fit
            budget_score = self.calculate_budget_fit(
                budget, 
                room_info["price_per_night"], 
                days, 
                season
            )
            
            # Calculate purpose match
            purpose_score = self.calculate_purpose_match(purpose, room_slug)
            
            # Calculate capacity fit
            capacity_fit = 1.0 if room_info["capacity"] >= people else 0.3
            
            # Weighted final score
            final_score = (
                feature_score * 0.3 +
                budget_score * 0.3 +
                purpose_score * 0.2 +
                capacity_fit * 0.2
            )
            
            recommendations.append((
                room_slug,
                final_score,
                {
                    "room_name": room_info["name"],
                    "price_per_night": room_info["price_per_night"],
                    "capacity": room_info["capacity"],
                    "feature_score": feature_score,
                    "budget_score": budget_score,
                    "purpose_score": purpose_score,
                    "capacity_fit": capacity_fit
                }
            ))
        
        # Sort by score (descending)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations

