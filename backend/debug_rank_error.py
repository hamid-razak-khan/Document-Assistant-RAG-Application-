import os
import django
import sys
import traceback

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_backend.settings")
django.setup()

from screening.views import process_screening
from django.test import RequestFactory
from screening.models import JobDescription

def test():
    # Assuming there's a job ID. If 49 doesn't exist, we just find the first one.
    job = JobDescription.objects.last()
    if not job:
        print("No jobs found")
        return
        
    print(f"Testing ranking for job ID {job.id}")
    factory = RequestFactory()
    request = factory.post(f"/api/screening/jobs/{job.id}/rank/")
    
    try:
        response = process_screening(request, job_id=job.id)
        print(f"Status code: {response.status_code}")
    except Exception as e:
        traceback.print_exc()

if __name__ == "__main__":
    test()
