# 🚀 ResumeAI - AI-Powered Career Platform

An intelligent platform that helps professionals optimize their resumes and discover job gaps using AI-driven analysis and real-time feedback.

## 🌐 Live Deployment

- **Deployment Server**: [https://resumeai-backend-c3q4.onrender.com](https://resumeai-backend-c3q4.onrender.com)

> **⚠️ Note:** The backend is deployed on Render's free tier, which spins down after periods of inactivity. **It may take up to 5 minutes to start the server** upon your first request. Please be patient!

## ✨ Features

### 📄 Resume Analysis
- **AI-Powered Deep Analysis**: Uses Groq API (llama-3.3-70b) to analyze resume structure, content, and formatting
- **ATS Score Calculation**: Get your Applicant Tracking System compatibility score (0-100)
- **Detailed Breakdown**: Contact information, formatting, keywords, experience, and education scores
- **Skill Extraction**: Automatically detect and categorize 300+ technical skills using spaCy NLP
- **Job Matching**: Compare your resume against specific job descriptions for match percentages and gap analysis
- **Actionable Recommendations**: AI-generated improvement suggestions specific to your resume

### 📊 Dashboard Analytics
- **Comprehensive Statistics**: Track your ATS scores, skills, and progress over time
- **Visual Insights**: Beautiful charts and analytics for career tracking
- **Resume History**: View and compare multiple resume analyses

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.1.1 with Flask-CORS, Flask-SQLAlchemy, Flask-JWT-Extended
- **AI Integration**: Groq API (llama-3.3-70b-versatile model)
- **PDF Processing**: pdfplumber 0.11.4 for text extraction and section identification
- **NLP**: spaCy (en_core_web_sm) for entity recognition and skill extraction
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens for secure API access

### Frontend
- **Framework**: React 19.0.0 with React Router 7.1.0
- **Build Tool**: Vite 6.0.0
- **Data Visualization**: Recharts 2.15.0
- **HTTP Client**: Axios with JWT interceptors
- **Styling**: CSS3 with custom design system

### Environment
- **Python**: 3.11 virtual environment
- **Node.js**: Latest LTS with npm

---

## 📦 Project Structure

```
ResumeAI/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Environment variables (local only)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── resume.py          # Resume SQLAlchemy model
│   │   └── user.py            # User model
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── resume.py          # Resume upload & analysis endpoints
│   │   └── dashboard.py        # Dashboard statistics endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── ai_analyzer.py     # Groq AI analysis service
│   │   ├── pdf_parser.py      # PDF extraction and section parsing
│   │   ├── nlp_engine.py      # Skill & entity extraction
│   │   └── ats_scorer.py      # ATS score calculation
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py         # Utility functions
│   ├── uploads/               # Uploaded PDF storage
│   └── instance/              # SQLite database location

├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── App.jsx            # Main application component
│   │   ├── main.jsx           # React entry point
│   │   ├── index.css          # Global styles
│   │   ├── api/
│   │   │   └── api.js         # Centralized API client with JWT interceptors
│   │   ├── context/
│   │   │   └── AuthContext.jsx # Authentication context
│   │   ├── components/
│   │   │   ├── FileUpload.jsx/css
│   │   │   ├── Navbar.jsx/css
│   │   │   ├── ScoreGauge.jsx/css
│   │   │   ├── Sidebar.jsx/css
│   │   │   ├── SkillBadge.jsx/css
│   │   │   └── StatsCard.jsx/css
│   │   └── pages/
│   │       ├── Dashboard.jsx/css
│   │       ├── Landing.jsx/css
│   │       ├── Login.jsx/css
│   │       ├── Register.jsx/css
│   │       ├── ResumeAnalysis.jsx/css
│   │       └── ResumeUpload.jsx/css

└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js LTS
- Groq API Key (get it from [groq.com](https://console.groq.com))

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv ..\.venv
..\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Create .env file with your Groq API key
echo "GROQ_API_KEY=your_api_key_here" > .env

# Run Flask development server
$env:FLASK_APP="app.py"
flask run --port=5001
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server (runs on port 5174)
npm run dev

# Build for production
npm run build
```

### Access the Application
- **Frontend**: http://localhost:5174
- **Backend API**: http://localhost:5001/api

---

## 🔑 Key Technologies & Features

### AI Analysis Engine
- **Groq llama-3.3-70b model** for resume analysis
- Generates: candidate summary, key strengths, improvement areas, and recommendations
- JSON-formatted responses with structured output

### NLP & Skill Detection
- **300+ technical skills** organized by category:
  - Programming Languages (Python, Java, C++, etc.)
  - Web Frameworks (React, Django, Spring, etc.)
  - Databases (MySQL, MongoDB, PostgreSQL, etc.)
  - Cloud & DevOps (AWS, Azure, Docker, etc.)
  - Data Science & ML (TensorFlow, PyTorch, Pandas, etc.)
  - And more...

### ATS Scoring Algorithm
- Contact Information (10%)
- Formatting & Structure (20%)
- Keywords Optimization (25%)
- Experience & Achievements (25%)
- Education & Certifications (20%)

---

## 🔐 Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **CORS Protection**: Cross-Origin Resource Sharing configured
- **Environment Variables**: Sensitive keys stored in .env (not committed)
- **Input Validation**: Server-side validation on all endpoints

---

## 📱 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/profile` - Get current user profile

### Resume Management
- `POST /api/resume/upload` - Upload and analyze resume (PDF)
- `GET /api/resume/list` - List all user resumes
- `GET /api/resume/<id>` - Get resume details with analysis
- `POST /api/resume/match-job` - Match resume against a job description
- `DELETE /api/resume/<id>` - Delete resume

### Dashboard
- `GET /api/dashboard/stats` - Overall statistics
- `GET /api/dashboard/latest_resume` - Latest resume with insights
- `GET /api/dashboard/skills` - Skill distribution
- `GET /api/dashboard/progress` - Progress over time

---

## 🎯 Current Status

✅ **Completed Features**
- User authentication and JWT tokens
- Resume PDF upload and parsing
- AI-powered resume analysis with Groq API
- Skill extraction (300+ skills database)
- ATS score calculation with breakdown
- Job matching with gap analysis and role suggestions
- Dashboard with statistics and analytics
- Resume history and management
- Responsive UI with modern design

🚧 **In Development**
- Real-time progress tracking
- Advanced analytics and trends

---

## 📝 Environment Configuration

Create a `.env` file in the `backend/` directory:

```
GROQ_API_KEY=your_groq_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///instance/resumeai.db
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

---

## 📄 License

This project is provided as-is for educational and professional purposes.

---

## 📧 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for career advancement**
