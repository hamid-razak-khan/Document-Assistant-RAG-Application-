#!/usr/bin/env python
import os
import sys
import django
from django.conf import settings

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.rag_pipeline import rank_resumes

# Sample job description
job_description = """
We are looking for a Senior Software Engineer with expertise in Python, Django, and React.
Required skills:
- Python programming
- Django framework
- React.js
- PostgreSQL
- RESTful APIs
- Git version control
- Agile development methodologies
"""

# Sample resumes
resumes = [
    {
        "id": 1,
        "filename": "john_doe_resume.pdf",
        "text": """
        John Doe
        Senior Software Engineer
        
        Experience:
        - 5 years of Python development
        - 3 years of Django experience
        - 2 years of React development
        - PostgreSQL database design
        - REST API development
        - Git workflow
        - Scrum methodology
        
        Skills:
        - Python
        - Django
        - React
        - PostgreSQL
        - REST APIs
        - Git
        - Agile
        """
    },
    {
        "id": 2,
        "filename": "jane_smith_resume.pdf",
        "text": """
        Jane Smith
        Software Developer
        
        Experience:
        - 2 years of Python programming
        - 1 year of Django experience
        - JavaScript development
        - MySQL databases
        - API integration
        
        Skills:
        - Python
        - Django
        - JavaScript
        - MySQL
        - APIs
        """
    }
]

if __name__ == "__main__":
    print("Testing ranking functionality...")
    results = rank_resumes(job_description, resumes)
    
    print("\nRanking Results:")
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['filename']}")
        print(f"   Final Score: {result['final_score']}")
        print(f"   Keyword Score: {result['keyword_score']}")
        print(f"   Semantic Score: {result['semantic_score']}")
        print(f"   Algorithmic Score: {result['algorithmic_score']}")