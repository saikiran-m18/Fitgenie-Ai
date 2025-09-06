import requests

url = "http://127.0.0.1:5000/recommend"
data = {"goal": "weight_loss", "days": 5, "username": "testuser"}

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)
