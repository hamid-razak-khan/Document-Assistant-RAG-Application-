import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_backend.settings')
django.setup()

from screening.models import JobDescription
from screening.rag_pipeline import load_resume_document

def debug_pdf_extraction():
    print("=== Debugging PDF Extraction ===")
    
    job = JobDescription.objects.get(pk=40)
    resumes = job.resumes.all()
    
    for r in resumes:
        print(f"\nProcessing Resume ID: {r.id}")
        print(f"Filename: {r.filename}")
        print(f"File Path: {r.file.path}")
        
        if not os.path.exists(r.file.path):
            print("ERROR: File does not exist!")
            continue
            
        try:
            docs = load_resume_document(r.file.path)
            full_text = "\n".join([d.page_content for d in docs])
            print(f"Extracted Text Length: {len(full_text)}")
            if len(full_text) < 100:
                print(f"Text Content: {full_text!r}")
            else:
                print(f"Text Content (first 100 chars): {full_text[:100]!r}")
        except Exception as e:
            print(f"ERROR extracting text: {e}")

if __name__ == "__main__":
    debug_pdf_extraction()
