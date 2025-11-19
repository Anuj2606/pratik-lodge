"""
Room Data Configuration
Defines room features, prices, and metadata for recommendation system
"""

ROOM_DATA = {
    "regular-room": {
        "name": "Regular Room",
        "price_per_night": 899,
        "capacity": 2,
        "features": {
            "wifi": True,
            "ac": False,
            "tv": True,
            "room_service": True,
            "balcony": False,
            "luxury": False
        },
        "amenities_score": 3,  # Out of 10
        "comfort_score": 5,     # Out of 10
        "value_score": 9        # Out of 10
    },
    "deluxe-room": {
        "name": "Deluxe Room",
        "price_per_night": 1799,
        "capacity": 3,
        "features": {
            "wifi": True,
            "ac": True,
            "tv": True,
            "room_service": True,
            "balcony": False,
            "luxury": True
        },
        "amenities_score": 7,
        "comfort_score": 8,
        "value_score": 7
    },
    "twin-room": {
        "name": "Twin Bed with balcony",
        "price_per_night": 2299,
        "capacity": 6,
        "features": {
            "wifi": True,
            "ac": True,
            "tv": True,
            "room_service": True,
            "balcony": True,
            "luxury": True
        },
        "amenities_score": 9,
        "comfort_score": 9,
        "value_score": 6
    }
}

# Season multipliers for pricing
SEASON_MULTIPLIERS = {
    "peak": 1.3,      # Summer, holidays
    "moderate": 1.0,  # Spring, Autumn
    "low": 0.8        # Winter, off-season
}

# Purpose-based preferences
PURPOSE_PREFERENCES = {
    "business": {
        "preferred_features": ["wifi", "ac", "room_service"],
        "budget_range": "medium_to_high",
        "comfort_priority": "high"
    },
    "leisure": {
        "preferred_features": ["tv", "balcony", "luxury"],
        "budget_range": "flexible",
        "comfort_priority": "medium"
    },
    "family": {
        "preferred_features": ["capacity", "balcony", "tv"],
        "budget_range": "medium",
        "comfort_priority": "high"
    },
    "solo": {
        "preferred_features": ["wifi", "value_score"],
        "budget_range": "low_to_medium",
        "comfort_priority": "medium"
    }
}

