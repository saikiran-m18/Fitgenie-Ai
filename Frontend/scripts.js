const API_URL = "http://127.0.0.1:5000";

/* Section switching */
function showSection(id){
  document.getElementById("auth-section").classList.add("hidden");
  document.getElementById("plan-section").classList.add("hidden");
  document.getElementById(id).classList.remove("hidden");
}

window.addEventListener("DOMContentLoaded", () => {
  const token = localStorage.getItem("token");
  const username = localStorage.getItem("username");
  if (token && username) {
    document.getElementById("user-name").innerText = username;
    showSection("plan-section");
  } else {
    showSection("auth-section");
  }
});

function clearFields(){
  document.getElementById("username").value="";
  document.getElementById("password").value="";
}

/* Popup functions */
function showPopup(message){
  document.getElementById("popup-message").innerText = message;
  document.getElementById("popup").classList.remove("hidden");
}
function closePopup(){
  document.getElementById("popup").classList.add("hidden");
}

/* Register */
async function register(){
  const username=document.getElementById("username").value.trim();
  const password=document.getElementById("password").value;
  if(!username || !password){return showPopup("Enter username & password");}

  const res=await fetch(`${API_URL}/register`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,password})
  });
  const data=await res.json();
  showPopup(data.msg || "Registered successfully ✅");
}

/* Login */
async function login(){
  const username=document.getElementById("username").value.trim();
  const password=document.getElementById("password").value;
  if(!username || !password){return showPopup("Enter username & password");}

  const res=await fetch(`${API_URL}/login`,{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({username,password})
  });
  const data=await res.json();
  if(data.access_token){
    localStorage.setItem("token", data.access_token);
    localStorage.setItem("username", username);
    document.getElementById("user-name").innerText = username;
    showSection("plan-section");
  }else{
    showPopup(data.msg || "❌ Invalid username or password");
  }
}

function logout(){
  localStorage.removeItem("token");
  localStorage.removeItem("username");
  showSection("auth-section");
}

/* Get Plan */
async function getPlan(){
  const token=localStorage.getItem("token");
  if(!token) return showPopup("Please login first");

  const goal=document.getElementById("goal").value;
  const days=parseInt(document.getElementById("days").value || "6",10);
  const loader=document.getElementById("loader");
  loader.classList.remove("hidden");

  try{
    const res=await fetch(`${API_URL}/recommend`,{
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        "Authorization":"Bearer "+token
      },
      body:JSON.stringify({goal, days})
    });
    const data=await res.json();

    const weekDays=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const split=["Chest","Back","Legs","Biceps","Triceps","Shoulders"];
    const icons={Chest:"💪",Back:"🦾",Legs:"🦵",Biceps:"💥",Triceps:"🔥",Shoulders:"🏋️"};

    const rows = [];
    for(let i=0;i<Math.min(days,6);i++){
      rows.push(
        `<tr class="fade-stagger" style="animation-delay:${i*120}ms">
           <td>${weekDays[i]}</td>
           <td>${icons[split[i]]} ${split[i]}</td>
         </tr>`
      );
    }

    const workoutTable = `
      <h3>Weekly Workout Plan 🏋️</h3>
      <table class="workout-table animated">
        <thead><tr><th>Day</th><th>Workout Focus</th></tr></thead>
        <tbody>${rows.join("")}</tbody>
      </table>
    `;
    document.getElementById("workout").innerHTML = workoutTable;

    const dietImages=["🍳","🥗","🍲","🥤","🍎","🥘"];
    const dietHtml = `
      <div class="diet-card">
        <h3>Diet Plan 🥗</h3>
        ${data.diet.map((line,i)=>`
          <p class="diet-item" style="animation-delay:${i*120}ms">
            ${dietImages[i % dietImages.length]} ${line}
          </p>`).join("")}
      </div>
    `;
    document.getElementById("diet").innerHTML = dietHtml;

  } catch (e){
    showPopup("⚠️ Could not fetch plan. Is the backend running?");
  } finally{
    loader.classList.add("hidden");
  }
}

function refreshPlan(){ getPlan(); }
