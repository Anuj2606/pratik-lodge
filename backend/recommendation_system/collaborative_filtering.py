"""
Collaborative Filtering Recommendation Algorithm
Recommends rooms based on similar users' preferences and booking history
"""

from typing import Dict, List, Tuple
from collections import defaultdict
import math


class CollaborativeFilteringRecommender:
    """
    Collaborative filtering recommendation system
    Uses user-item interactions to find similar users and recommend rooms
    """
    
    def __init__(self, booking_history: List[Dict] = None):
        """
        Initialize with booking history
        
        Args:
            booking_history: List of booking records with user preferences
        """
        self.booking_history = booking_history or []
        self.user_room_matrix = defaultdict(lambda: defaultdict(float))
        self.room_user_matrix = defaultdict(lambda: defaultdict(float))
        self._build_matrices()
    
    def _build_matrices(self):
        """Build user-room and room-user interaction matrices"""
        for booking in self.booking_history:
            user_id = booking.get("user_id") or booking.get("email", "anonymous")
            room_type = booking.get("roomType", "").lower()
            
            # Create room slug from room type
            room_slug = self._room_type_to_slug(room_type)
            if not room_slug:
                continue
            
            # Calculate interaction score based on booking
            score = 1.0  # Base score for booking
            
            # Increase score if user rebooks same room type
            if self.user_room_matrix[user_id][room_slug] > 0:
                score = 1.5
            
            self.user_room_matrix[user_id][room_slug] += score
            self.room_user_matrix[room_slug][user_id] += score
    
    def _room_type_to_slug(self, room_type: str) -> str:
        """Convert room type string to slug"""
        room_type_lower = room_type.lower()
        if "regular" in room_type_lower:
            return "regular-room"
        elif "deluxe" in room_type_lower:
            return "deluxe-room"
        elif "twin" in room_type_lower:
            return "twin-room"
        return ""
    
    def calculate_user_similarity(self, user1_prefs: Dict, user2_prefs: Dict) -> float:
        """
        Calculate cosine similarity between two users
        
        Args:
            user1_prefs: First user's room preferences
            user2_prefs: Second user's room preferences
            
        Returns:
            Similarity score (0-1)
        """
        # Get common rooms
        common_rooms = set(user1_prefs.keys()) & set(user2_prefs.keys())
        
        if not common_rooms:
            return 0.0
        
        # Calculate cosine similarity
        dot_product = sum(user1_prefs[room] * user2_prefs[room] for room in common_rooms)
        
        magnitude1 = math.sqrt(sum(score ** 2 for score in user1_prefs.values()))
        magnitude2 = math.sqrt(sum(score ** 2 for score in user2_prefs.values()))
        
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def find_similar_users(self, current_user_prefs: Dict, top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find users similar to current user
        
        Args:
            current_user_prefs: Current user's preferences
            top_k: Number of similar users to return
            
        Returns:
            List of (user_id, similarity_score) tuples
        """
        similarities = []
        
        for user_id, user_prefs in self.user_room_matrix.items():
            similarity = self.calculate_user_similarity(current_user_prefs, user_prefs)
            if similarity > 0:
                similarities.append((user_id, similarity))
        
        # Sort by similarity and return top k
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]
    
    def recommend(self, 
                  user_prefs: Dict = None,
                  user_id: str = None,
                  top_n: int = 3) -> List[Tuple[str, float, Dict]]:
        """
        Generate recommendations using collaborative filtering
        
        Args:
            user_prefs: User's current preferences (optional)
            user_id: User ID to find similar users (optional)
            top_n: Number of recommendations to return
            
        Returns:
            List of (room_slug, score, details) tuples
        """
        if not self.booking_history:
            # No history - return empty or use fallback
            return []
        
        # Get user's previous preferences if user_id provided
        if user_id and user_id in self.user_room_matrix:
            current_user_prefs = self.user_room_matrix[user_id]
        elif user_prefs:
            current_user_prefs = user_prefs
        else:
            return []
        
        # Find similar users
        similar_users = self.find_similar_users(current_user_prefs, top_k=10)
        
        if not similar_users:
            return []
        
        # Calculate recommendation scores
        room_scores = defaultdict(float)
        total_similarity = 0.0
        
        for similar_user_id, similarity in similar_users:
            total_similarity += similarity
            for room_slug, score in self.user_room_matrix[similar_user_id].items():
                if room_slug not in current_user_prefs:  # Don't recommend already booked
                    room_scores[room_slug] += score * similarity
        
        # Normalize scores
        if total_similarity > 0:
            for room_slug in room_scores:
                room_scores[room_slug] /= total_similarity
        
        # Convert to list and sort
        recommendations = [
            (room_slug, score, {"method": "collaborative_filtering"})
            for room_slug, score in room_scores.items()
        ]
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return recommendations[:top_n]
    
    def update_history(self, new_booking: Dict):
        """
        Update booking history with new booking
        
        Args:
            new_booking: New booking record
        """
        self.booking_history.append(new_booking)
        self._build_matrices()

