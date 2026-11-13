# Simple test to debug the scoring issue
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_scores(job_text: str, resume_texts: list):
    corpus = [job_text] + resume_texts
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    return sims.tolist()

# Test data
job_text = 'Python developer with experience in Django and React'
resume_texts = [
    'Experienced Python developer with Django skills',
    'Java developer with Spring framework experience',
    'Full stack developer with Python, Django, and React skills'
]

# Compute scores
keyword_scores = compute_scores(job_text, resume_texts)
print("Raw TF-IDF scores (0-1):", keyword_scores)
print("TF-IDF scores (0-100):", [score * 100 for score in keyword_scores])

# Test semantic scores (simulated)
semantic_scores = [0.43, 0.30, 0.61]

print("\nCombined scoring:")
for i, (kw, sem) in enumerate(zip(keyword_scores, semantic_scores)):
    kw_100 = kw * 100
    sem_100 = sem * 100
    algo_score = 0.6 * sem_100 + 0.4 * kw_100
    print(f"Resume {i+1}:")
    print(f"  Keyword score (0-1): {kw:.4f}")
    print(f"  Keyword score (0-100): {kw_100:.2f}")
    print(f"  Semantic score (0-1): {sem:.4f}")
    print(f"  Semantic score (0-100): {sem_100:.2f}")
    print(f"  Algorithmic score: {algo_score:.2f}")
    print()