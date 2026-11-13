import os
import django
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_backend.settings")
django.setup()

from screening.models import Resume

print(f"Total resumes in DB: {Resume.objects.count()}")
