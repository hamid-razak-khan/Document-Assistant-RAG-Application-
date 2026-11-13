import requests

# Test single file upload
url = "http://127.0.0.1:8000/api/screening/jobs/25/resumes/"

# Open single file
files = {'files': open('test_resume.txt', 'rb')}

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
finally:
    files['files'].close()