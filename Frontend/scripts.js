// scripts.js
const API_URL = "http://127.0.0.1:5000";

// DOM elements
const authSection = document.getElementById("auth-section");
const planSection = document.getElementById("plan-section");
const userNameSpan = document.getElementById("user-name");
const loader = document.getElementById("loader");
const workoutDiv = document.getElementById("workout");
const dietDiv = document.getElementById("diet");
const popup = document.getElementById("popup");
const popupMessage = document.getElementById("popup-message");
const dashboard = document.getElementById("dashboard");
const streakLine = document.getElementById("streak-line");
const achievementsList = document.getElementById("achievements-list");

let currentUsername = "";
let currentGoal = "";

// Helper function to show popups
function showPopup(message) {
  popupMessage.textContent = message;
  popup.classList.remove("hidden");
}

function closePopup() {
  popup.classList.add("hidden");
}

// User Authentication
async function register() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const response = await fetch(`${API_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  showPopup(data.msg || data.error);
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const response = await fetch(`${API_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await response.json();
  if (response.ok) {
    currentUsername = username;
    userNameSpan.textContent = username;
    authSection.classList.add("hidden");
    planSection.classList.remove("hidden");
    await getDashboard();
  } else {
    showPopup(data.error);
  }
}

function logout() {
  currentUsername = "";
  authSection.classList.remove("hidden");
  planSection.classList.add("hidden");
  clearFields();
  workoutDiv.classList.add('hidden');
  dietDiv.classList.add('hidden');
}

function clearFields() {
  document.getElementById("username").value = "";
  document.getElementById("password").value = "";
}

// User Profile
async function saveProfile() {
  const height = document.getElementById("height").value;
  const weight = document.getElementById("weight").value;
  const age = document.getElementById("age").value;
  const gender = document.getElementById("gender").value;

  if (!height || !weight || !age || !gender) {
    showPopup("Please fill in all profile fields.");
    return;
  }

  const profile = { height, weight, age, gender };
  const response = await fetch(`${API_URL}/profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: currentUsername, profile }),
  });
  const data = await response.json();
  showPopup(data.msg);
}

// Get Workout and Diet Plan
async function getPlan() {
  loader.classList.remove("hidden");
  const goal = document.getElementById("goal").value;
  const days = document.getElementById("days").value;
  currentGoal = goal;

  const response = await fetch(`${API_URL}/recommend`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ goal, days, username: currentUsername }),
  });
  const data = await response.json();

  if (response.ok) {
    loader.classList.add("hidden");
    displayPlan(data.workout_plan, data.diet_plan);
  } else {
    loader.classList.add("hidden");
    showPopup(data.error || "An unexpected error occurred.");
  }
}

function refreshPlan() {
  getPlan();
}

function displayPlan(workoutPlan, dietPlan) {
  const workoutOrder = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
  const dietOrder = ["breakfast", "lunch", "dinner", "snacks"];

  workoutDiv.classList.remove('hidden');
  dietDiv.classList.remove('hidden');

  workoutDiv.innerHTML = "<h3>🏋️ Workout Plan</h3>";
  dietDiv.innerHTML = "<h3>🍎 Diet Plan</h3>";

  workoutOrder.forEach(day => {
    if (workoutPlan[day]) {
      const dayCard = document.createElement("div");
      dayCard.className = "plan-item";
      dayCard.innerHTML = `
        <h4>${day}</h4>
        <p>${workoutPlan[day]}</p>
      `;
      workoutDiv.appendChild(dayCard);
    }
  });

  dietOrder.forEach(meal => {
    if (dietPlan[meal]) {
      const mealCard = document.createElement("div");
      mealCard.className = "plan-item";
      mealCard.innerHTML = `
        <h4>${meal.charAt(0).toUpperCase() + meal.slice(1)}</h4>
        <p>${dietPlan[meal]}</p>
      `;
      dietDiv.appendChild(mealCard);
    }
  });
}

// Mark Today as Completed
async function markTodayDone() {
  const response = await fetch(`${API_URL}/mark_done`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: currentUsername, goal: currentGoal }),
  });
  const data = await response.json();
  showPopup(data.msg);
}

// Dashboard
async function toggleDashboard(show) {
  if (show) {
    if (!currentUsername) {
      showPopup("Please log in to view the dashboard.");
      return;
    }
    dashboard.classList.remove("hidden");
    await getDashboard();
  } else {
    dashboard.classList.add("hidden");
  }
}

async function getDashboard() {
  const response = await fetch(`${API_URL}/dashboard`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username: currentUsername }),
  });
  const data = await response.json();

  if (response.ok) {
    streakLine.textContent = `🔥 Streak: ${data.streak} days | 🧮 Total Workouts: ${data.total_workouts}`;

    achievementsList.innerHTML = "";
    data.achievements.forEach(ach => {
      const li = document.createElement("li");
      li.textContent = `🏆 ${ach}`;
      achievementsList.appendChild(li);
    });

    const ctx = document.getElementById('progressChart').getContext('2d');
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.history,
        datasets: [{
          label: 'Workouts Completed',
          data: data.history.map(() => 1),
          backgroundColor: 'rgba(54, 162, 235, 0.5)',
          borderColor: 'rgba(54, 162, 235, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              stepSize: 1
            }
          }
        }
      }
    });
  } else {
    showPopup(data.error);
  }
}
