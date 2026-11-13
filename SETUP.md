# 🚀 Setup Guide - AI Resume Screening Agent

Complete installation and configuration guide for development and deployment.

---

## 📋 Prerequisites

### Required Software
- **Python**: 3.10 or higher
- **Node.js**: 18+ (LTS recommended)
- **npm**: 9+ (comes with Node.js)
- **Git**: Latest version

### System Requirements
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **RAM**: Minimum 4GB (8GB+ recommended)
- **Disk Space**: 2GB free space

### API Keys
- **Groq API Key**: Get from [https://console.groq.com](https://console.groq.com)
  - Sign up for free account
  - Generate API key from dashboard
  - Free tier includes generous limits

---

## ⚙️ Backend Setup (Django)

### Step 1: Navigate to Backend Directory

```cmd
cd backend
```

### Step 2: Create Virtual Environment

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```cmd
pip install --upgrade pip
pip install -r requirements.txt
```

This will install:
- Django 5.0.4
- Django REST Framework 3.15.2
- ChromaDB 0.5.3
- LangChain 0.3.0 ecosystem
- Groq integration
- ReportLab (PDF generation)
- Document loaders (PyPDF, python-docx)
- scikit-learn for TF-IDF

### Step 4: Create Environment File

Create `backend/.env`:

```env
# Django Configuration
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
 
# ChromaDB Configuration
CHROMA_DB_DIR=chroma_store

# Top-K LLM Analysis (only analyze top K resumes)
MAX_LLM_ANALYSIS=3
```

**Important Notes:**
- **SECRET_KEY**: Generate using `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
- **GROQ_API_KEY**: Required for LLM analysis. Get from [https://console.groq.com](https://console.groq.com)
- **GROQ_MODEL_NAME**: Options:
  - `llama-3.3-70b-versatile` (Recommended - Balanced speed/quality)
  - `mixtral-8x7b-32768` (Fast, good for testing)
  - `llama-3.1-8b-instant` (Fastest, lower quality)
- **MAX_LLM_ANALYSIS**: Number of top candidates to analyze with LLM (default: 3)

### Step 5: Apply Database Migrations

```cmd
python manage.py migrate
```

This creates:
- `db.sqlite3` database
- Tables: JobDescription, Resume, JobHistory, RankedResult
- Admin user table

### Step 6: Create Superuser (Optional but Recommended)

```cmd
python manage.py createsuperuser
```

Follow prompts to create admin account. Access admin panel at `http://127.0.0.1:8000/admin/`

### Step 7: Run Development Server

```cmd
python manage.py runserver 0.0.0.0:8000
```

✅ Backend running at: `http://127.0.0.1:8000`

---

## 🎨 Frontend Setup (React)

### Step 1: Navigate to Frontend Directory

**Open new terminal window:**
```cmd
cd frontend
```

### Step 2: Install Dependencies

```cmd
npm install
```

This installs:
- React 19.2.0
- React Router 7.9.6
- TailwindCSS 3.4.0
- Axios 1.13.2
- Development tools

### Step 3: Create Environment File

Create `frontend/.env.local`:

```env
REACT_APP_API_BASE_URL=http://127.0.0.1:8000/api/screening
```

**Note**: This connects frontend to backend API

### Step 4: Start Development Server

```cmd
npm start
```

✅ Frontend running at: `http://localhost:3000`

Your browser should automatically open. If not, navigate to `http://localhost:3000`

---

## 🧪 Verification Steps

### 1. Check Backend API

Visit: `http://127.0.0.1:8000/api/screening/jobs/`

Expected: API root page or empty JSON array

### 2. Check Frontend

Visit: `http://localhost:3000`

Expected: Beautiful home page with hero section

### 3. Test Complete Flow

1. Click "Create Job Description"
2. Select template or enter custom job description
3. Upload sample resume files
4. Click "Process Resumes"
5. View results with rankings

### 4. Check ChromaDB

After first upload, verify:
```cmd
ls backend/chroma_store
```

Should see ChromaDB files created

---

## 🗂️ Project Structure

```
resume-screening-agent_6/
├── backend/
│   ├── resume_backend/
│   │   ├── settings.py          # Django configuration
│   │   ├── urls.py              # Main URL routing
│   │   └── wsgi.py
│   ├── screening/
│   │   ├── migrations/          # Database migrations
│   │   ├── models.py            # Data models
│   │   ├── views.py             # API endpoints
│   │   ├── serializers.py       # DRF serializers
│   │   ├── urls.py              # App URL routing
│   │   ├── rag_pipeline.py      # ⭐ Core ranking logic
│   │   └── pdf_generator.py     # PDF report generation
│   ├── media/                   # Uploaded files
│   ├── chroma_store/            # Vector database
│   ├── manage.py
│   ├── requirements.txt
│   └── .env                     # Environment variables
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   └── ResumePreviewModal.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx               # Landing page
│   │   │   ├── JobDescriptionPage.jsx     # Create job
│   │   │   ├── ResumeUploadPage.jsx       # Upload resumes
│   │   │   ├── ScreeningResultsPage.jsx   # View rankings
│   │   │   ├── JobHistoryPage.jsx         # History list
│   │   │   └── JobHistoryDetailsPage.jsx  # History details
│   │   ├── api/
│   │   │   └── apiClient.js               # Axios instance
│   │   ├── App.jsx                        # Main app component
│   │   ├── index.css                      # Global styles
│   │   └── index.js                       # Entry point
│   ├── tailwind.config.js       # Tailwind configuration
│   ├── postcss.config.js
│   ├── package.json
│   └── .env.local               # Frontend environment
│
├── ARCHITECTURE.md              # System architecture doc
├── SETUP.md                     # This file
└── README.md                    # Project overview
```

---

## 🐛 Troubleshooting

### Backend Issues

#### 1. **ModuleNotFoundError**
```
Problem: Missing Python packages
Solution: Activate venv and reinstall:
  pip install -r requirements.txt
```

#### 2. **Port 8000 Already in Use**
```
Problem: Another process using port 8000
Solution: 
  Windows: netstat -ano | findstr :8000
          taskkill /PID <process_id> /F
  Mac/Linux: lsof -ti:8000 | xargs kill -9
  
  Or use different port:
  python manage.py runserver 8001
```

#### 3. **ChromaDB Permission Error**
```
Problem: Can't write to chroma_store directory
Solution: Delete and recreate:
  rm -rf chroma_store
  mkdir chroma_store
```

#### 4. **Groq API Errors**
```
Problem: Invalid API key or quota exceeded
Solution:
  - Verify API key in .env
  - Check quota at console.groq.com
  - Try different model (llama-3.1-8b-instant faster)
```

### Frontend Issues

#### 1. **npm install fails**
```
Problem: Node version mismatch
Solution: Update Node.js to 18+ LTS
  https://nodejs.org/
```

#### 2. **CORS Errors**
```
Problem: Backend not allowing frontend requests
Solution: 
  - Verify backend is running
  - Check CORS_ALLOW_ALL_ORIGINS=True in settings.py
  - Verify REACT_APP_API_BASE_URL in .env.local
```

#### 3. **Tailwind Styles Not Applied**
```
Problem: PostCSS/Tailwind not configured
Solution:
  - Verify tailwind.config.js exists
  - Check @tailwind directives in index.css
  - Restart dev server: npm start
```

#### 4. **Blank Page / White Screen**
```
Problem: JavaScript error
Solution:
  - Open browser console (F12)
  - Check for errors
  - Verify all pages imported in App.jsx
```

### Common Errors

#### 1. **SQLite Database Locked**
```
Solution: Close all Django shells/servers
  Delete db.sqlite3 and re-migrate:
  python manage.py migrate
```

#### 2. **File Upload Fails**
```
Problem: File size or type restriction
Solution:
  - Max file size: Check Django settings
  - Supported: PDF, DOCX, TXT only
  - Verify file is not corrupted
```

#### 3. **LLM Returns Empty Summary**
```
Problem: Model timeout or API error
Solution:
  - Check Groq API status
  - Reduce MAX_LLM_ANALYSIS to 1
  - Try faster model (llama-3.1-8b-instant)
```

---

## 🧪 Testing

### Run Backend Tests

```cmd
cd backend
python manage.py test screening
```

### Run Frontend Tests

```cmd
cd frontend
npm test
```

---

## 📦 Production Deployment

### Backend (Django)

1. **Update settings.py:**
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = ['https://yourdomain.com']
```

2. **Use Production Database:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'resume_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Collect Static Files:**
```cmd
python manage.py collectstatic
```

4. **Use Production Server:**
```cmd
pip install gunicorn
gunicorn resume_backend.wsgi:application --bind 0.0.0.0:8000
```

5. **Set Up Nginx Reverse Proxy:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /media/ {
        alias /path/to/backend/media/;
    }
}
```

### Frontend (React)

1. **Update API URL:**
```env
REACT_APP_API_BASE_URL=https://api.yourdomain.com/api/screening
```

2. **Build Production Bundle:**
```cmd
npm run build
```

3. **Deploy Build Folder:**
- Use services like:
  - Vercel (recommended)
  - Netlify
  - AWS S3 + CloudFront
  - GitHub Pages

### Docker Deployment (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - GROQ_API_KEY=${GROQ_API_KEY}
    volumes:
      - ./backend/media:/app/media
      - ./backend/chroma_store:/app/chroma_store
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_BASE_URL=http://localhost:8000/api/screening
```

Run:
```cmd
docker-compose up -d
```

---

## 🔐 Security Checklist

- [ ] Change SECRET_KEY to strong random string
- [ ] Set DEBUG=False in production
- [ ] Use HTTPS (SSL certificate)
- [ ] Add authentication (JWT/OAuth)
- [ ] Implement rate limiting
- [ ] Sanitize file uploads
- [ ] Use environment variables for secrets
- [ ] Enable CSRF protection
- [ ] Set up database backups
- [ ] Monitor API usage and logs

---

## 📚 Additional Resources

- **Django Docs**: https://docs.djangoproject.com/
- **React Docs**: https://react.dev/
- **TailwindCSS**: https://tailwindcss.com/docs
- **ChromaDB**: https://docs.trychroma.com/
- **Groq API**: https://console.groq.com/docs
- **LangChain**: https://python.langchain.com/docs

---

## 💬 Support

If you encounter issues:

1. Check this troubleshooting guide
2. Review console logs (browser & server)
3. Verify all environment variables
4. Ensure all services are running
5. Check GitHub Issues

---

## 🎉 You're All Set!

Access your application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://127.0.0.1:8000/api/screening
- **Admin Panel**: http://127.0.0.1:8000/admin

Start screening resumes with AI! 🚀

---

**Last Updated**: December 2024
