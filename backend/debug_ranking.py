# Debug script to check the ranking pipeline
import os
from dotenv import load_dotenv
load_dotenv()

# Set up Django
import sys
import django
from django.conf import settings

# Add the project directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.rag_pipeline import compute_scores, semantic_score_for_resume

def debug_ranking():
    # Test data
    job_text = 'Python developer with experience in Django and React'
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    print("=== DEBUGGING RANKING PIPELINE ===")
    
    # Compute TF-IDF scores
    print("\n1. Computing TF-IDF scores:")
    keyword_scores = compute_scores(job_text, resume_texts)
    for i, score in enumerate(keyword_scores):
        print(f"  Resume {i+1}: {score:.6f} ({score*100:.2f})")
    
    # Test semantic scores with dummy resume IDs (these will likely return 0)
    print("\n2. Computing semantic scores (with dummy IDs):")
    semantic_scores = []
    for i in range(len(resume_texts)):
        sem_score = semantic_score_for_resume(job_text, i+1)  # Dummy IDs
        semantic_scores.append(sem_score)
        print(f"  Resume {i+1}: {sem_score:.6f} ({sem_score*100:.2f})")
    
    # Calculate algorithmic scores
    print("\n3. Calculating algorithmic scores:")
    for i, (kw, sem) in enumerate(zip(keyword_scores, semantic_scores)):
        kw_100 = kw * 100
        sem_100 = sem * 100
        algo_score = 0.6 * sem_100 + 0.4 * kw_100
        print(f"  Resume {i+1}:")
        print(f"    Keyword: {kw_100:.2f}")
        print(f"    Semantic: {sem_100:.2f}")
        print(f"    Algorithmic (0.6*{sem_100:.2f} + 0.4*{kw_100:.2f}): {algo_score:.2f}")

if __name__ == "__main__":
    debug_ranking()