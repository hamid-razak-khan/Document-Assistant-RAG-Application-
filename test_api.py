import requests
import json

# Test if the API is reachable
try:
    response = requests.get("http://localhost:8000/api/screening/jobs/1/resumes/list/")
    print(f"GET Status Code: {response.status_code}")
    print(f"GET Response: {response.text}")
except Exception as e:
    print(f"GET Error: {e}")

# Test POST request
try:
    data = {"title": "Test Job", "text": "Looking for a software engineer with Python experience"}
    response = requests.post("http://localhost:8000/api/screening/jobs/", json=data)
    print(f"POST Status Code: {response.status_code}")
    print(f"POST Response: {response.text}")
except Exception as e:
    print(f"POST Error: {e}")