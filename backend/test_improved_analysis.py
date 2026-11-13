# Test to verify the improved analysis
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

from screening.rag_pipeline import compute_scores, semantic_score_for_resume

def test_algorithmic_scores():
    # Test data
    job_text = 'Data Scientist with Python, machine learning, TensorFlow, PyTorch, scikit-learn, statistical analysis, data visualization, SQL, big data, Computer Science, Statistics, PhD, Master\'s degree'
    resume_texts = [
        'Experienced Data Scientist with Python, machine learning, TensorFlow, PyTorch, scikit-learn, statistical analysis, data visualization, SQL, big data, Computer Science, Statistics',
        # This resume is missing PhD and Master's degree
    ]
    
    print("Testing algorithmic scores...")
    print(f"Job text: {job_text}")
    print(f"Number of resumes: {len(resume_texts)}")
    
    # Test TF-IDF scores
    tfidf_scores = compute_scores(job_text, resume_texts)
    print(f"TF-IDF scores: {tfidf_scores}")
    
    # Test semantic scores (these will be 0 since we don't have actual resumes in the DB)
    # But the function should work correctly
    print("TF-IDF computation successful!")
    
    print("\nResults:")
    for i, (resume_text, score) in enumerate(zip(resume_texts, tfidf_scores)):
        print(f"  Resume {i+1}:")
        print(f"    Score: {score}")
        print(f"    Score (0-100): {score * 100}")
        print()

if __name__ == "__main__":
    test_algorithmic_scores()