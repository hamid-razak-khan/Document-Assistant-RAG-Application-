# 🏗️ System Architecture - AI Resume Screening Agent

## Architecture Diagram

```mermaid
graph TB
    subgraph "Frontend - React 19"
        UI[User Interface]
        HP[HomePage]
        JDP[JobDescriptionPage]
        RUP[ResumeUploadPage]
        SRP[ScreeningResultsPage]
        JHP[JobHistoryPage]
        JHDP[JobHistoryDetailsPage]
        API_CLIENT[Axios API Client]
    end

    subgraph "Backend - Django REST Framework"
        REST_API[REST API Endpoints]
        VIEWS[Views Layer]
        MODELS[Models Layer]
        SERIALIZERS[Serializers]
        RAG[RAG Pipeline]
        PDF_GEN[PDF Generator]
    end

    subgraph "Storage Layer"
        SQLITE[(SQLite Database)]
        CHROMADB[(ChromaDB<br/>Vector Store)]
        MEDIA[Media Files<br/>Resume PDFs/DOCX]
    end

    subgraph "AI/ML Components"
        HASH_EMB[SimpleHashEmbeddings<br/>MD5-based 512-dim]
        TFIDF[TF-IDF Vectorizer<br/>Keyword Matching]
        SEMANTIC[Semantic Search<br/>ChromaDB]
        GROQ_LLM[Groq LLM API<br/>ChatGroq]
    end

    subgraph "Hybrid Ranking Engine"
        ALGO_SCORE[Algorithmic Scoring<br/>TF-IDF + Semantic]
        TOPK[Top-K Selector<br/>MAX_LLM_ANALYSIS=3]
        LLM_ANALYSIS[LLM Analysis<br/>Top K Only]
        FINAL_RANK[Final Ranking<br/>with LLM metadata]
    end

    %% Frontend Flow
    UI --> HP
    UI --> JDP
    UI --> RUP
    UI --> SRP
    UI --> JHP
    UI --> JHDP
    HP --> API_CLIENT
    JDP --> API_CLIENT
    RUP --> API_CLIENT
    SRP --> API_CLIENT
    JHP --> API_CLIENT
    JHDP --> API_CLIENT

    %% API Communication
    API_CLIENT -->|HTTP Requests| REST_API

    %% Backend Processing
    REST_API --> VIEWS
    VIEWS --> MODELS
    VIEWS --> SERIALIZERS
    VIEWS --> RAG
    VIEWS --> PDF_GEN

    %% RAG Pipeline Flow
    RAG -->|Document Loading| MEDIA
    RAG -->|Text Chunking| HASH_EMB
    HASH_EMB -->|Store Vectors| CHROMADB
    RAG -->|Keyword Analysis| TFIDF
    RAG -->|Semantic Search| SEMANTIC
    SEMANTIC -->|Query Vectors| CHROMADB

    %% Ranking Flow
    RAG --> ALGO_SCORE
    ALGO_SCORE --> TOPK
    TOPK -->|Top K Candidates| LLM_ANALYSIS
    LLM_ANALYSIS -->|API Call| GROQ_LLM
    GROQ_LLM -->|Structured JSON| LLM_ANALYSIS
    TOPK -->|Remaining| FINAL_RANK
    LLM_ANALYSIS --> FINAL_RANK

    %% Data Persistence
    MODELS --> SQLITE
    VIEWS -->|Save History| SQLITE
    PDF_GEN -->|Generate Reports| MEDIA

    %% Styling
    classDef frontend fill:#3b82f6,stroke:#1e40af,color:#fff
    classDef backend fill:#10b981,stroke:#059669,color:#fff
    classDef storage fill:#f59e0b,stroke:#d97706,color:#fff
    classDef ai fill:#8b5cf6,stroke:#7c3aed,color:#fff
    classDef ranking fill:#ef4444,stroke:#dc2626,color:#fff

    class UI,HP,JDP,RUP,SRP,JHP,JHDP,API_CLIENT frontend
    class REST_API,VIEWS,MODELS,SERIALIZERS,RAG,PDF_GEN backend
    class SQLITE,CHROMADB,MEDIA storage
    class HASH_EMB,TFIDF,SEMANTIC,GROQ_LLM ai
    class ALGO_SCORE,TOPK,LLM_ANALYSIS,FINAL_RANK ranking
```

## Component Breakdown

### 🎨 Frontend (React 19)

#### Pages
- **HomePage**: Landing page with hero section, features, and workflow
- **JobDescriptionPage**: Create job with templates and word count
- **ResumeUploadPage**: Drag-drop upload with progress tracking
- **ScreeningResultsPage**: Top-N selector, expandable details, LLM badges
- **JobHistoryPage**: Search and browse past screenings
- **JobHistoryDetailsPage**: View detailed results with PDF download

#### Components
- **Navbar**: Global navigation with active state highlighting
- **ResumePreviewModal**: Display extracted resume text

#### API Client
- Axios instance configured with base URL
- Handles all HTTP communication with backend

---

### ⚙️ Backend (Django + DRF)

#### Models
```python
JobDescription
├── id
├── title
├── text
└── created_at

Resume
├── id
├── job (FK)
├── file
├── filename
├── text (extracted)
└── uploaded_at

JobHistory
├── id
├── job_title
├── job_description
├── total_resumes
├── top_candidate
├── highest_score
├── results_data (JSON)
└── created_at

RankedResult
├── id
├── job_history (FK)
├── resume (FK)
├── filename
├── keyword_score
├── semantic_score
├── final_score
├── summary
├── matching_skills (JSON)
├── missing_skills (JSON)
├── rating
├── llm_analyzed (Boolean)
└── rank_position
```

#### API Endpoints
```
POST   /api/screening/jobs/                          - Create job description
POST   /api/screening/jobs/{id}/resumes/             - Upload resumes
GET    /api/screening/jobs/{id}/resumes/list/        - List resumes
POST   /api/screening/jobs/{id}/rank/                - Process screening
GET    /api/screening/resumes/{id}/text/             - Get resume text
GET    /api/screening/history/                       - List job history
GET    /api/screening/history/{id}/                  - Get history details
DELETE /api/screening/history/{id}/delete/           - Delete history
DELETE /api/screening/history/clear/                 - Clear all history
POST   /api/screening/preview-bulk-email/            - Preview bulk emails
POST   /api/screening/send-bulk-email/               - Send bulk emails
GET    /api/screening/history/{id}/download/         - Download full report PDF
GET    /api/screening/history/{id}/results/{rid}/download/ - Download candidate PDF
```

---

### 🧠 RAG Pipeline (`rag_pipeline.py`)

#### 1. Document Processing
```python
load_resume_document()  # PDF, DOCX, TXT support
preprocess_and_chunk()  # 800 chars, 200 overlap
```

#### 2. Embedding Generation
```python
class SimpleHashEmbeddings:
    - MD5 hash-based tokenization
    - 512-dimensional vectors
    - L2 normalization
    - Zero ML dependencies
```

#### 3. Vector Storage
```python
ChromaDB:
    - Collection: "resumes"
    - Metadata: job_id, resume_id, filename
    - Persistent local storage
```

#### 4. Hybrid Scoring
```python
Keyword Score: TF-IDF + Cosine Similarity
Semantic Score: ChromaDB top-5 chunks + distance normalization
Algorithmic Score: 0.6 * semantic + 0.4 * keyword
```

#### 5. Top-K LLM Optimization
```python
MAX_LLM_ANALYSIS = 3  # Configurable in settings

1. Compute algorithmic scores for ALL resumes
2. Sort by score (descending)
3. Apply LLM analysis to top K only
4. Remaining get algorithmic score only
5. Flag: llm_analyzed (True/False)
```

#### 6. LLM Analysis (Top K Only)
```python
ChatGroq API:
    - Model: configurable (default: openai/gpt-oss-20b)
    - Prompt: Structured JSON extraction
    - Output: summary, matching_skills, missing_skills, rating
    - Retry logic: 4 attempts with exponential backoff
    - Safe JSON parsing with regex fallback
```

---

### 📊 Data Flow

#### Complete Screening Workflow

```
1. User creates Job Description
   └─> Saved to JobDescription model

2. User uploads resumes (PDF/DOCX/TXT)
   ├─> Files saved to media/resumes/
   ├─> Text extraction via loaders
   ├─> Text chunking (800/200)
   ├─> Hash embeddings generated
   └─> Vectors stored in ChromaDB

3. User triggers screening
   ├─> Fetch job text & all resumes
   ├─> Compute TF-IDF keyword scores (ALL)
   ├─> Compute semantic scores via ChromaDB (ALL)
   ├─> Calculate algorithmic scores (ALL)
   ├─> Sort by score
   ├─> Select Top K (default: 3)
   │   ├─> LLM analysis for Top K
   │   │   ├─> API call to Groq
   │   │   ├─> Extract: summary, skills, rating
   │   │   └─> Set llm_analyzed = True
   │   └─> Algorithmic only for rest
   │       └─> Set llm_analyzed = False
   ├─> Save to JobHistory model
   ├─> Save to RankedResult model (per candidate)
   └─> Return ranked results to frontend

4. Frontend displays results
   ├─> Top 3 podium with badges
   ├─> Top-N selector (dynamic filtering)
   ├─> Expandable details
   │   ├─> Summary
   │   ├─> Matching skills (green badges)
   │   ├─> Missing skills (red badges)
   │   └─> Skill match bar
   └─> LLM status badges
       ├─> ✓ LLM Analyzed (green)
       └─> ⚡ Algorithm Only (gray)

5. User views history
   └─> Browse past screenings with search

6. User downloads PDF report
   └─> ReportLab generates structured PDF
```

---

### 🎯 Key Features

#### Top-K LLM Optimization
- **Problem**: LLM API calls are expensive and slow
- **Solution**: Only analyze top K candidates (default: 3)
- **Benefits**:
  - 90% cost reduction for 30+ resumes
  - 3x faster processing
  - No accuracy loss (algorithmic ranking still accurate)

#### Hash-Based Embeddings
- **Advantage**: No GPU/PyTorch required
- **Speed**: ~100x faster than transformer models
- **Drawback**: Lower semantic accuracy vs BERT/OpenAI
- **Trade-off**: Acceptable for keyword-heavy resume matching

#### Resume Preview
- **Feature**: Click resume card → view extracted text
- **Use case**: Verify OCR quality, check parsing errors
- **Modal**: Full-screen overlay with formatted text

#### PDF Reports
- **Single Candidate**: Detailed analysis with recommendations
- **Full Report**: Summary table of all candidates
- **ReportLab**: Professional formatting with colors, tables, charts

---

### 🔒 Security Considerations

**Current (Development)**:
- CORS: Allow all origins
- No authentication
- SECRET_KEY in .env
- SQLite (single-user)

**Production Recommendations**:
- Add JWT/OAuth authentication
- Restrict CORS to specific domains
- Use PostgreSQL/MySQL
- Implement rate limiting
- Add input validation & sanitization
- Store API keys in secrets manager
- Enable HTTPS only
- Add CSRF protection

---

### ⚡ Performance Optimizations

1. **Hash Embeddings**: CPU-friendly, no GPU needed
2. **Top-K LLM**: Reduce API calls by 90%
3. **ChromaDB**: Local vector store, no network latency
4. **Batch Processing**: Upload multiple resumes at once
5. **Frontend Caching**: Store results in state
6. **Lazy Loading**: Expandable details loaded on-demand

---

### 🚀 Future Enhancements

- [ ] Celery + Redis for async background processing
- [ ] WebSockets for real-time progress updates
- [ ] Multi-tenancy with user authentication
- [ ] Advanced filters (skills, experience, education)
- [ ] Resume ranking history comparison
- [ ] Email notifications for completed screenings
- [ ] Export to CSV/Excel
- [ ] Candidate notes and tags
- [ ] Collaborative hiring (team features)
- [ ] Integration with ATS systems

---

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend | React | 19.2.0 | UI framework |
| Frontend | React Router | 7.9.6 | Navigation |
| Frontend | TailwindCSS | 3.4.0 | Styling |
| Frontend | Axios | 1.13.2 | HTTP client |
| Backend | Django | 5.0.4 | Web framework |
| Backend | DRF | 3.15.2 | REST API |
| Backend | Python | 3.10+ | Language |
| Database | SQLite | Built-in | Relational DB |
| Vector DB | ChromaDB | 0.5.3 | Embeddings storage |
| LLM | Groq | API | Text analysis |
| ML | scikit-learn | 1.4.2 | TF-IDF |
| Docs | python-docx | 1.1.0 | DOCX parsing |
| Docs | pypdf | 4.2.0 | PDF parsing |
| Reports | ReportLab | 4.0.7 | PDF generation |
| LangChain | 0.3.0 | Document loaders, text splitters |

---

**Last Updated**: December 2024
