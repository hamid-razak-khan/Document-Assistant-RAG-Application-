import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.models import Resume, JobDescription

def check_db_content():
    print("=== Checking Database Content ===")
    
    jobs = JobDescription.objects.all()
    print(f"Total Jobs: {jobs.count()}")
    
    resumes = Resume.objects.all()
    print(f"Total Resumes: {resumes.count()}")
    
    for r in resumes:
        print(f"\nResume ID: {r.id}")
        print(f"Filename: {r.filename}")
        print(f"Text Length: {len(r.text)}")
        if len(r.text) < 100:
            print(f"Text Content: {r.text!r}")
        else:
            print(f"Text Content (first 100 chars): {r.text[:100]!r}")

if __name__ == "__main__":
    check_db_content()
