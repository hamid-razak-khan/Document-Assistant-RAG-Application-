import requests
import json

# Create a test job
url = "http://localhost:8000/api/screening/jobs/"
data = {
    "title": "Test Job",
    "text": "Looking for a software engineer with Python experience"
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    if response.status_code == 201:
        job_data = response.json()
        print(f"Created job ID: {job_data['id']}")
except Exception as e:
    print(f"Error: {e}")