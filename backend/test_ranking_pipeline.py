# Test to verify the ranking pipeline
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

from screening.rag_pipeline import rank_resumes

def test_ranking_pipeline():
    # Test data
    job_text = 'Python developer with experience in Django and React'
    resumes = [
        {
            "id": 1,
            "filename": "resume1.pdf",
            "text": "Experienced Python developer with Django skills"
        },
        {
            "id": 2,
            "filename": "resume2.pdf",
            "text": "Java developer with Spring framework experience"
        },
        {
            "id": 3,
            "filename": "resume3.pdf",
            "text": "Full stack developer with Python, Django, and React skills"
        }
    ]
    
    print("Testing ranking pipeline...")
    print(f"Job text: {job_text}")
    print(f"Number of resumes: {len(resumes)}")
    
    results = rank_resumes(job_text, resumes)
    
    print("\nResults:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['filename']}")
        print(f"     Keyword Score: {result['keyword_score']}")
        print(f"     Semantic Score: {result['semantic_score']}")
        print(f"     Algorithmic Score: {result['algorithmic_score']}")
        print(f"     Final Score: {result['final_score']}")
        print()

if __name__ == "__main__":
    test_ranking_pipeline()