import requests

response = requests.post(
    "http://localhost:5000/api/process",
    json={
        "text": "Show me sales data for Q1 2023",
        "session_id": "user123"
    }
)

print(response.json())
