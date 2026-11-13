#!/usr/bin/env python
"""
Test script to verify that the resume upload functionality is working correctly.
"""

import requests
import json
import time

def test_upload():
    # Base URL for the API
    base_url = "http://127.0.0.1:8000/api/screening"
    
    # Step 1: Create a test job
    print("Creating test job...")
    job_data = {
        "title": "Software Engineer Test Position",
        "text": "We are looking for a software engineer with experience in Python, Django, and REST APIs. Required skills: Python, Django, REST API, AWS, Docker, PostgreSQL, Git. Preferred skills: React, Kubernetes, CI/CD, Machine Learning."
    }
    
    try:
        job_response = requests.post(f"{base_url}/jobs/", json=job_data, timeout=10)
        job_response.raise_for_status()
        job_id = job_response.json()["id"]
        print(f"Created job with ID: {job_id}")
    except Exception as e:
        print(f"Error creating job: {e}")
        return
    
    # Step 2: Test single file upload
    print("\nTesting single file upload...")
    try:
        with open("test_resume.txt", "rb") as f:
            files = {"files": f}
            upload_response = requests.post(
                f"{base_url}/jobs/{job_id}/resumes/", 
                files=files,
                timeout=60  # 60 second timeout for file upload
            )
            upload_response.raise_for_status()
            print("Single file upload successful!")
            print(f"Response: {upload_response.json()}")
    except Exception as e:
        print(f"Error uploading single file: {e}")
        return
    
    # Step 3: Test multiple file upload
    print("\nTesting multiple file upload...")
    try:
        with open("test_resume.txt", "rb") as f1, open("test_resume2.txt", "rb") as f2:
            files = [
                ("files", ("test_resume1.txt", f1, "text/plain")),
                ("files", ("test_resume2.txt", f2, "text/plain"))
            ]
            upload_response = requests.post(
                f"{base_url}/jobs/{job_id}/resumes/", 
                files=files,
                timeout=60  # 60 second timeout for file upload
            )
            upload_response.raise_for_status()
            print("Multiple file upload successful!")
            print(f"Response: {upload_response.json()}")
    except Exception as e:
        print(f"Error uploading multiple files: {e}")
        return
    
    # Step 4: List uploaded resumes
    print("\nListing uploaded resumes...")
    try:
        list_response = requests.get(f"{base_url}/jobs/{job_id}/resumes/list/", timeout=10)
        list_response.raise_for_status()
        resumes = list_response.json()
        print(f"Found {len(resumes)} uploaded resumes:")
        for resume in resumes:
            print(f"  - {resume['filename']} (ID: {resume['id']})")
    except Exception as e:
        print(f"Error listing resumes: {e}")
        return
    
    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_upload()