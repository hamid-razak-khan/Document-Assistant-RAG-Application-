import re
import json
import time
import hashlib
from pathlib import Path
from typing import List, Dict, Any
from uuid import uuid4

import numpy as np
from django.conf import settings

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.embeddings import Embeddings

from chromadb.config import Settings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# 1. Simple Hash Embeddings (No PyTorch, No Heavy Deps)
# ============================================================

class SimpleHashEmbeddings(Embeddings):
    def __init__(self, dim: int = 512):
        self.dim = dim

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"\w+", text.lower())

    def _token_hash_index(self, token: str) -> int:
        h = hashlib.md5(token.encode("utf-8")).hexdigest()
        return int(h, 16) % self.dim

    def _embed(self, text: str) -> List[float]:
        vec = np.zeros(self.dim, dtype=np.float32)
        for tok in self._tokenize(text):
            vec[self._token_hash_index(tok)] += 1.0

        norm = np.linalg.norm(vec)
        if norm > 0:
            vec /= norm

        return vec.tolist()

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed(text)


EMBEDDINGS = None


def get_embeddings():
    """Lazy initialization of embeddings to prevent pickling issues during Django startup"""
    global EMBEDDINGS
    if EMBEDDINGS is None:
        EMBEDDINGS = SimpleHashEmbeddings(dim=512)
    return EMBEDDINGS


# ============================================================
# 2. Chroma Vector DB
# ============================================================

VECTOR_DB = None


def get_vector_db():
    """Lazy initialization of vector DB to prevent pickling issues during Django startup"""
    global VECTOR_DB
    if VECTOR_DB is None:
        CHROMA_DIR = Path(settings.CHROMA_DB_DIR)
        CHROMA_DIR.mkdir(exist_ok=True)
        VECTOR_DB = Chroma(
            collection_name="resumes",
            embedding_function=get_embeddings(),
            persist_directory=str(CHROMA_DIR),
            client_settings=Settings(
                allow_reset=True,
                anonymized_telemetry=False,
            ),
        )
    return VECTOR_DB


# ============================================================
# 3. Groq LLM (Lazy Initialization to prevent pickling issues)
# ============================================================

LLM = None


def get_llm():
    """Lazy initialization of LLM to prevent pickling issues during Django startup"""
    global LLM
    if LLM is None:
        LLM = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model_name=settings.GROQ_MODEL_NAME,
            temperature=0.2,
        )
    return LLM


# ============================================================
# 4. Resume Loader (Fixed for DOCX)
# ============================================================

def load_resume_document(file_path: str):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        loader = PyPDFLoader(file_path)
        return loader.load()

    elif ext in [".doc", ".docx"]:
        # FIXED DOCX LOADER (Docx2txt was returning empty docs)
        import docx2txt
        text = docx2txt.process(file_path)
        return [Document(page_content=text)]

    else:
        loader = TextLoader(file_path, encoding="utf-8")
        return loader.load()


# ============================================================
# 5. Chunking
# ============================================================

def preprocess_and_chunk(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        add_start_index=True,
    )
    return splitter.split_documents(docs)


# ============================================================
# 6. Index Resume (Fully fixed)
# ============================================================

def index_resume(job_id: int, resume_id: int, filename: str, file_path: str) -> str:
    print(f"\n=== Indexing Resume: {filename} ===")

    docs = load_resume_document(file_path)
    print(f"Loaded {len(docs)} pages")

    full_text = "\n".join([d.page_content for d in docs])
    print(f"Extracted text length: {len(full_text)}")

    # FIX 1: Ensure metadata values are STRINGS
    for d in docs:
        d.metadata = {
            "job_id": str(job_id),
            "resume_id": str(resume_id),
            "filename": str(filename),
        }

    chunks = preprocess_and_chunk(docs)
    print(f"Created {len(chunks)} chunks")

    # FIX 2: Ensure unique chunk IDs (prevents Chroma duplicate errors)
    for c in chunks:
        c.metadata["chunk_id"] = str(uuid4())

    vector_db = get_vector_db()
    vector_db.add_documents(chunks)

    print("Resume indexed successfully.\n")
    return full_text


# ============================================================
# 7. TF-IDF Keyword Matching
# ============================================================

def compute_scores(job_text: str, resume_texts: List[str]) -> List[float]:
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
    except Exception as e:
        print(f"TF-IDF computation failed: {e}. Switching to Jaccard fallback.")
        scores = [0.0] * len(resume_texts)

    # Apply Fallback if score is 0.0
    final_scores = []
    for i, score in enumerate(scores):
        if score <= 0.001:  # If TF-IDF is 0 or very low, try Jaccard
            jaccard = calculate_jaccard(resume_texts[i])
            final_scores.append(jaccard)
        else:
            final_scores.append(score)
            
    return final_scores


# ============================================================
# 8. Semantic Similarity (Chroma)
# ============================================================

def semantic_score_for_resume(job_text: str, resume_id: int) -> float:
    vector_db = get_vector_db()
    results = vector_db.similarity_search_with_score(
        query=job_text,
        k=5,
        filter={"resume_id": str(resume_id)},  # FIXED filter type
    )

    if not results:
        return 0.0

    distances = [d for _, d in results]
    sims = [1 / (1 + d) for d in distances]
    return float(sum(sims) / len(sims))


# ============================================================
# 9. LLM Response Parser
# ============================================================

import re


def parse_llm_response(response_text: str) -> Dict[str, Any]:
    """
    Parse the LLM response text according to the specified format.
    """
    # Initialize default values
    result = {
        "summary": "",
        "matching_skills": [],
        "missing_skills": [],
        "rating": 0,
    }
    
    # Split the response into sections
    sections = response_text.split('\n\n')
    
    for section in sections:
        section = section.strip()
        if section.startswith('Summary:'):
            result["summary"] = section.replace('Summary:', '', 1).strip()
        elif section.startswith('Extracted Resume Skills:'):
            # Skip this section as we don't need to return it
            pass
        elif section.startswith('JD Required Skills:'):
            # Skip this section as we don't need to return it
            pass
        elif section.startswith('Matching Skills:'):
            skills_text = section.replace('Matching Skills:', '', 1).strip()
            if skills_text and skills_text != "None identified":
                # Split by newlines and clean up
                skills = [skill.strip().lstrip('•- ').strip() for skill in skills_text.split('\n') if skill.strip()]
                result["matching_skills"] = [skill for skill in skills if skill]
        elif section.startswith('Missing Skills:'):
            skills_text = section.replace('Missing Skills:', '', 1).strip()
            if skills_text and skills_text != "None identified":
                # Split by newlines and clean up
                skills = [skill.strip().lstrip('•- ').strip() for skill in skills_text.split('\n') if skill.strip()]
                result["missing_skills"] = [skill for skill in skills if skill]
        elif section.startswith('Keyword Score:'):
            # Extract scores from the section
            keyword_match = re.search(r'Keyword Score:\s*(\d+)', section)
            semantic_match = re.search(r'Semantic Score:\s*(\d+)', section)
            final_match = re.search(r'Final Score:\s*(\d+)', section)
            
            if keyword_match:
                result["keyword_score"] = int(keyword_match.group(1))
            if semantic_match:
                result["semantic_score"] = int(semantic_match.group(1))
            if final_match:
                result["rating"] = int(final_match.group(1))
    
    return result


# ============================================================
# 10. LLM Summary (Stable)
# ============================================================

def summarize_with_llm(job_text: str, resume_text: str) -> Dict[str, Any]:
    resume_crop = resume_text[:2000]  # limit for safety

    prompt = f"""
You are an AI Resume Analyzer. You will receive a Job Description (JD) and Resume Text.

IMPORTANT INSTRUCTIONS:
- ONLY extract skills that are EXPLICITLY mentioned in the provided text
- DO NOT invent or hallucinate skills that are not in the text
- If a skill is not clearly stated, DO NOT include it
- Base ALL your analysis on the actual text provided

TASKS TO PERFORM:

1. Extract skills EXPLICITLY mentioned in the resume (programming languages, tools, ML skills, cloud, frameworks, analytics, soft skills, etc.)

2. Extract skills EXPLICITLY required in the Job Description

3. Identify:
   • Matching Skills (skills explicitly mentioned in BOTH resume and JD)
   • Missing Skills (skills explicitly required in JD but NOT found in resume)

SCORING GUIDELINES:

- Keyword Score (0–100):
  Count the matching skills and divide by total JD skills, then multiply by 100
  Formula: (Matching skills ÷ Total JD skills) × 100

- Semantic Score (0–100):
  Rate how well the resume content aligns with the JD based on actual experience, projects, tools, responsibilities, and relevance mentioned in the text

- Final Score (0–100):
  Weighted combination: (0.40 × Keyword Score) + (0.60 × Semantic Score)

OUTPUT FORMAT (No JSON):
Provide results in the following sections clearly, and DO NOT add extra commentary:

Summary:
(3–5 lines describing how well the resume fits the JD based on explicit content)

Extracted Resume Skills:
(List ONLY skills explicitly mentioned in the resume)

JD Required Skills:
(List ONLY skills explicitly required in the JD)

Matching Skills:
(List ONLY skills that appear in BOTH lists above)

Missing Skills:
(List ONLY skills from JD that are NOT in resume)

Keyword Score: xx/100
Semantic Score: xx/100
Final Score: xx/100

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_crop}

CRITICAL REMINDER: ONLY use skills that are explicitly stated in the provided text. DO NOT infer or assume skills that are not clearly written.
"""

    try:
        llm = get_llm()
        resp = llm.invoke(prompt)
        content = resp.content.strip()
        
        # Parse the structured response
        return parse_llm_response(content)
    except Exception as e:
        print(f"LLM Error: {e}")
        pass

    # fallback
    return {
        "summary": "Unable to generate summary.",
        "matching_skills": [],
        "missing_skills": [],
        "keyword_score": 0,
        "semantic_score": 0,
        "rating": 0,
    }


# ============================================================
# 10. Ranking Pipeline (Hybrid + LLM top K)
# ============================================================

def rank_resumes(job_text: str, resumes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    MAX_LLM_ANALYSIS = getattr(settings, "MAX_LLM_ANALYSIS", 3)

    resume_texts = [r["text"] for r in resumes]
    keyword_scores = compute_scores(job_text, resume_texts)

    ranked = []
    for i, r in enumerate(resumes):
        kw = keyword_scores[i]
        sem = semantic_score_for_resume(job_text, r["id"])
        
        # Ensure we have valid scores
        kw = max(0.0, min(1.0, kw))  # Clamp between 0 and 1
        sem = max(0.0, min(1.0, sem))  # Clamp between 0 and 1

        # Calculate algorithmic score (60% semantic + 40% keyword)
        algo_score = 0.6 * sem * 100 + 0.4 * kw * 100

        ranked.append({
            "resume_id": r["id"],
            "filename": r["filename"],
            "keyword_score": round(kw * 100, 2),
            "semantic_score": round(sem * 100, 2),
            "algorithmic_score": round(algo_score, 2),
            "resume_text": r["text"],
        })

    ranked.sort(key=lambda x: x["algorithmic_score"], reverse=True)

    results = []
    for i, r in enumerate(ranked):
        if i < MAX_LLM_ANALYSIS:
            llm = summarize_with_llm(job_text, r["resume_text"])
            # Always use algorithmic scores as the primary scores
            # LLM scores are for enhancement only
            keyword_score = r["keyword_score"]
            semantic_score = r["semantic_score"]
            # Calculate final score using algorithmic scores
            algo_final_score = r["algorithmic_score"]
            # Use LLM rating only if it's reasonable (not 0) and enhances the analysis
            llm_rating = llm.get("rating")
            final_score = algo_final_score if llm_rating is None or llm_rating <= 0 else llm_rating
            results.append({
                **r,
                "keyword_score": keyword_score,
                "semantic_score": semantic_score,
                "final_score": round(final_score, 2),
                "summary": llm["summary"],
                "matching_skills": llm["matching_skills"],
                "missing_skills": llm["missing_skills"],
                "rating": llm_rating,
                "llm_analyzed": True,
            })
        else:
            results.append({
                **r,
                "final_score": r["algorithmic_score"],
                "summary": "LLM analysis skipped (Top-K optimization)",
                "matching_skills": [],
                "missing_skills": [],
                "rating": None,
                "llm_analyzed": False,
            })

    # Sort by final score for correct ordering in the results table
    results.sort(key=lambda x: x["final_score"], reverse=True)
    
    return results
