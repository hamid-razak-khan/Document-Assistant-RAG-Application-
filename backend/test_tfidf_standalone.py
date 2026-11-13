# Standalone test for TF-IDF computation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_scores(job_text: str, resume_texts: list):
    print(f"Computing TF-IDF scores for job: {job_text[:50]}...")
    print(f"Number of resumes: {len(resume_texts)}")
    corpus = [job_text] + resume_texts
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    scores = sims.tolist()
    print(f"TF-IDF scores: {scores}")
    return scores

if __name__ == "__main__":
    # Test data
    job_text = 'Python developer with experience in Django and React'
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    scores = compute_scores(job_text, resume_texts)
    print("Final scores:", scores)
    print("Scores (0-100):", [score * 100 for score in scores])