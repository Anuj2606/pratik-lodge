"use client";

import { useState } from "react";
import { Montserrat } from "next/font/google";
import Image from "next/image";
import Link from "next/link";
import localFont from "next/font/local";

const montserrat = Montserrat({
  subsets: ["latin"],
  weight: ["400", "500", "600", "700"],
  variable: "--font-montserrat",
});

const kugile = localFont({
  src: "../fonts/Kugile_Demo.ttf",
  variable: "--font-kugile",
  display: "swap",
});

interface Recommendation {
  room_slug: string;
  room_name: string;
  recommendation_score: number;
  price_per_night: number;
  capacity: number;
  details: {
    feature_score: number;
    budget_score: number;
    purpose_score: number;
    capacity_fit: number;
  };
}

interface RecommendationResponse {
  recommendations: Recommendation[];
  total_recommendations: number;
  top_recommendation: Recommendation | null;
  error?: string;
}

const roomSlugToImage: Record<string, string> = {
  "regular-room": "/regular_1.jpg",
  "deluxe-room": "/deluxroom1.jpg",
  "twin-room": "/twin_3.jpg",
};

const roomSlugToRoute: Record<string, string> = {
  "regular-room": "/rooms/regular-room",
  "deluxe-room": "/rooms/deluxe-room",
  "twin-room": "/rooms/twin-room",
};

export default function RoomRecommendation() {
  const [formData, setFormData] = useState({
    budget: "",
    people: "1",
    days: "1",
    season: "moderate",
    ac: "0",
    purpose: "leisure",
    user_email: "",
    check_in_date: "",
  });

  const [recommendations, setRecommendations] =
    useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setRecommendations(null);

    try {
      const backendUrl =
        process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:5000";

      const response = await fetch(`${backendUrl}/recommend-room`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          budget: parseInt(formData.budget),
          people: parseInt(formData.people),
          days: parseInt(formData.days),
          season: formData.season,
          ac: parseInt(formData.ac),
          purpose: formData.purpose,
          user_email: formData.user_email || undefined,
          check_in_date: formData.check_in_date || undefined,
        }),
      });

      const data: RecommendationResponse = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Failed to get recommendations");
      }

      setRecommendations(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-[#F8F8F8] via-white to-[#F3F3F3] py-8 px-4 sm:px-6 md:px-12 lg:px-24 ${montserrat.variable}`}>
      {/* Header Section */}
      <div className="max-w-7xl mx-auto mb-12 text-center">
        <h1 className={`${kugile.className} text-4xl sm:text-5xl md:text-6xl lg:text-7xl mb-4 text-gray-800`}>
          Find Your Perfect Room
        </h1>
        <p className="text-lg sm:text-xl text-gray-600 max-w-2xl mx-auto">
          Our intelligent system analyzes your preferences to recommend the ideal room for your stay
        </p>
      </div>

      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Form Section */}
          <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-xl border border-gray-100 hover:shadow-2xl transition-shadow duration-300">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-yellow-400 to-yellow-500 rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-6 h-6 text-white">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h11.25c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25zM6.75 12h.008v.008H6.75V12zm0 3h.008v.008H6.75V15zm0 3h.008v.008H6.75V18z" />
                </svg>
              </div>
              <h2 className={`${montserrat.className} text-2xl sm:text-3xl font-bold text-gray-800`}>
                Your Preferences
              </h2>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                  Budget (₹)
                </label>
                <input
                  type="number"
                  name="budget"
                  value={formData.budget}
                  onChange={handleChange}
                  placeholder="Enter your total budget"
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all"
                  required
                  min="1"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                    People
                  </label>
                  <input
                    type="number"
                    name="people"
                    value={formData.people}
                    onChange={handleChange}
                    className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all"
                    required
                    min="1"
                    max="10"
                  />
                </div>

                <div className="flex flex-col gap-2">
                  <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                    <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                    Days
                  </label>
                  <input
                    type="number"
                    name="days"
                    value={formData.days}
                    onChange={handleChange}
                    className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all"
                    required
                    min="1"
                    max="30"
                  />
                </div>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                  Season
                </label>
                <select
                  name="season"
                  value={formData.season}
                  onChange={handleChange}
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all bg-white"
                >
                  <option value="peak">Peak (Summer/Holidays)</option>
                  <option value="moderate">Moderate (Spring/Autumn)</option>
                  <option value="low">Low (Winter/Off-season)</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                  AC Requirement
                </label>
                <select
                  name="ac"
                  value={formData.ac}
                  onChange={handleChange}
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all bg-white"
                >
                  <option value="0">Not Required</option>
                  <option value="1">Required</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-yellow-400 rounded-full"></span>
                  Purpose of Visit
                </label>
                <select
                  name="purpose"
                  value={formData.purpose}
                  onChange={handleChange}
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all bg-white"
                >
                  <option value="business">Business</option>
                  <option value="leisure">Leisure</option>
                  <option value="family">Family</option>
                  <option value="solo">Solo Travel</option>
                </select>
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-gray-300 rounded-full"></span>
                  Check-in Date (Optional)
                </label>
                <input
                  type="date"
                  name="check_in_date"
                  value={formData.check_in_date}
                  onChange={handleChange}
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all"
                />
              </div>

              <div className="flex flex-col gap-2">
                <label className="text-sm font-semibold text-gray-700 flex items-center gap-2">
                  <span className="w-2 h-2 bg-gray-300 rounded-full"></span>
                  Email (Optional)
                </label>
                <input
                  type="email"
                  name="user_email"
                  value={formData.user_email}
                  onChange={handleChange}
                  placeholder="your@email.com"
                  className="px-4 py-3 border-2 border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-yellow-400 focus:border-yellow-400 transition-all"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full py-4 bg-gradient-to-r from-yellow-400 to-yellow-500 text-black rounded-xl font-bold text-lg hover:from-yellow-500 hover:to-yellow-600 transition-all duration-300 shadow-lg hover:shadow-xl disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {loading ? (
                  <>
                    <svg className="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-5 h-5">
                      <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                    </svg>
                    Get Recommendations
                  </>
                )}
              </button>
            </form>

            {error && (
              <div className="mt-4 p-4 bg-red-50 border-2 border-red-200 text-red-700 rounded-xl">
                <div className="flex items-center gap-2">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-5 h-5">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                  </svg>
                  <span className="font-semibold">{error}</span>
                </div>
              </div>
            )}
          </div>

          {/* Recommendations Section */}
          <div className="bg-white p-6 sm:p-8 rounded-2xl shadow-xl border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-6 h-6 text-white">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 className={`${montserrat.className} text-2xl sm:text-3xl font-bold text-gray-800`}>
                Recommendations
              </h2>
            </div>

            {!recommendations && !loading && (
              <div className="text-center py-16">
                <div className="w-24 h-24 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5" stroke="currentColor" className="w-12 h-12 text-gray-400">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                  </svg>
                </div>
                <p className="text-gray-500 text-lg font-medium">Fill out the form to get personalized recommendations</p>
                <p className="text-gray-400 text-sm mt-2">Our system will analyze your preferences and suggest the perfect room</p>
              </div>
            )}

            {loading && (
              <div className="text-center py-16">
                <div className="w-24 h-24 mx-auto mb-4">
                  <svg className="animate-spin h-24 w-24 text-yellow-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                </div>
                <p className="text-gray-600 text-lg font-semibold">Analyzing your preferences...</p>
                <p className="text-gray-400 text-sm mt-2">Finding the perfect room match for you</p>
              </div>
            )}

            {recommendations && recommendations.recommendations.length > 0 && (
              <div className="space-y-6">
                {recommendations.recommendations.map((rec, index) => (
                  <div
                    key={rec.room_slug}
                    className={`relative overflow-hidden rounded-xl border-2 transition-all duration-300 hover:scale-[1.02] ${
                      index === 0
                        ? "border-yellow-400 bg-gradient-to-br from-yellow-50 to-yellow-100 shadow-lg"
                        : "border-gray-200 bg-white shadow-md hover:shadow-lg"
                    }`}
                  >
                    {index === 0 && (
                      <div className="absolute top-4 right-4 z-10">
                        <span className="bg-gradient-to-r from-yellow-400 to-yellow-500 text-black px-4 py-1.5 rounded-full text-sm font-bold shadow-md flex items-center gap-1">
                          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="2" stroke="currentColor" className="w-4 h-4">
                            <path strokeLinecap="round" strokeLinejoin="round" d="M11.48 3.499a.562.562 0 011.04 0l2.125 5.111a.563.563 0 00.475.345l5.518.442c.499.04.701.663.321.988l-4.204 3.602a.563.563 0 00-.182.557l1.285 5.385a.562.562 0 01-.84.61l-4.725-2.885a.563.563 0 00-.586 0L6.982 20.54a.562.562 0 01-.84-.61l1.285-5.386a.562.562 0 00-.182-.557l-4.204-3.602a.563.563 0 01.321-.988l5.518-.442a.563.563 0 00.475-.345L11.48 3.5z" />
                          </svg>
                          Top Pick
                        </span>
                      </div>
                    )}

                    <div className="p-6">
                      <div className="flex flex-col sm:flex-row gap-6">
                        <div className="relative w-full sm:w-40 h-48 sm:h-40 rounded-xl overflow-hidden flex-shrink-0 shadow-md">
                          <Image
                            src={roomSlugToImage[rec.room_slug] || "/placeholder.webp"}
                            alt={rec.room_name}
                            fill
                            className="object-cover"
                          />
                        </div>

                        <div className="flex-1">
                          <h3 className={`${montserrat.className} text-2xl font-bold mb-3 text-gray-800`}>
                            {rec.room_name}
                          </h3>

                          <div className="grid grid-cols-2 gap-3 mb-4">
                            <div className="bg-white/80 rounded-lg p-3 border border-gray-200">
                              <div className="text-xs text-gray-500 mb-1">Price/Night</div>
                              <div className="text-lg font-bold text-gray-800">₹{rec.price_per_night}</div>
                            </div>
                            <div className="bg-white/80 rounded-lg p-3 border border-gray-200">
                              <div className="text-xs text-gray-500 mb-1">Capacity</div>
                              <div className="text-lg font-bold text-gray-800">{rec.capacity} guests</div>
                            </div>
                          </div>

                          <div className="mb-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="text-sm font-semibold text-gray-700">Match Score</span>
                              <span className="text-lg font-bold text-green-600">
                                {(rec.recommendation_score * 100).toFixed(0)}%
                              </span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2.5">
                              <div
                                className="bg-gradient-to-r from-green-400 to-green-500 h-2.5 rounded-full transition-all duration-500"
                                style={{ width: `${rec.recommendation_score * 100}%` }}
                              ></div>
                            </div>
                          </div>

                          <div className="flex flex-wrap gap-2 mt-4">
                            <Link
                              href={roomSlugToRoute[rec.room_slug] || "#"}
                              className="flex-1 px-4 py-2.5 bg-gradient-to-r from-yellow-400 to-yellow-500 text-black rounded-lg font-semibold hover:from-yellow-500 hover:to-yellow-600 transition-all text-center text-sm shadow-md hover:shadow-lg"
                            >
                              View Details
                            </Link>
                            <Link
                              href="/booking"
                              className="flex-1 px-4 py-2.5 bg-gray-800 text-white rounded-lg font-semibold hover:bg-gray-900 transition-all text-center text-sm shadow-md hover:shadow-lg"
                            >
                              Book Now
                            </Link>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
