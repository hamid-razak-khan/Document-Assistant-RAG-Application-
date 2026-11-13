import sys
import os
import django
from django.conf import settings

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.rag_pipeline import summarize_with_llm

# Test data
job_description = """
We are looking for a Senior Python Developer with experience in Django, REST APIs, and cloud platforms.
Required skills: Python, Django, REST API, AWS, Docker, PostgreSQL, Git
Preferred skills: React, Kubernetes, CI/CD, Machine Learning
"""

resume_text = """
John Doe
Senior Software Engineer

Experience:
- 5 years of Python development
- Django REST framework expert
- AWS certified developer
- Docker containerization specialist
- PostgreSQL database design
- Git version control

Projects:
- Built scalable REST APIs using Django
- Containerized applications with Docker
- Deployed services on AWS EC2 and S3
"""

# Test the LLM function
result = summarize_with_llm(job_description, resume_text)
print("LLM Response:")
print(result)