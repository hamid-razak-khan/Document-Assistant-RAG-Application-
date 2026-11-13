import os
from dotenv import load_dotenv
load_dotenv()

# Test TF-IDF computation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_scores(job_text: str, resume_texts: list) -> list:
    corpus = [job_text] + resume_texts
    tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    return sims.tolist()

if __name__ == "__main__":
    job_text = 'Python developer with experience in Django and React'
    resume_texts = [
        'Experienced Python developer with Django skills',
        'Java developer with Spring framework experience',
        'Full stack developer with Python, Django, and React skills'
    ]
    
    scores = compute_scores(job_text, resume_texts)
    print('TF-IDF similarities:', scores)
    print('Scores (0-100):', [round(score * 100, 2) for score in scores])