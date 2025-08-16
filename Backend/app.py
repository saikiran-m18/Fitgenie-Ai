from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import os
from dotenv import load_dotenv
from recommender import generate_workout_plan, generate_diet_plan

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Config
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "super-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/fitness_app")
client = MongoClient(MONGO_URI)
db = client["fitness_app"]

# ✅ Serve frontend
@app.route("/")
def serve_index():
    return send_from_directory("../frontend", "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory("../frontend", path)

# ---------------- USER AUTH ---------------- #
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if db.users.find_one({"username": username}):
        return jsonify({"msg": "User already exists"}), 400

    hashed_pw = generate_password_hash(password)
    db.users.insert_one({"username": username, "password": hashed_pw})
    return jsonify({"msg": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    user = db.users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        token = create_access_token(identity=username)
        return jsonify({"access_token": token}), 200
    return jsonify({"msg": "Invalid credentials"}), 401

# ---------------- FITNESS PLAN ---------------- #
@app.route("/recommend", methods=["POST"])
@jwt_required()
def recommend():
    data = request.json
    goal = data.get("goal", "strength")
    days = int(data.get("days", 3))

    workout_plan = generate_workout_plan(goal, days)
    diet_plan = generate_diet_plan(goal)

    return jsonify({
        "workout": workout_plan,
        "diet": diet_plan
    }), 200

# ---------------- USER LOGGING ---------------- #
@app.route("/log", methods=["POST"])
@jwt_required()
def add_log():
    current_user = get_jwt_identity()
    data = request.json
    entry = {
        "user": current_user,
        "type": data.get("type"),
        "details": data.get("details")
    }
    db.logs.insert_one(entry)
    return jsonify({"msg": "Log added"}), 201


@app.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    current_user = get_jwt_identity()
    logs = list(db.logs.find({"user": current_user}, {"_id": 0}))
    return jsonify({"logs": logs}), 200


if __name__ == "__main__":
    app.run(debug=True)
