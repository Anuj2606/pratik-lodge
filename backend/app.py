from flask import Flask, request, jsonify
from flask_cors import CORS
from recommendation_service import RecommendationService
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Initialize recommendation service
# In production, load booking history from MongoDB
recommendation_service = RecommendationService()

@app.route("/", methods=["GET"])
def index():
    """Root endpoint with API information"""
    return jsonify({
        "service": "Pratik Lodge Room Recommendation API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "GET /": "API information (this endpoint)",
            "GET /health": "Health check endpoint",
            "POST /recommend-room": "Get room recommendations",
            "GET /recommend-room/<room_slug>": "Get specific room details",
            "GET /rooms": "Get all available rooms"
        },
        "example_request": {
            "endpoint": "POST /recommend-room",
            "body": {
                "budget": 5000,
                "people": 2,
                "days": 3,
                "season": "moderate",
                "ac": 1,
                "purpose": "leisure"
            }
        }
    }), 200

@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "room-recommendation-api"})

@app.route("/recommend-room", methods=["POST"])
def recommend_room():
    """
    Get room recommendations based on user inputs
    
    Expected JSON body:
    {
        "budget": int,
        "people": int,
        "days": int,
        "season": str (peak/moderate/low),
        "ac": int (0 or 1),
        "purpose": str (business/leisure/family/solo),
        "user_email": str (optional),
        "check_in_date": str (optional, YYYY-MM-DD format)
    }
    """
    try:
        content = request.json
        
        if not content:
            return jsonify({"error": "Request body is required"}), 400
        
        # Extract required fields
        budget = int(content.get("budget", 0))
        people = int(content.get("people", 1))
        days = int(content.get("days", 1))
        season = content.get("season", "moderate")
        ac = int(content.get("ac", 0))
        purpose = content.get("purpose", "leisure")
        
        # Optional fields
        user_email = content.get("user_email")
        check_in_date = content.get("check_in_date")
        
        # Get recommendations
        result = recommendation_service.get_recommendations(
            budget=budget,
            people=people,
            days=days,
            season=season,
            ac=ac,
            purpose=purpose,
            user_email=user_email,
            check_in_date=check_in_date
        )
        
        if "error" in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route("/recommend-room/<room_slug>", methods=["GET"])
def get_room_details(room_slug):
    """Get detailed information about a specific room"""
    room_details = recommendation_service.get_room_details(room_slug)
    
    if not room_details:
        return jsonify({"error": "Room not found"}), 404
    
    return jsonify(room_details), 200

@app.route("/rooms", methods=["GET"])
def get_all_rooms():
    """Get list of all available rooms"""
    from recommendation_system.room_data import ROOM_DATA
    
    rooms = []
    for slug, details in ROOM_DATA.items():
        rooms.append({
            "slug": slug,
            "name": details["name"],
            "price_per_night": details["price_per_night"],
            "capacity": details["capacity"],
            "features": details["features"]
        })
    
    return jsonify({"rooms": rooms}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
