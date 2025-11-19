# Quick Start Guide - Room Recommendation System

## 🚀 Quick Setup

### 1. Backend Setup (5 minutes)

```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

Server will start at: `http://localhost:5000`

### 2. Test the API

Open a new terminal and test:

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

### 3. Frontend Integration

The recommendation component is already created! Just:

1. **Add environment variable** (create `.env.local` in root):
```env
NEXT_PUBLIC_BACKEND_URL=http://localhost:5000
```

2. **Access the page**:
   - Navigate to: `http://localhost:3000/recommendations`
   - Or use the component: `app/components/RoomRecommendation.tsx`

## 📁 Project Structure

```
backend/
├── app.py                          # Main Flask API
├── recommendation_service.py       # Service layer
└── recommendation_system/
    ├── room_data.py               # Room configurations
    ├── content_based.py           # Content-based algorithm
    ├── collaborative_filtering.py # Collaborative filtering
    ├── hybrid_recommender.py      # Hybrid system
    └── utils.py                   # Utilities

app/
├── components/
│   └── RoomRecommendation.tsx     # Frontend component
└── recommendations/
    └── page.tsx                    # Recommendations page
```

## 🎯 How It Works

1. **User Inputs**: Budget, people, days, season, AC, purpose
2. **Content-Based**: Matches preferences with room features
3. **Collaborative**: Learns from booking history (if available)
4. **Hybrid**: Combines both for best recommendations
5. **Output**: Top 3 room recommendations with scores

## 📊 Example Response

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

## 🔧 Customization

### Add New Room
Edit `backend/recommendation_system/room_data.py`

### Adjust Algorithm Weights
Edit `backend/recommendation_system/hybrid_recommender.py`

### Change Season Pricing
Edit `SEASON_MULTIPLIERS` in `room_data.py`

## 📚 Full Documentation

- **Complete Guide**: See `RECOMMENDATION_SYSTEM_GUIDE.md`
- **API Docs**: See `backend/README.md`
- **Code Comments**: All files are well-documented

## ✅ Next Steps

1. ✅ Backend is ready - just run `python app.py`
2. ✅ Frontend component is ready - use `/recommendations` page
3. 🔄 Optional: Connect MongoDB for collaborative filtering
4. 🔄 Optional: Train ML models on booking data

## 🐛 Troubleshooting

**CORS Error?** → Make sure `flask-cors` is installed

**No Recommendations?** → Check server logs and input validation

**Port Already in Use?** → Change port in `app.py` or use `PORT=5001 python app.py`

---

**That's it! Your recommendation system is ready to use! 🎉**

