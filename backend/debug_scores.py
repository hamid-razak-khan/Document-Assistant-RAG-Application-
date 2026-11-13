import os
from dotenv import load_dotenv
load_dotenv()

# Import the functions from rag_pipeline
import sys
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')

import django
django.setup()

from screening.rag_pipeline import compute_scores, semantic_score_for_resume
from screening.models import JobDescription, Resume

def debug_scores():
    # Create a test job and resumes
    job_text = 'Python developer with experience in Django and React'
    
    # Simulate resume texts
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    # Compute TF-IDF scores
    keyword_scores = compute_scores(job_text, resume_texts)
    print("TF-IDF scores:", keyword_scores)
    print("TF-IDF scores (0-100):", [score * 100 for score in keyword_scores])
    
    # For semantic scores, we would need actual resumes in the database
    # Let's just test the formula
    semantic_scores = [0.43, 0.30, 0.61]  # Example scores
    
    print("\nCombined scoring:")
    for i, (kw, sem) in enumerate(zip(keyword_scores, semantic_scores)):
        kw_100 = kw * 100
        sem_100 = sem * 100
        algo_score = 0.6 * sem_100 + 0.4 * kw_100
        print(f"Resume {i+1}:")
        print(f"  Keyword score (0-1): {kw:.4f}")
        print(f"  Keyword score (0-100): {kw_100:.2f}")
        print(f"  Semantic score (0-1): {sem:.4f}")
        print(f"  Semantic score (0-100): {sem_100:.2f}")
        print(f"  Algorithmic score: {algo_score:.2f}")
        print()

if __name__ == "__main__":
    debug_scores()