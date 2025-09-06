from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime
import os
import recommender
import ai_model
import utils

# ----------------------------
# Setup Flask and MongoDB
# ----------------------------
app = Flask(__name__)
CORS(app)

print(">>> LOADED app.py with /recommend route")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["fitness_app"]
users = db["users"]

# ----------------------------
# Root route
# ----------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"msg": "Backend is working ✅"})

# ----------------------------
# Register route
# ----------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if users.find_one({"username": username}):
        return jsonify({"error": "User already exists"}), 400

    hashed_pw = utils.hash_password(password)
    users.insert_one({"username": username, "password": hashed_pw, "profile": {}, "history": []})
    return jsonify({"msg": "Registration successful"})

# ----------------------------
# Login route
# ----------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.find_one({"username": username})
    if user and utils.verify_password(password, user["password"]):
        return jsonify({"msg": "Login successful ✅"})
    else:
        return jsonify({"error": "Invalid username or password"}), 401
        
# ----------------------------
# User Profile route
# ----------------------------
@app.route("/profile", methods=["POST"])
def save_profile():
    data = request.get_json()
    username = data.get("username")
    profile = data.get("profile")

    if not username:
        return jsonify({"error": "Username is required"}), 400
    
    users.update_one({"username": username}, {"$set": {"profile": profile}})
    return jsonify({"msg": "Profile updated successfully"})

# ----------------------------
# Recommend route (diet plan demo)
# ----------------------------
@app.route("/recommend", methods=["POST"])
def recommend():
    print(">>> /recommend route was hit")
    data = request.get_json()
    goal = data.get("goal", "general")
    days = int(data.get("days", 6))
    username = data.get("username")

    # Check if user exists before proceeding
    user = users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found. Please log in first."}), 404

    # Fetch user profile to make recommendations more personalized
    profile = user.get("profile", {})
    
    # Handle the case where profile values might be None or strings
    try:
        if profile.get('height') is not None:
            profile['height'] = float(profile['height'])
        if profile.get('weight') is not None:
            profile['weight'] = float(profile['weight'])
        if profile.get('age') is not None:
            profile['age'] = int(profile['age'])
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid profile data. Height, weight, and age must be numbers."}), 400

    bmi, bmr = ai_model.calculate_bmi_bmr(profile)

    # Pass the days parameter to the recommender
    workout_plan = recommender.generate_workout_plan(goal, days)
    diet_plan = recommender.generate_diet_plan(goal)

    return jsonify({"workout_plan": workout_plan, "diet_plan": diet_plan, "bmi": bmi, "bmr": bmr})

# ----------------------------
# Mark Done route
# ----------------------------
@app.route("/mark_done", methods=["POST"])
def mark_done():
    data = request.get_json()
    username = data.get("username")
    goal = data.get("goal")

    today = datetime.now().strftime("%Y-%m-%d")
    user = users.find_one({"username": username})

    if not user:
        return jsonify({"error": "User not found"}), 404

    history = user.get("history", [])

    if history and history[-1]["date"] == today:
        return jsonify({"msg": "You've already marked today's workout as completed."})

    history.append({"date": today, "goal": goal})
    users.update_one({"username": username}, {"$set": {"history": history}})

    return jsonify({"msg": "Workout marked as completed!"})

# ----------------------------
# Dashboard route
# ----------------------------
@app.route("/dashboard", methods=["POST"])
def get_dashboard():
    data = request.get_json()
    username = data.get("username")

    user = users.find_one({"username": username})
    if not user:
        return jsonify({"error": "User not found"}), 404

    history = user.get("history", [])
    
    # Calculate streak and total workouts
    total_workouts = len(history)
    streak = 0
    if total_workouts > 0:
        streak = 1
        for i in range(len(history) - 1, 0, -1):
            date_current = datetime.strptime(history[i]["date"], "%Y-%m-%d").date()
            date_prev = datetime.strptime(history[i-1]["date"], "%Y-%m-%d").date()
            if (date_current - date_prev).days == 1:
                streak += 1
            else:
                break
    
    # Simple achievements
    achievements = []
    if total_workouts >= 7:
        achievements.append("Week-long Warrior: Completed 7 workouts!")
    if total_workouts >= 30:
        achievements.append("Month-long Maven: Completed 30 workouts!")

    # Format history for chart
    history_dates = [h["date"] for h in history]

    return jsonify({
        "streak": streak,
        "total_workouts": total_workouts,
        "achievements": achievements,
        "history": history_dates
    })

# ----------------------------
# Run server
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
