import os
import django

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

# Test if Django is set up correctly
from django.conf import settings
print("Django settings loaded successfully")
print(f"GROQ API Key: {settings.GROQ_API_KEY}")
print(f"GROQ Model Name: {settings.GROQ_MODEL_NAME}")