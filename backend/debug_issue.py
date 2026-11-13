import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.models import JobDescription, Resume
from screening.rag_pipeline import rank_resumes

def reproduce_issue():
    print("=== Reproducing Issue with Real Data ===")
    
    # Get the latest job
    job = JobDescription.objects.last()
    if not job:
        print("No jobs found in DB.")
        return

    print(f"Using Job ID: {job.id}")
    print(f"Job Title: {job.title}")
    print(f"Job Text Length: {len(job.text)}")
    print(f"Job Text Preview: {job.text[:100]!r}")
    
    # Get resumes for this job
    resumes_qs = job.resumes.all()
    print(f"Found {resumes_qs.count()} resumes for this job.")
    
    if not resumes_qs.exists():
        print("No resumes for this job.")
        return

    resumes = [
        {"id": r.id, "filename": r.filename, "text": r.text}
        for r in resumes_qs
    ]
    
    # Run ranking
    print("\nRunning rank_resumes...")
    ranked = rank_resumes(job.text, resumes)
    
    print("\nResults:")
    for r in ranked[:5]:  # Show top 5
        print(f"Filename: {r['filename']}")
        print(f"Keyword Score: {r['keyword_score']}")
        print(f"Semantic Score: {r['semantic_score']}")
        print(f"Final Score: {r['final_score']}")
        print("-" * 20)

if __name__ == "__main__":
    reproduce_issue()
