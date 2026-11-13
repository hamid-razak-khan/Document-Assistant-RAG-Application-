import requests

# Test the clear history endpoint
try:
    response = requests.delete("http://localhost:8000/api/screening/history/clear/")
    print(f"Clear History Status Code: {response.status_code}")
    print(f"Clear History Response: {response.text}")
except Exception as e:
    print(f"Clear History Error: {e}")