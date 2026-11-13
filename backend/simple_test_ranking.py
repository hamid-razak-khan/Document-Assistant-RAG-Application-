from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def test():
    print("Starting test...")
    corpus = [
        "Python developer with Django",
        "Java developer",
        "Python developer"
    ]
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(corpus)
    sims = cosine_similarity(tfidf[0:1], tfidf[1:])[0]
    print(f"Scores: {sims}")

if __name__ == "__main__":
    test()
