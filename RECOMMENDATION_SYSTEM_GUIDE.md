# Room Recommendation System - Complete Guide

## Overview

This is a comprehensive AI/ML-based room recommendation system for Pratik Lodge. It uses multiple recommendation algorithms to provide personalized room suggestions based on user preferences.

## Project Structure

```
pratik-lodge/
├── backend/
│   ├── app.py                          # Flask API server
│   ├── recommendation_service.py       # Service layer
│   ├── recommendation_system/          # Core algorithms
│   │   ├── room_data.py               # Room configurations
│   │   ├── content_based.py           # Content-based filtering
│   │   ├── collaborative_filtering.py # Collaborative filtering
│   │   ├── hybrid_recommender.py      # Hybrid system
│   │   └── utils.py                   # Utilities
│   └── requirements.txt
├── app/
│   ├── components/
│   │   └── RoomRecommendation.tsx     # Frontend component
│   └── recommendations/
│       └── page.tsx                    # Recommendations page
└── RECOMMENDATION_SYSTEM_GUIDE.md     # This file
```

## How It Works

### 1. Content-Based Filtering
- **What it does**: Matches user preferences with room features
- **How it works**:
  - Analyzes user inputs (budget, people, days, AC requirement, purpose)
  - Compares with room features (price, capacity, amenities)
  - Scores each room based on feature matching
- **Best for**: New users without booking history

### 2. Collaborative Filtering
- **What it does**: Learns from other users' booking patterns
- **How it works**:
  - Finds users with similar preferences
  - Recommends rooms that similar users booked
  - Improves with more booking data
- **Best for**: Returning customers with booking history

### 3. Hybrid System
- **What it does**: Combines both algorithms for best results
- **How it works**:
  - Gets recommendations from both algorithms
  - Combines scores with weighted average
  - Provides top 3 recommendations
- **Best for**: All users (optimal approach)

## User Inputs

The system accepts these inputs:

| Input | Type | Description | Options |
|-------|------|-------------|---------|
| `budget` | int | Total budget for stay | Any positive number |
| `people` | int | Number of guests | 1-10 |
| `days` | int | Number of nights | 1-30 |
| `season` | string | Travel season | `peak`, `moderate`, `low` |
| `ac` | int | AC requirement | `0` (no), `1` (yes) |
| `purpose` | string | Purpose of visit | `business`, `leisure`, `family`, `solo` |
| `user_email` | string | User email (optional) | Any email |
| `check_in_date` | string | Check-in date (optional) | YYYY-MM-DD format |

## Room Types

### 1. Regular Room
- **Price**: ₹899/night
- **Capacity**: 2 people
- **Features**: WiFi, TV, Room Service
- **Best for**: Solo travelers, budget-conscious guests

### 2. Deluxe Room
- **Price**: ₹1799/night
- **Capacity**: 3 people
- **Features**: WiFi, AC, TV, Room Service, Luxury
- **Best for**: Business travelers, couples

### 3. Twin Bed with Balcony
- **Price**: ₹2299/night
- **Capacity**: 6 people
- **Features**: WiFi, AC, TV, Room Service, Balcony, Luxury
- **Best for**: Families, groups

## Setup Instructions

### Backend Setup

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Run the Flask server**:
```bash
python app.py
```

Server will start on `http://localhost:5000`

### Frontend Integration

1. **Add environment variable** (create `.env.local`):
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

2. **Access the recommendation page**:
- Navigate to `/recommendations` in your Next.js app
- Or use the `RoomRecommendation` component anywhere

### MongoDB Integration (Optional)

For collaborative filtering with booking history:

1. **Update `recommendation_service.py`**:
```python
from pymongo import MongoClient
import os

# Connect to MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/pratik_lodge"))
db = client['pratik_lodge']
bookings = list(db['bookings'].find())

# Initialize with booking history
recommendation_service = RecommendationService(bookings)
```

2. **Update after new bookings**:
```python
# In your booking API route
recommendation_service.update_booking_history(new_booking)
```

## API Usage Examples

### Example 1: Basic Recommendation
```javascript
const response = await fetch('http://localhost:5000/recommend-room', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    budget: 5000,
    people: 2,
    days: 3,
    season: 'moderate',
    ac: 1,
    purpose: 'leisure'
  })
});

const data = await response.json();
console.log(data.recommendations);
```

### Example 2: With User Email
```javascript
const response = await fetch('http://localhost:5000/recommend-room', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    budget: 8000,
    people: 4,
    days: 5,
    season: 'peak',
    ac: 1,
    purpose: 'family',
    user_email: 'user@example.com',
    check_in_date: '2024-06-15'
  })
});
```

## Algorithm Scoring

### Content-Based Scores
- **Feature Score** (30%): How well room features match user needs
- **Budget Score** (30%): How well room fits user budget
- **Purpose Score** (20%): How well room matches travel purpose
- **Capacity Score** (20%): How well room accommodates guests

### Final Recommendation Score
- Combines all scores with weights
- Range: 0.0 to 1.0 (0% to 100% match)
- Higher score = better recommendation

## Customization

### Adding New Rooms

Edit `backend/recommendation_system/room_data.py`:

```python
ROOM_DATA["new-room"] = {
    "name": "New Room Type",
    "price_per_night": 1500,
    "capacity": 4,
    "features": {
        "wifi": True,
        "ac": True,
        # ... other features
    },
    "amenities_score": 8,
    "comfort_score": 7,
    "value_score": 8
}
```

### Adjusting Algorithm Weights

Edit `backend/recommendation_system/hybrid_recommender.py`:

```python
recommendations = self.recommender.recommend(
    # ... other params
    content_weight=0.7,      # Increase content-based weight
    collaborative_weight=0.3  # Decrease collaborative weight
)
```

### Modifying Season Multipliers

Edit `backend/recommendation_system/room_data.py`:

```python
SEASON_MULTIPLIERS = {
    "peak": 1.5,      # Increase peak season price
    "moderate": 1.0,
    "low": 0.7        # Decrease low season price
}
```

## Testing

### Test the API
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

### Test Health Endpoint
```bash
curl http://localhost:5000/health
```

### Test Get All Rooms
```bash
curl http://localhost:5000/rooms
```

## Troubleshooting

### Issue: CORS Error
**Solution**: Make sure `flask-cors` is installed and `CORS(app)` is enabled in `app.py`

### Issue: No Recommendations
**Solution**: 
- Check if all required fields are provided
- Verify room data is properly configured
- Check server logs for errors

### Issue: Low Recommendation Scores
**Solution**:
- Adjust algorithm weights
- Update room feature scores
- Check if user inputs are realistic

## Future Enhancements

1. **Machine Learning Models**
   - Train on historical booking data
   - Use scikit-learn for predictions
   - Implement neural networks for deep learning

2. **Real-time Learning**
   - Update recommendations based on user clicks
   - A/B testing for algorithm improvements
   - User feedback integration

3. **Advanced Features**
   - Sentiment analysis from reviews
   - Seasonal demand prediction
   - Dynamic pricing recommendations
   - Multi-criteria optimization

4. **Performance**
   - Redis caching for recommendations
   - Database indexing
   - Async processing
   - CDN for static assets

## Support

For issues or questions:
1. Check the `backend/README.md` for detailed API documentation
2. Review algorithm implementations in `recommendation_system/`
3. Test with the provided examples

## License

This recommendation system is part of the Pratik Lodge project.

