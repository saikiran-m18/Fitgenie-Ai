# recommender.py
"""
Recommender system for FitGenie AI
Provides diet and workout plans based on user goals
"""

# ---------------- DIET PLAN ----------------
def generate_diet_plan(goal="general"):
    """
    Returns a simple diet plan based on user fitness goal.
    """
    if goal.lower() == "weight_loss":
        return {
            "breakfast": "Oats with fruits 🍓 + Green tea 🍵",
            "lunch": "Grilled chicken 🐔 + salad 🥗",
            "dinner": "Soup 🍲 + steamed vegetables 🥦",
            "snacks": "Nuts & seeds 🌰",
        }
    elif goal.lower() == "muscle_gain":
        return {
            "breakfast": "Eggs 🍳 + protein shake 🥤",
            "lunch": "Rice 🍚 + chicken breast 🍗 + veggies 🥦",
            "dinner": "Paneer/tofu curry 🍛 + roti 🫓",
            "snacks": "Peanut butter sandwich 🥪 + whey protein",
        }
    else:  # general or maintenance
        return {
            "breakfast": "Idli/dosa 🥞 + chutney",
            "lunch": "Dal + rice 🍛 + salad 🥗",
            "dinner": "Roti 🫓 + sabzi 🍆",
            "snacks": "Fruit bowl 🍎🍌",
        }

# ---------------- WORKOUT PLAN ----------------
def generate_workout_plan(goal="general", days=6):
    """
    Returns a workout plan split across days of the week,
    based on the specified number of days.
    """
    plans = {
        "weight_loss": {
            "Monday": "Cardio 🏃 + Abs workout 💪",
            "Tuesday": "HIIT 🔥",
            "Wednesday": "Yoga 🧘 + stretching",
            "Thursday": "Cardio cycling 🚴",
            "Friday": "HIIT + strength",
            "Saturday": "Full-body workout 🏋️",
            "Sunday": "Rest / Light walk",
        },
        "muscle_gain": {
            "Monday": "Chest workout 🏋️‍♂️",
            "Tuesday": "Back + Biceps 💪",
            "Wednesday": "Leg day 🦵",
            "Thursday": "Shoulders + Triceps 💪",
            "Friday": "Chest + Core",
            "Saturday": "Legs + HIIT",
            "Sunday": "Rest",
        },
        "general": {
            "Monday": "Light cardio + yoga 🧘",
            "Tuesday": "Full-body workout 🏋️",
            "Wednesday": "Rest / Stretching",
            "Thursday": "Cardio + Core",
            "Friday": "Strength training",
            "Saturday": "Outdoor sports ⚽🏸",
            "Sunday": "Rest",
        }
    }
    
    # Select the base plan and slice it to the requested number of days
    base_plan = plans.get(goal.lower(), plans["general"])
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    workout_plan = {}
    for i in range(min(days, len(ordered_days))):
        day = ordered_days[i]
        workout_plan[day] = base_plan.get(day, "Rest")
    
    return workout_plan
