# Backend Documentation - Resume ATS Analysis Platform

## Table of Contents
1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Technology Stack & Dependencies](#technology-stack--dependencies)
4. [Database Models](#database-models)
5. [API Endpoints](#api-endpoints)
6. [Core Services](#core-services)
7. [PDF Parsing & Text Extraction](#pdf-parsing--text-extraction)
8. [Groq AI Integration](#groq-ai-integration)
9. [Skills Extraction Engine](#skills-extraction-engine)
10. [ATS Score Calculation](#ats-score-calculation)
11. [Skills & ATS Distribution](#skills--ats-distribution)
12. [Configuration](#configuration)

---

## System Overview

**Resume ATS Analysis Platform** is a Flask-based backend system that provides:
- User authentication & profile management
- Resume upload & PDF parsing
- ATS (Applicant Tracking System) scoring
- AI-powered resume analysis using Groq LLM
- Skills extraction & categorization
- Job description matching
- Dashboard with aggregated statistics
- Interview session tracking
- Coding challenge execution

The system is designed to help candidates optimize their resumes for ATS systems and improve their job application success rate.

---

## Architecture

### High-Level Flow

```
User Upload Resume (PDF)
    ↓
[Flask API] - /api/resume/upload (POST)
    ↓
Parse PDF → Extract Text (pdfplumber)
    ↓
Parallel Processing:
├─ Extract Sections (Header, Experience, Education, Skills, etc.)
├─ Extract Skills (NLP + Keyword Matching)
├─ Extract Entities (Email, Phone, LinkedIn, etc.)
├─ Extract Experience Years
├─ Calculate ATS Score (Weighted Multi-Category Scoring)
└─ Run AI Analysis (Groq LLM)
    ↓
Store in Database (PostgreSQL/SQLite)
    ↓
Return Analysis to Frontend
```

### Component Breakdown

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Web Framework** | Flask 3.1+ | HTTP REST API |
| **Database** | PostgreSQL/SQLite | Data Persistence |
| **Authentication** | JWT (Flask-JWT-Extended) | Secure Token-Based Auth |
| **PDF Parsing** | pdfplumber 0.11+ | Text Extraction from PDFs |
| **NLP** | spaCy, NLTK | Named Entity Recognition, Text Processing |
| **LLM** | Groq API (llama-3.3-70b) | AI Analysis & Recommendations |
| **CORS** | Flask-CORS | Cross-Origin Request Handling |
| **Deployment** | Gunicorn, Docker | Production Hosting |

---

## Technology Stack & Dependencies

### Python Dependencies

```
Flask>=3.1.1                          # Web framework
Flask-CORS>=5.0.1                     # CORS support
Flask-SQLAlchemy>=3.1.1               # ORM
Flask-JWT-Extended>=4.7.1             # JWT authentication
pdfplumber>=0.11.4                    # PDF parsing
spacy                                 # NLP - Named Entity Recognition
nltk                                  # NLP - Text processing
python-dotenv>=1.0.1                  # Environment variable management
Werkzeug>=3.1.3                       # Security utilities
gunicorn>=22.0.0                      # WSGI HTTP Server
groq>=0.9.0                           # Groq AI API client
psycopg2-binary>=2.9.9                # PostgreSQL adapter
```

### Key Libraries Overview

- **pdfplumber**: Advanced PDF text extraction with page-by-page processing
- **spacy**: Pre-trained English model (`en_core_web_sm`) for entity recognition
- **nltk**: Natural language processing toolkit
- **Groq**: Async API client for LLaMA 3.3 70B model
- **SQLAlchemy**: ORM for database operations

---

## Database Models

### User Model
```python
class User:
  - id (Primary Key)
  - username (Unique, String)
  - email (Unique, String)
  - password_hash (String, Bcrypt + Salt)
  - created_at (DateTime)
  - Relationships: resumes, interview_sessions, coding_tests
```

### Resume Model
```python
class Resume:
  - id (Primary Key)
  - user_id (Foreign Key → User)
  - filename (String, Unique Hash)
  - original_filename (String)
  - raw_text (Text, Full PDF content)
  - skills_json (Text, JSON list of extracted skills)
  - ats_score (Float, 0-100)
  - analysis_json (Text, JSON analysis result)
  - uploaded_at (DateTime)
  - Relationships: interview_sessions
```

### Interview Session Model
```python
class InterviewSession:
  - id (Primary Key)
  - user_id (Foreign Key)
  - resume_id (Foreign Key)
  - topic (String)
  - score (Float)
  - created_at (DateTime)
```

### Coding Test Model
```python
class CodingTest:
  - id (Primary Key)
  - user_id (Foreign Key)
  - problem_id (String)
  - language (String, python/javascript)
  - code_submitted (Text)
  - passed (Boolean)
  - score (Float)
  - created_at (DateTime)
```

---

## API Endpoints

### Authentication Routes (`/api/auth`)

#### 1. Register User
- **Endpoint**: `POST /api/auth/register`
- **Request Body**:
  ```json
  {
    "username": "john_doe",
    "email": "john@example.com",
    "password": "securePass123"
  }
  ```
- **Validation**:
  - Username: 3-80 chars, alphanumeric + dots/hyphens/underscores
  - Email: Valid email format
  - Password: Minimum 6 characters
  - Username & Email uniqueness check
- **Response** (201 Created):
  ```json
  {
    "message": "Registration successful",
    "access_token": "eyJhbGc...",
    "user": { "id": 1, "username": "john_doe", "email": "john@example.com", "created_at": "2024-..." }
  }
  ```

#### 2. Login User
- **Endpoint**: `POST /api/auth/login`
- **Request Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securePass123"
  }
  ```
- **Response** (200 OK):
  ```json
  {
    "message": "Login successful",
    "access_token": "eyJhbGc...",
    "user": { "id": 1, "username": "john_doe", ... }
  }
  ```

#### 3. Get User Profile
- **Endpoint**: `GET /api/auth/profile`
- **Auth**: Required (Bearer Token)
- **Response** (200 OK):
  ```json
  {
    "user": { "id": 1, "username": "john_doe", "email": "john@example.com", "created_at": "2024-..." }
  }
  ```

---

### Resume Routes (`/api/resume`)

#### 1. Upload & Analyze Resume
- **Endpoint**: `POST /api/resume/upload`
- **Auth**: Required (Bearer Token)
- **Content-Type**: `multipart/form-data`
- **Request**: File upload with key `file` (PDF only, max 16 MB)
- **Processing Steps**:
  1. Validate file (PDF format)
  2. Save file with unique hash filename
  3. Parse PDF text using pdfplumber
  4. Extract sections (Contact, Experience, Education, Skills, etc.)
  5. Extract skills using NLP engine
  6. Calculate ATS score
  7. Generate AI insights using Groq
  8. Store all data in database
- **Response** (201 Created):
  ```json
  {
    "message": "Resume uploaded and analyzed successfully",
    "resume": {
      "id": 1,
      "user_id": 1,
      "filename": "abc123_john_resume.pdf",
      "original_filename": "john_resume.pdf",
      "skills": [
        { "skill": "Python", "category": "Programming Languages", "confidence": 0.95 },
        { "skill": "React", "category": "Web Frameworks", "confidence": 0.90 }
      ],
      "ats_score": 78.5,
      "analysis": {
        "sections": { "contact": "...", "experience": "...", ... },
        "entities": { "emails": [...], "phones": [...], ... },
        "experience_years": 5,
        "ats_breakdown": { ... },
        "suggestions": [ ... ],
        "word_count": 450,
        "skill_count": 18,
        "ai_insights": { "candidate_summary": "...", "key_strengths": [...], ... }
      },
      "uploaded_at": "2024-..."
    }
  }
  ```

#### 2. List User's Resumes
- **Endpoint**: `GET /api/resume/list`
- **Auth**: Required
- **Response** (200 OK):
  ```json
  {
    "resumes": [
      { "id": 1, "filename": "...", "ats_score": 78.5, ... },
      { "id": 2, "filename": "...", "ats_score": 82.0, ... }
    ],
    "count": 2
  }
  ```

#### 3. Get Single Resume
- **Endpoint**: `GET /api/resume/<resume_id>`
- **Auth**: Required
- **Response** (200 OK): Full resume object (same structure as upload)

#### 4. Delete Resume
- **Endpoint**: `DELETE /api/resume/<resume_id>`
- **Auth**: Required
- **Processing**: 
  - Delete physical PDF file from uploads folder
  - Delete database record
- **Response** (200 OK):
  ```json
  {
    "message": "Resume deleted successfully"
  }
  ```

#### 5. Match Resume to Job Description
- **Endpoint**: `POST /api/resume/match-job`
- **Auth**: Required
- **Request Body**:
  ```json
  {
    "resume_id": 1,
    "job_description": "We are looking for a Python developer with 5+ years experience..."
  }
  ```
- **Processing**:
  - Fetch resume by ID
  - Send both resume text and job description to Groq AI
  - Get match percentage, matching/missing skills, improvement suggestions
  - Provide alternative job recommendations if match < 40%
- **Response** (200 OK):
  ```json
  {
    "match_result": {
      "match_percentage": 75,
      "matching_skills": ["Python", "Flask", "PostgreSQL", "Docker"],
      "missing_skills": ["Kubernetes", "Apache Spark", "AWS"],
      "improvement_suggestions": [
        "Add Kubernetes experience to your experience section",
        "Mention specific AWS services you've used",
        "Highlight big data projects"
      ],
      "alternative_jobs": []
    }
  }
  ```

---

### Dashboard Routes (`/api/dashboard`)

#### 1. Get User Statistics
- **Endpoint**: `GET /api/dashboard/stats`
- **Auth**: Required
- **Response** (200 OK):
  ```json
  {
    "stats": {
      "total_resumes": 2,
      "avg_ats_score": 80.25,
      "total_interviews": 5,
      "avg_interview_score": 75.0,
      "total_coding_tests": 3,
      "coding_pass_rate": 66.7
    }
  }
  ```

#### 2. Get Skills Data
- **Endpoint**: `GET /api/dashboard/skills`
- **Auth**: Required
- **Processing**: 
  - Aggregate skills from all user's resumes
  - Count frequency of each skill
  - Group skills by category
- **Response** (200 OK):
  ```json
  {
    "skills": [
      { "skill": "Python", "count": 3 },
      { "skill": "JavaScript", "count": 2 },
      { "skill": "React", "count": 2 }
    ],
    "categories": [
      { "category": "Programming Languages", "count": 5 },
      { "category": "Web Frameworks", "count": 4 },
      { "category": "Cloud & DevOps", "count": 2 }
    ],
    "total_unique_skills": 15,
    "total_categories": 8
  }
  ```

---

## Core Services

### 1. PDF Parser Service (`services/pdf_parser.py`)

#### Functions:

**`parse_pdf(file_path: str) → str`**
- Reads PDF file page-by-page using pdfplumber
- Extracts text from each page
- Cleans and normalizes text:
  - Removes non-printable characters
  - Normalizes whitespace (multiple spaces → single space)
  - Normalizes newlines (3+ → 2 newlines)
  - Strips line-level whitespace
- Returns cleaned text string
- Raises `ValueError` if PDF is invalid or empty

**`extract_sections(text: str) → dict`**
- Uses regex patterns to identify resume sections
- Recognizes: Contact, Summary, Experience, Education, Skills, Projects, Certifications
- Maps each line to the most appropriate section header
- Returns dictionary with section content

**Section Detection Patterns**:
```
Contact: "Contact Info", "Contact Information", "Personal Details"
Summary: "Summary", "Objective", "Profile", "About Me"
Experience: "Work Experience", "Employment History", "Experience"
Education: "Education", "Academic Background", "Qualifications"
Skills: "Technical Skills", "Key Skills", "Expertise", "Technologies"
Projects: "Projects", "Portfolio", "Notable Projects"
Certifications: "Certifications", "Licenses", "Awards", "Achievements"
```

---

### 2. NLP Engine Service (`services/nlp_engine.py`)

#### Key Features:

**Comprehensive Skills Database (300+ skills)**
- Programming Languages (35+): Python, Java, JavaScript, C++, Go, Rust, etc.
- Web Frameworks (40+): React, Angular, Vue, Django, Flask, Spring Boot, etc.
- Databases (25+): PostgreSQL, MongoDB, MySQL, Redis, Cassandra, etc.
- Cloud & DevOps (50+): AWS, Azure, GCP, Docker, Kubernetes, Jenkins, etc.
- Data Science & ML (50+): TensorFlow, PyTorch, scikit-learn, Pandas, etc.
- Mobile Development (15+): React Native, Flutter, Swift, Kotlin, etc.
- Testing (20+): Jest, Selenium, Cypress, pytest, etc.
- Tools & Platforms (60+): Git, Jira, Docker, VS Code, etc.
- Architecture & Patterns: Microservices, REST, GraphQL, CQRS, etc.
- Security: OAuth, SAML, Encryption, GDPR, etc.
- Soft Skills (30+): Leadership, Communication, Project Management, etc.

#### Functions:

**`extract_skills(text: str) → List[Dict]`**
- **Pass 1**: Multi-word/special-character skills (exact substring matching)
- **Pass 2**: Single-word skills (word-boundary regex matching)
- **Pass 3**: spaCy NER enhancement (if available)
- Returns sorted list of skills with confidence scores (0.0-1.0)

**Confidence Scoring**:
```
≥ 5 occurrences   → confidence = 0.95
≥ 3 occurrences   → confidence = 0.90
≥ 2 occurrences   → confidence = 0.80
1 occurrence      → confidence = 0.70
```

**`extract_entities(text: str) → dict`**
- Extracts:
  - Emails: Regex pattern matching
  - Phone numbers: Multiple format support (with country codes, extensions)
  - URLs: HTTP/HTTPS URLs
  - LinkedIn profiles: Special pattern extraction
  - Names & Organizations: Using spaCy NER (if available)
- Returns deduplicated lists

**`extract_experience_years(text: str) → int`**
- Detects date patterns in text
- Calculates years of experience from employment dates
- Returns estimated total experience

---

### 3. ATS Scorer Service (`services/ats_scorer.py`)

#### Overall Score Calculation

**Weighted Multi-Category Scoring** (0-100 scale):

```
Overall Score = 
  (Contact Info Score × 0.10) +
  (Formatting Score × 0.20) +
  (Skills Keywords Score × 0.30) +
  (Experience Score × 0.25) +
  (Education Score × 0.15)
```

#### Category Breakdown:

##### 1. Contact Info Score (10% Weight, 100 pts max)
- **Email**: +35 pts (Regex: `[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}`)
- **Phone**: +30 pts (Regex: `(\d{3})-(\d{3})-(\d{4})` variants)
- **LinkedIn**: +20 pts (Keyword match: "linkedin")
- **Name Detection**: +15 pts (First line non-digit content)

##### 2. Formatting Score (20% Weight, 100 pts max)
- **Section Headers** (0-30 pts):
  - All 3 key sections (Experience, Education, Skills) present: +30 pts
  - 2 sections: +20 pts
  - 1 section: +10 pts
  
- **Bullet Points** (0-20 pts):
  - ≥10 bullet points: +20 pts
  - 5-9 bullet points: +12 pts
  - 1-4 bullet points: +6 pts
  - 0 bullet points: 0 pts
  - Patterns detected: `[•●○◦▪▸►\-\*]` or `^\d+[.)]`
  
- **Resume Length** (0-25 pts):
  - 300-1200 words: +25 pts (Optimal)
  - 200-299 words: +15 pts (Too short)
  - 1200-1800 words: +18 pts (Slightly long)
  - >1800 words: +10 pts (Too long)
  
- **Date Formatting** (0-15 pts):
  - ≥2 dates found: +15 pts
  - 1 date: +8 pts
  - 0 dates: 0 pts
  
- **Special Characters** (0-10 pts):
  - <2% special chars: +10 pts
  - 2-5% special chars: +5 pts
  - >5% special chars: 0 pts

##### 3. Skills Keywords Score (30% Weight, 100 pts max)
- **Number of Skills** (0-50 pts):
  - ≥15 skills: +50 pts
  - 10-14 skills: +40 pts
  - 6-9 skills: +28 pts
  - 3-5 skills: +15 pts
  - 1-2 skills: +8 pts
  - 0 skills: 0 pts
  
- **Category Diversity** (0-30 pts):
  - ≥5 categories: +30 pts
  - 3-4 categories: +20 pts
  - 2 categories: +12 pts
  - 1 category: +5 pts
  
- **Technical vs Soft Skills Balance** (0-20 pts):
  - Both present: +20 pts
  - Only technical: +12 pts
  - Only soft skills: +8 pts
  - None: 0 pts

##### 4. Experience Score (25% Weight, 100 pts max)
- **Experience Section Presence** (0-20 pts):
  - Present & detailed (>50 chars): +20 pts
  - Present but thin: +10 pts
  - Missing: 0 pts
  
- **Quantifiable Achievements** (0-30 pts):
  - ≥8 metrics (%, $, numbers): +30 pts
  - 4-7 metrics: +20 pts
  - 1-3 metrics: +10 pts
  - 0 metrics: 0 pts
  - Patterns: `\d+\s*%`, `\$[\d,.]+`, `\b\d{2,}\b`
  
- **Action Verbs** (0-25 pts):
  - ≥8 verbs: +25 pts (led, managed, developed, designed, implemented, etc.)
  - 4-7 verbs: +18 pts
  - 2-3 verbs: +10 pts
  - 0-1 verbs: 0 pts
  
- **Keyword Presence** (0-25 pts):
  - Industry-relevant keywords detected

##### 5. Education Score (15% Weight, 100 pts max)
- **Education Section Presence** (0-30 pts): Full/Partial education info
- **Degree Information** (0-30 pts): Bachelor, Master, PhD detected
- **Institution Names** (0-20 pts): Recognized institutions
- **Certifications** (0-20 pts): Relevant certifications

#### Suggestions Generation

Based on category scores, the system generates targeted suggestions:
- If Contact Info < 80: "Add missing contact information"
- If Formatting < 70: "Use more bullet points" or "Reduce resume length"
- If Skills < 60: "Add more technical keywords"
- If Experience < 70: "Include quantifiable metrics" or "Use stronger action verbs"
- If Education < 60: "Add relevant certifications"

---

### 4. AI Analyzer Service (`services/ai_analyzer.py`)

#### Function: `analyze_resume_with_ai(resume_text: str) → dict`

**Groq API Configuration**:
- Model: `llama-3.3-70b-versatile`
- Temperature: 0.3 (Lower = more focused/deterministic)
- Max Tokens: 1024
- Response Format: JSON

**Prompt Engineering**:
```
System Role: "You are an expert ATS. You must ONLY output a valid JSON object. No explanation, no markdown tags."

User Prompt: [Resume analysis request with truncated resume text (first 6000 chars)]

Requested JSON Format:
{
  "candidate_summary": "2-sentence summary of candidate profile",
  "key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
  "areas_for_improvement": ["Improvement 1", "Improvement 2"],
  "ai_recommendation": "Actionable paragraph for resume improvement"
}
```

**Processing Steps**:
1. Check for GROQ_API_KEY environment variable
2. Initialize Groq client
3. Truncate resume to first 6000 characters (token budget)
4. Send to Groq API with JSON response format
5. Parse JSON response (strip markdown fencing if present)
6. Return structured analysis

**Error Handling**:
- Returns error dict if API key not configured
- Returns error dict if API call fails
- Includes exception details for debugging

---

### 5. Job Matcher Service (`services/job_matcher.py`)

#### Function: `match_resume_to_job(resume_text: str, job_description: str) → dict`

**Comparison Process** using Groq AI:

**Request Format**:
```json
{
  "match_percentage": 0-100,
  "matching_skills": ["skill1", "skill2", ...],
  "missing_skills": ["skill1", "skill2", ...],
  "improvement_suggestions": [
    "Specific actionable suggestion 1",
    "Specific actionable suggestion 2",
    "Specific actionable suggestion 3"
  ],
  "alternative_jobs": ["Job Title 1", "Job Title 2"]  // Only if match < 40%
}
```

**Groq Prompt**:
- Truncates resume to first 5000 chars
- Truncates job description to first 3000 chars
- Instructs model to identify:
  - How well resume matches job (0-100%)
  - Matching skills from job description found in resume
  - Missing skills needed for the role
  - 3-5 specific improvements to make resume more suitable
  - 3-5 alternative jobs better suited for candidate (if match < 40%)

**Response Validation**:
- Ensures all expected keys exist
- Defaults to empty arrays if keys missing
- Sets alternative_jobs to empty array if match ≥ 40%

---

## PDF Parsing & Text Extraction

### Detailed PDF Processing Flow

```
PDF File Upload (max 16 MB)
    ↓
File Type Validation (extension: .pdf)
    ↓
Save to Disk: backend/uploads/{hash_timestamp}_{original_name}.pdf
    ↓
pdfplumber.open(file_path)
    ├─ Iterate each page
    ├─ Extract text using OCR-aware extraction
    └─ Concatenate with newline separator
    ↓
Text Cleaning Pipeline:
├─ Remove non-printable chars: [^\x20-\x7E\n\t]
├─ Normalize spaces: [ \t]+ → single space
├─ Normalize newlines: \n{3,} → \n\n
├─ Strip per-line whitespace
└─ Remove leading/trailing whitespace
    ↓
Store cleaned text in Resume.raw_text column
    ↓
Extract sections using regex patterns
    ↓
Return to caller
```

### Error Handling

| Error | Cause | Response |
|-------|-------|----------|
| No file provided | Missing 'file' key in form data | 400 Bad Request |
| No file selected | Empty filename | 400 Bad Request |
| File type invalid | Not .pdf extension | 400 Bad Request |
| PDF Syntax Error | Corrupted PDF file | 422 Unprocessable Entity |
| No readable text | Image-based PDF or empty | 422 Unprocessable Entity |
| Parse failure | Unexpected exception | 500 Internal Server Error |

### Text Extraction Example

**Original PDF Text**:
```
John Doe
john@example.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years...
```

**After Cleaning**:
```
John Doe
john@example.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Experienced software engineer with 5+ years...
```

---

## Groq AI Integration

### API Setup & Configuration

**Environment Variable**:
```bash
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxx
```

**Groq Models Available** (as of 2024):
- `llama-3.3-70b-versatile` (Primary model used)
- `llama-3.1-70b-versatile`
- `mixtral-8x7b-32768`
- `gemma-7b-it`

### Two Main Use Cases

#### 1. Resume Analysis (AI Insights)

**Service**: `ai_analyzer.py::analyze_resume_with_ai()`

**Use Case**: Generate insights about candidate's resume

**Request**:
```
POST https://api.groq.com/openai/v1/chat/completions
Authorization: Bearer {GROQ_API_KEY}

{
  "model": "llama-3.3-70b-versatile",
  "messages": [
    {
      "role": "system",
      "content": "You are an expert ATS. Output ONLY valid JSON."
    },
    {
      "role": "user",
      "content": "[Resume text + analysis request]"
    }
  ],
  "temperature": 0.3,
  "max_tokens": 1024,
  "response_format": {"type": "json_object"}
}
```

**Response Parse**:
```python
response_text = completion.choices[0].message.content.strip()

# Strip markdown if present
if response_text.startswith("```"):
    response_text = response_text.split("\n", 1)[1]
if response_text.endswith("```"):
    response_text = response_text[:-3]

# Parse JSON
result = json.loads(response_text.strip())
```

**Output**:
```json
{
  "candidate_summary": "Senior Full Stack Developer with 8+ years experience...",
  "key_strengths": [
    "Strong backend architecture skills",
    "Proven leadership in team environments",
    "Extensive cloud platform experience"
  ],
  "areas_for_improvement": [
    "Limited AI/ML exposure",
    "Few published technical articles"
  ],
  "ai_recommendation": "To strengthen your resume, consider taking an AI/ML course..."
}
```

#### 2. Job Matching (Resume vs Job Description)

**Service**: `job_matcher.py::match_resume_to_job()`

**Use Case**: Compare resume against specific job posting

**Request**:
```
Same API endpoint, but with comparative prompt including both resume and JD
```

**Output**:
```json
{
  "match_percentage": 78,
  "matching_skills": ["Python", "Django", "PostgreSQL", "Docker", "AWS"],
  "missing_skills": ["Kubernetes", "GraphQL", "Machine Learning"],
  "improvement_suggestions": [
    "Add Kubernetes experience to your project portfolio",
    "Include GraphQL projects in your experience",
    "Consider taking an ML certification course"
  ],
  "alternative_jobs": []
}
```

### Temperature & Sampling

- **Temperature = 0.3**: Low temperature for consistent, predictable outputs
  - Better for structured extraction
  - Less creative variation
  - More suitable for ATS analysis

### Token Limits & Budget

- **Resume Truncation**: 6000 characters (≈1500 tokens)
- **Job Description Truncation**: 3000 characters (≈750 tokens)
- **Max Response Tokens**: 1024-1500
- **Typical Request**: 3000-4000 tokens total
- **Groq Rate Limits**: Varies by plan (typically generous for async)

---

## Skills Extraction Engine

### Multi-Pass Extraction Strategy

#### Pass 1: Multi-Word Skills (Exact Substring Matching)
- Sorted by length (longest first) to avoid partial matches
- Searches for exact substring in lowercase text
- Examples: "React.js", "AWS Lambda", "ASP.NET Core"
- Confidence: 0.70 - 0.95 based on frequency

#### Pass 2: Single-Word Skills (Word-Boundary Regex)
- Uses word boundaries: `\b{skill}\b`
- Prevents partial word matches (e.g., "use" in "useful")
- Examples: "Python", "Java", "React"
- Only processes skills not found in Pass 1

#### Pass 3: spaCy NER Enhancement (Optional)
- Loads pre-trained model: `en_core_web_sm`
- Extracts ORG entities and checks against skill database
- Boosts confidence by +0.1 for recognized organizations
- Fallback if model not installed (graceful degradation)

### Skill Database Structure

```python
SKILLS_DATABASE = {
  "Programming Languages": [
    "Python", "Java", "JavaScript", "TypeScript", ...
    # 35+ languages
  ],
  "Web Frameworks": [
    "React", "Angular", "Vue", "Django", "Flask", ...
    # 40+ frameworks
  ],
  "Databases": [
    "PostgreSQL", "MongoDB", "MySQL", "Redis", ...
    # 25+ databases
  ],
  "Cloud & DevOps": [
    "AWS", "Azure", "Docker", "Kubernetes", ...
    # 50+ tools
  ],
  "Data Science & ML": [
    "TensorFlow", "PyTorch", "scikit-learn", ...
    # 50+ tools
  ],
  # ... 10 more categories (Mobile, Testing, Tools, Architecture, Security, Soft Skills)
}
```

### Confidence Scoring Algorithm

```python
def _compute_confidence(skill_lower, text_lower):
    count = text_lower.count(skill_lower)
    if count >= 5:
        return 0.95  # Very high confidence
    if count >= 3:
        return 0.90  # High confidence
    if count >= 2:
        return 0.80  # Good confidence
    return 0.70      # Baseline confidence
```

### Output Format

```python
{
  "skill": "Python",
  "category": "Programming Languages",
  "confidence": 0.95
}
```

**Returns**: Sorted list by confidence (descending), then skill name (ascending)

### Skill Categorization

All 300+ skills are pre-mapped to categories:
1. **Programming Languages** (35+ skills)
2. **Web Frameworks** (40+ skills)
3. **Databases** (25+ skills)
4. **Cloud & DevOps** (50+ skills)
5. **Data Science & ML** (50+ skills)
6. **Mobile Development** (15+ skills)
7. **Testing** (20+ skills)
8. **Tools & Platforms** (60+ skills)
9. **Architecture & Patterns** (20+ skills)
10. **Security** (20+ skills)
11. **Soft Skills** (30+ skills)

### Example Extraction

**Resume Text**:
```
Senior Python Developer with 8 years of experience
Expertise in Django, Flask, and React
Experienced with PostgreSQL, MongoDB, and Redis
DevOps: Docker, Kubernetes, AWS, GitHub Actions
```

**Extracted Skills**:
```json
[
  {"skill": "Python", "category": "Programming Languages", "confidence": 0.95},
  {"skill": "Django", "category": "Web Frameworks", "confidence": 0.95},
  {"skill": "Flask", "category": "Web Frameworks", "confidence": 0.95},
  {"skill": "React", "category": "Web Frameworks", "confidence": 0.90},
  {"skill": "PostgreSQL", "category": "Databases", "confidence": 0.95},
  {"skill": "MongoDB", "category": "Databases", "confidence": 0.90},
  {"skill": "Redis", "category": "Databases", "confidence": 0.90},
  {"skill": "Docker", "category": "Cloud & DevOps", "confidence": 0.95},
  {"skill": "Kubernetes", "category": "Cloud & DevOps", "confidence": 0.95},
  {"skill": "AWS", "category": "Cloud & DevOps", "confidence": 0.90},
  {"skill": "GitHub Actions", "category": "Cloud & DevOps", "confidence": 0.85}
]
```

---

## ATS Score Calculation

### Complete Scoring Flow

```
Resume Text + Extracted Skills + Sections
    ↓
Calculate 5 Category Scores:
├─ Contact Info (0-100) → Weight 0.10
├─ Formatting (0-100) → Weight 0.20
├─ Skills Keywords (0-100) → Weight 0.30
├─ Experience (0-100) → Weight 0.25
└─ Education (0-100) → Weight 0.15
    ↓
Weighted Average = Σ(Category Score × Weight)
    ↓
Clamp to 0-100 range
    ↓
Round to 1 decimal place
    ↓
Generate Improvement Suggestions
    ↓
Return: {overall_score, breakdown, suggestions}
```

### Detailed Scoring Example

**Resume**:
```
John Smith
john@example.com | (555) 123-4567 | linkedin.com/in/johnsmith

PROFESSIONAL SUMMARY
Senior Software Engineer with 7+ years in Python, Django, and React development.

EXPERIENCE
Senior Backend Engineer at TechCorp (2020-Present)
• Led migration of monolith to microservices using Docker and Kubernetes
• Reduced API latency by 40% through Redis caching optimization
• Mentored 3 junior engineers
• Increased code coverage from 60% to 88%

EDUCATION
B.S. Computer Science, State University, 2015
AWS Solutions Architect Professional Certification, 2022

SKILLS
Languages: Python, JavaScript, SQL
Frameworks: Django, Flask, React
Databases: PostgreSQL, MongoDB
DevOps: Docker, Kubernetes, AWS, GitHub Actions
```

**Scoring Breakdown**:

| Category | Component | Score | Max | Details |
|----------|-----------|-------|-----|---------|
| **Contact Info** (10%) | Email | 35 | 35 | Found email |
| | Phone | 30 | 30 | Valid phone |
| | LinkedIn | 20 | 20 | Profile found |
| | Name | 15 | 15 | Name detected |
| **Total** | | **100** | **100** | **Score: 100** |
| **Formatting** (20%) | Sections | 30 | 30 | All present |
| | Bullets | 20 | 20 | 4 bullets (≥ 1) |
| | Length | 25 | 25 | ~300 words (optimal) |
| | Dates | 15 | 15 | Multiple dates found |
| | Special Chars | 10 | 10 | Clean formatting |
| **Total** | | **100** | **100** | **Score: 100** |
| **Skills** (30%) | Count | 40 | 50 | 10 skills |
| | Diversity | 20 | 30 | 3 categories |
| | Balance | 20 | 20 | Both technical & soft |
| **Total** | | **80** | **100** | **Score: 80** |
| **Experience** (25%) | Section | 20 | 20 | Present & detailed |
| | Metrics | 30 | 30 | 4 metrics (40%, 88%, etc.) |
| | Verbs | 25 | 25 | 5+ action verbs (Led, Reduced, Mentored) |
| | Keywords | 20 | 25 | Good industry terms |
| **Total** | | **95** | **100** | **Score: 95** |
| **Education** (15%) | Section | 30 | 30 | Present |
| | Degree | 30 | 30 | B.S. found |
| | Certifications | 20 | 20 | AWS cert found |
| | Other | 15 | 20 | Relevant info |
| **Total** | | **95** | **100** | **Score: 95** |

**Final Calculation**:
```
Overall = (100 × 0.10) + (100 × 0.20) + (80 × 0.30) + (95 × 0.25) + (95 × 0.15)
        = 10 + 20 + 24 + 23.75 + 14.25
        = 92.0 ← ATS Score
```

**Suggestions Generated**:
```json
[
  "Consider adding more quantifiable achievements (current: 4, optimal: 8+)",
  "Excellent contact information and formatting!",
  "Consider adding more technical skills or certifications",
  "Strong use of action verbs in experience section"
]
```

---

## Skills & ATS Distribution

### Skills Distribution Analysis

#### How Skills are Distributed

**At Database Level**:
- Each resume stores skills as JSON array in `skills_json` column
- Each skill object contains: skill name, category, confidence score
- Multiple resumes can have overlapping skills

**At Dashboard Level** (`/api/dashboard/skills`):
```python
skill_counter = Counter()       # Total skill frequency
category_counter = Counter()    # Total category frequency

for resume in user_resumes:
    for skill in resume.get_skills():
        skill_counter[skill_name] += 1      # Count occurrences
        category_counter[category] += 1      # Count category
```

**Response Structure**:
```json
{
  "skills": [
    {"skill": "Python", "count": 3},
    {"skill": "React", "count": 2},
    {"skill": "JavaScript", "count": 2}
  ],
  "categories": [
    {"category": "Programming Languages", "count": 5},
    {"category": "Web Frameworks", "count": 4}
  ],
  "total_unique_skills": 15,
  "total_categories": 8
}
```

### ATS Score Distribution Analysis

#### How ATS Scores are Stored & Displayed

**Storage**:
- Each resume has `ats_score` field (Float, 0.0-100.0)
- Stored at 1 decimal place precision
- Scores recalculated if resume is re-analyzed

**Dashboard Statistics** (`/api/dashboard/stats`):
```python
scores = [resume.ats_score for resume in user_resumes if resume.ats_score]
avg_ats_score = sum(scores) / len(scores)  # Average across resumes
```

**Response**:
```json
{
  "stats": {
    "total_resumes": 2,
    "avg_ats_score": 80.25,
    "total_interviews": 5,
    "avg_interview_score": 75.0,
    "total_coding_tests": 3,
    "coding_pass_rate": 66.7
  }
}
```

### Distribution Charts (Frontend Rendering)

#### 1. Skills Frequency Chart
- **Type**: Horizontal Bar Chart
- **X-axis**: Skill names (most frequent first)
- **Y-axis**: Occurrence count
- **Data Source**: `/api/dashboard/skills` → `skills` array

#### 2. Skills by Category Pie/Donut Chart
- **Type**: Pie or Donut Chart
- **Segments**: Each skill category
- **Size**: Proportional to count in that category
- **Data Source**: `/api/dashboard/skills` → `categories` array

#### 3. ATS Score Trend
- **Type**: Line Chart (if multiple resumes)
- **X-axis**: Resume number or upload date
- **Y-axis**: ATS score (0-100)
- **Data Source**: Aggregate from `/api/resume/list`

#### 4. ATS Score Distribution
- **Type**: Histogram or Gauge
- **Shows**: Current average ATS score
- **Range**: 0-100 with color coding
  - Red: 0-40 (Poor)
  - Yellow: 40-70 (Fair)
  - Green: 70-100 (Good)

#### 5. Skills Strength Matrix
- **Type**: Heatmap or Matrix
- **Rows**: Skill categories
- **Columns**: Individual resumes
- **Color intensity**: Number of skills in that category for each resume

### Visualization Example

**Dashboard Display**:
```
┌─ ATS Score Summary ─────────────────────┐
│ Average ATS Score: 82.5                 │
│ Best Score: 92.0 (Resume 1)             │
│ Worst Score: 73.0 (Resume 2)            │
│ Total Resumes: 2                        │
└─────────────────────────────────────────┘

┌─ Skills Distribution ───────────────────┐
│ Python:              ████████████ (12)  │
│ JavaScript:          ██████████ (10)    │
│ React:               █████████ (9)      │
│ PostgreSQL:          ████████ (8)       │
│ Docker:              ████████ (8)       │
│ ... (more skills)                       │
└─────────────────────────────────────────┘

┌─ Skills by Category ────────────────────┐
│ Programming Languages:  ████████ 35%    │
│ Web Frameworks:         ██████ 28%      │
│ Cloud & DevOps:         ████ 22%        │
│ Databases:              ██ 15%          │
│ ... (more categories)                   │
└─────────────────────────────────────────┘
```

---

## Configuration

### Environment Variables

Create `.env` file in backend root:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=postgresql://user:password@localhost/resumeai_db
# OR for SQLite (default if DATABASE_URL not set)
# DATABASE_URL=sqlite:///instance/app.db

# JWT
JWT_SECRET_KEY=your-jwt-secret-key

# Groq API
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5000,https://yourdomain.com

# Upload settings
UPLOAD_FOLDER=backend/uploads
MAX_CONTENT_LENGTH=16777216  # 16 MB in bytes
```

### Database Configuration

#### SQLite (Development)
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/app.db'
```

#### PostgreSQL (Production - Render)
```bash
# Render provides DATABASE_URL in format:
# postgres://user:password@host:port/dbname

# Auto-converts postgres:// → postgresql:// for compatibility
if _db_url.startswith('postgres://'):
    _db_url = _db_url.replace('postgres://', 'postgresql://', 1)
```

### CORS Configuration

```python
CORS(app, resources={
    r"/api/*": {
        "origins": app.config['CORS_ORIGINS'],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

### File Upload Configuration

```python
UPLOAD_FOLDER = 'backend/uploads'      # Directory for PDFs
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
ALLOWED_EXTENSIONS = {'pdf'}           # Only PDFs allowed
```

### JWT Token Configuration

```python
JWT_SECRET_KEY = 'jwt-secret-key'
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)  # Token expires in 24 hours
JWT_TOKEN_LOCATION = ['headers']       # Tokens in Authorization header
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'             # Format: Bearer {token}
```

---

## Summary

This backend system provides a comprehensive resume analysis platform featuring:

✅ **Robust Authentication**: JWT-based secure authentication  
✅ **Advanced PDF Parsing**: Multi-page PDF text extraction with cleaning  
✅ **Comprehensive Skills Detection**: 300+ skills across 11 categories  
✅ **Intelligent ATS Scoring**: 5-category weighted scoring system  
✅ **AI-Powered Insights**: Groq LLM integration for recommendations  
✅ **Job Matching**: Resume-to-job-description comparison  
✅ **Dashboard Analytics**: Aggregated statistics and distributions  
✅ **Scalable Architecture**: Microservices-ready modular design  
✅ **Production Ready**: Gunicorn deployment, environment configuration, error handling  

---

**Documentation Version**: 1.0  
**Last Updated**: June 2, 2024  
**Backend Version**: Flask 3.1.1+
