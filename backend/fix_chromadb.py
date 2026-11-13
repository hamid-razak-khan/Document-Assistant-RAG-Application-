import os
import django
import shutil
import time

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "resume_backend.settings")
django.setup()

from screening.models import Resume
from screening.rag_pipeline import preprocess_and_chunk, get_vector_db
from langchain_core.documents import Document
from uuid import uuid4

print("Rebuilding ChromaDB from existing resumes in SQLite database...")
vector_db = get_vector_db()

resumes = Resume.objects.all()
total = resumes.count()

chunked_count = 0
for i, r in enumerate(resumes):
    if not r.text:
        print(f"Skipping resume ID {r.id} (no text)")
        continue
        
    docs = [Document(page_content=r.text)]
    for d in docs:
        d.metadata = {
            "job_id": str(r.job_id),
            "resume_id": str(r.id),
            "filename": str(r.filename),
        }
    
    chunks = preprocess_and_chunk(docs)
    for c in chunks:
        c.metadata["chunk_id"] = str(uuid4())
        
    if chunks:
        vector_db.add_documents(chunks)
        chunked_count += 1
        
    if i > 0 and i % 10 == 0:
        print(f"Processed {i}/{total} resumes")
        
vector_db.persist()
print(f"Successfully rebuilt vector index for {chunked_count} resumes!")
