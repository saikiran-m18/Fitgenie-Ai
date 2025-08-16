# recommender.py
# Simple rule-based workout & diet recommender

def generate_workout_plan(goal="strength", days=3):
    workouts = {
        "strength": ["Push-ups", "Pull-ups", "Squats", "Deadlifts", "Bench Press"],
        "weight_loss": ["Burpees", "Jump Rope", "Running", "Mountain Climbers", "HIIT"],
        "flexibility": ["Yoga", "Stretching", "Pilates", "Plank Variations", "Mobility Drills"]
    }

    plan = []
    chosen = workouts.get(goal, workouts["strength"])
    for i in range(days):
        plan.append({
            "day": i + 1,
            "exercises": chosen[:3]  # pick first 3 exercises
        })
    return plan


def generate_diet_plan(goal="weight_loss"):
    diets = {
        "weight_loss": [
            "Breakfast: Oats with fruits",
            "Lunch: Grilled chicken salad",
            "Dinner: Vegetable soup with quinoa"
        ],
        "strength": [
            "Breakfast: Eggs & avocado toast",
            "Lunch: Brown rice with salmon",
            "Dinner: Chicken breast with sweet potato"
        ],
        "flexibility": [
            "Breakfast: Smoothie with spinach and banana",
            "Lunch: Whole grain wrap with hummus",
            "Dinner: Lentil soup with veggies"
        ]
    }

    return diets.get(goal, diets["strength"])
