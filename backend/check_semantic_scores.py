# Test to check if semantic scores are returning 0
import os
from dotenv import load_dotenv
load_dotenv()

# Set up Django
import sys
import django
from django.conf import settings

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.rag_pipeline import compute_scores, semantic_score_for_resume

def test_scores():
    # Test data
    job_text = 'Python developer with experience in Django and React'
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    # Compute TF-IDF scores
    keyword_scores = compute_scores(job_text, resume_texts)
    print("TF-IDF scores:", keyword_scores)
    
    # Test semantic scores with dummy resume IDs
    print("\nTesting semantic scores with dummy IDs:")
    for i, resume_text in enumerate(resume_texts):
        # Since we don't have actual resumes in the DB, we'll test with ID 1
        # This should return 0 since there's no matching resume
        sem_score = semantic_score_for_resume(job_text, i+1)
        print(f"Resume ID {i+1}: Semantic score = {sem_score}")

if __name__ == "__main__":
    test_scores()