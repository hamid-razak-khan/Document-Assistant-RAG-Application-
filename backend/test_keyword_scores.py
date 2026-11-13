# Test to verify keyword scores calculation
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# Add the project directory to the path
sys.path.append(os.path.abspath('.'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
import django
django.setup()

from screening.rag_pipeline import compute_scores

def test_keyword_scores():
    # Test data
    job_text = 'Python developer with experience in Django and React'
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    print("Testing keyword scores calculation...")
    print(f"Job text: {job_text}")
    print(f"Number of resumes: {len(resume_texts)}")
    
    scores = compute_scores(job_text, resume_texts)
    
    print("\nResults:")
    for i, (resume_text, score) in enumerate(zip(resume_texts, scores)):
        print(f"  Resume {i+1}:")
        print(f"    Text: {resume_text}")
        print(f"    Score: {score}")
        print(f"    Score (0-100): {score * 100}")
        print()

if __name__ == "__main__":
    test_keyword_scores()