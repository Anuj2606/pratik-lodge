# Pratik Lodge – AI Powered Lodge Booking Website

This is a Next.js lodge booking web application for **Pratik Lodge** deployed on Vercel.  
Users can browse rooms, receive AI-based room recommendations, and book rooms online with automated confirmation emails.

- Live Website: https://www.pratiklodge.in/
- Repository: https://github.com/Anuj2606/pratik-lodge

---

## Features

- Responsive lodge booking platform
- AI-powered room recommendation system
- Personalized room suggestions based on user preferences
- Hybrid recommendation algorithm
- Booking data stored in MongoDB
- Automatic booking confirmation emails
- Deployed using Vercel

---

## Tech Stack

### Frontend
- Next.js
- React
- Tailwind CSS

### Backend
- Flask (Recommendation API)

### Database
- MongoDB

### Email Service
- Nodemailer

### Machine Learning
- Content-Based Filtering
- Collaborative Filtering
- Random Forest Model

---

## Recommendation System

The project uses a **Hybrid Recommendation System** combining multiple algorithms.

### Content-Based Filtering
Matches user preferences with room features such as:

- Budget
- Capacity
- AC requirement
- Amenities
- Purpose of stay

### Collaborative Filtering

Uses booking history to find users with similar preferences and recommend rooms they previously booked.

### Machine Learning

A Random Forest model predicts the best room recommendations using multiple input features.

---

## Getting Started

### Clone the Repository

```bash
git clone https://github.com/Anuj2606/pratik-lodge.git
cd pratik-lodge
```

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open your browser and visit:

```
http://localhost:3000
```

---

## Backend Setup

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask server:

```bash
python app.py
```

Backend will run at:

```
http://localhost:5000
```

---

## Project Structure

```bash
backend/
 ├── app.py
 ├── recommendation_service.py
 ├── recommendation_system/
 │   ├── content_based.py
 │   ├── collaborative_filtering.py
 │   ├── hybrid_recommender.py
 │   ├── room_data.py
 │   └── utils.py
 └── requirements.txt

app/
 ├── components/
 ├── recommendations/
 └── page.tsx
```

---

## Deployment

This project is deployed using **Vercel**.

Deployment steps:

1. Push project to GitHub
2. Connect repository to Vercel
3. Deploy the project

---

## Author

Anuj Sawant  
BTech Computer Science Engineering 

GitHub: https://github.com/Anuj2606
