# Machine Learning Recommendation - Simple Usage Guide

## What's Added

A simple **Random Forest** machine learning model has been integrated into the recommendation system. It's easy to use and doesn't require complex setup.

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the Model (One Time)

```bash
python train_model.py
```

This will:
- Generate training data (2000 samples)
- Train a Random Forest model
- Save the model to `models/ml_model.pkl`

**Note:** The model works even if not trained (uses default scores), but training improves accuracy.

### 3. Use the System

The ML model is **automatically integrated** into the recommendation system. Just use the API as usual:

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

## How It Works

The system now uses **3 algorithms** combined:

1. **Content-Based** (40% weight) - Matches features
2. **Collaborative Filtering** (20% weight) - Uses booking history
3. **Machine Learning** (40% weight) - Random Forest predictions

## Model Details

- **Algorithm:** Random Forest Classifier
- **Features:** 18 features (user preferences + room features)
- **Output:** Recommendation score (0-1)
- **Model File:** `backend/models/ml_model.pkl`

## Retraining

To retrain with new data, just run:

```bash
python train_model.py
```

The model will be automatically reloaded when the server restarts.

## Simple & Clean

- ✅ No complex setup
- ✅ Works without training (falls back to default)
- ✅ Easy to retrain
- ✅ Automatically integrated
- ✅ No manual configuration needed

That's it! The ML model is now part of your recommendation system.

