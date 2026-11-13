import re
from typing import List

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
    
    # Simulate TF-IDF failure
    print(f"DEBUG: TF-IDF failed (Simulated). Switching to Jaccard fallback.")
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
    
    print("Testing compute_scores (Fallback Only)...")
    scores = compute_scores(job, resumes)
    print("Final Scores:", scores)
    
    # Verify scores are not 0.0 for relevant resumes
    assert scores[0] > 0, "Resume 1 should have score > 0"
    assert scores[2] > 0, "Resume 3 should have score > 0"
    print("Verification PASSED!")
