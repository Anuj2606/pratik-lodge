# Room Recommendation System

A comprehensive AI/ML-based room recommendation system for Pratik Lodge using multiple recommendation algorithms.

## Architecture

```
backend/
├── app.py                          # Flask API server
├── recommendation_service.py       # Service layer
├── recommendation_system/          # Core recommendation algorithms
│   ├── __init__.py
│   ├── room_data.py               # Room configurations and metadata
│   ├── content_based.py           # Content-based filtering algorithm
│   ├── collaborative_filtering.py # Collaborative filtering algorithm
│   ├── hybrid_recommender.py      # Hybrid recommendation system
│   └── utils.py                   # Utility functions
└── requirements.txt               # Python dependencies
```

## Features

### 1. **Content-Based Filtering**
- Matches user preferences with room features
- Considers: budget, capacity, AC requirement, amenities
- Purpose-based matching (business, leisure, family, solo)

### 2. **Collaborative Filtering**
- Learns from booking history
- Finds similar users and recommends based on their preferences
- Improves over time with more data

### 3. **Hybrid Recommendation System**
- Combines content-based and collaborative filtering
- Weighted scoring for optimal recommendations
- Provides top 3 room recommendations with scores

## API Endpoints

### 1. Get Recommendations
```http
POST /recommend-room
Content-Type: application/json

{
  "budget": 5000,
  "people": 2,
  "days": 3,
  "season": "moderate",
  "ac": 1,
  "purpose": "leisure",
  "user_email": "user@example.com",  // optional
  "check_in_date": "2024-06-15"      // optional
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "room_slug": "deluxe-room",
      "room_name": "Deluxe Room",
      "recommendation_score": 0.85,
      "price_per_night": 1799,
      "capacity": 3,
      "details": {
        "feature_score": 0.9,
        "budget_score": 0.8,
        "purpose_score": 0.85,
        "capacity_fit": 1.0
      }
    }
  ],
  "total_recommendations": 3,
  "top_recommendation": { ... }
}
```

### 2. Get All Rooms
```http
GET /rooms
```

### 3. Get Room Details
```http
GET /recommend-room/<room_slug>
```

### 4. Health Check
```http
GET /health
```

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask server:
```bash
python app.py
```

The server will run on `http://localhost:5000`

## Configuration

### Room Data
Edit `recommendation_system/room_data.py` to:
- Add new room types
- Update prices and features
- Modify season multipliers
- Adjust purpose preferences

### Algorithm Weights
In `hybrid_recommender.py`, adjust:
- `content_weight`: Weight for content-based recommendations (default: 0.6)
- `collaborative_weight`: Weight for collaborative filtering (default: 0.4)

## Integration with MongoDB

To enable collaborative filtering with booking history:

1. Update `recommendation_service.py`:
```python
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient(MONGODB_URI)
db = client['pratik_lodge']
bookings = db['bookings'].find()

# Initialize with booking history
recommendation_service = RecommendationService(list(bookings))
```

2. Update booking history after new bookings:
```python
recommendation_service.update_booking_history(new_booking)
```

## Frontend Integration

The recommendation component is available at:
- Component: `app/components/RoomRecommendation.tsx`
- Page: `app/recommendations/page.tsx`

Set environment variable:
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

## Algorithm Details

### Content-Based Scoring
- Feature matching: 30%
- Budget fit: 30%
- Purpose match: 20%
- Capacity fit: 20%

### Collaborative Filtering
- Uses cosine similarity to find similar users
- Recommends rooms based on similar users' preferences
- Requires booking history for optimal results

### Hybrid Approach
- Combines both algorithms with weighted scores
- Provides more accurate and diverse recommendations
- Balances personalization with feature matching

## Testing

Test the API using curl:

```bash
curl -X POST http://localhost:5000/recommend-room \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 5000,
    "people": 2,
    "days": 3,
    "season": "moderate",
    "ac": 1,
    "purpose": "leisure"
  }'
```

## Future Enhancements

1. **Machine Learning Models**
   - Train ML models on historical booking data
   - Use scikit-learn or TensorFlow for predictions

2. **Real-time Learning**
   - Update recommendations based on user feedback
   - A/B testing for algorithm improvements

3. **Advanced Features**
   - Sentiment analysis from reviews
   - Seasonal demand prediction
   - Dynamic pricing recommendations

4. **Performance Optimization**
   - Caching frequently accessed recommendations
   - Database indexing for faster queries
   - Async processing for large datasets

