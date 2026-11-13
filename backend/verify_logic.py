import re
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def compute_scores(job_text: str, resume_texts: List[str]) -> List[float]:
    print(f"DEBUG: compute_scores called with {len(resume_texts)} resumes")
    
    # Pre-processing helper
    def tokenize(text):
        return set(re.findall(r"\w+", text.lower()))

    job_tokens = tokenize(job_text)
    
    # Fallback Jaccard Calculation
    def calculate_jaccard(text):
        tokens = tokenize(text)
        if not job_tokens or not tokens:
            return 0.0
        intersection = job_tokens.intersection(tokens)
        union = job_tokens.union(tokens)
        return len(intersection) / len(union) if union else 0.0

    scores = []
    
    # Try TF-IDF first
    try:
        corpus = [job_text] + resume_texts
        tfidf = TfidfVectorizer(stop_words="english").fit_transform(corpus)
        sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
        scores = sims.tolist()
        print(f"DEBUG: TF-IDF scores calculated: {scores}")
    except Exception as e:
        print(f"DEBUG: TF-IDF failed: {e}. Switching to Jaccard fallback.")
        scores = [0.0] * len(resume_texts)

    # Apply Fallback if score is 0.0
    final_scores = []
    for i, score in enumerate(scores):
        if score <= 0.001:  # If TF-IDF is 0 or very low, try Jaccard
            jaccard = calculate_jaccard(resume_texts[i])
            print(f"DEBUG: Resume {i} score 0.0 -> Jaccard fallback: {jaccard}")
            final_scores.append(jaccard)
        else:
            final_scores.append(score)
            
    return final_scores

if __name__ == "__main__":
    job = "python developer django"
    resumes = [
        "python developer with django skills",
        "java developer",
        "python but no django"
    ]
    
    print("Testing compute_scores...")
    scores = compute_scores(job, resumes)
    print("Final Scores:", scores)
    
    # Verify scores are not 0.0 for relevant resumes
    assert scores[0] > 0, "Resume 1 should have score > 0"
    assert scores[2] > 0, "Resume 3 should have score > 0"
    print("Verification PASSED!")
