# Simple TF-IDF test
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Test data
job_text = 'Python developer with experience in Django and React'
resume_texts = [
    'Experienced Python developer with Django skills',
    'Java developer with Spring framework experience',
    'Full stack developer with Python, Django, and React skills'
]

print("Testing TF-IDF computation...")
print(f"Job text: {job_text}")
print(f"Number of resumes: {len(resume_texts)}")

try:
    corpus = [job_text] + resume_texts
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    scores = sims.tolist()
    print(f"TF-IDF scores: {scores}")
    print("TF-IDF computation successful!")
except Exception as e:
    print(f"TF-IDF computation failed: {e}")
    scores = [0.0] * len(resume_texts)

print("\nResults:")
for i, (resume_text, score) in enumerate(zip(resume_texts, scores)):
    print(f"  Resume {i+1}:")
    print(f"    Text: {resume_text}")
    print(f"    Score: {score}")
    print(f"    Score (0-100): {score * 100}")
    print()