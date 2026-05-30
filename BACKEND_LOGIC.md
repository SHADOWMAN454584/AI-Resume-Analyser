# ⚙️ Backend Architecture & Logic Reference

This document provides a technical deep dive into the backend logic of ResumeAI, specifically focusing on the resume processing pipeline and the job matching engine.

## 🏗️ System Architecture

The backend is built as a RESTful API using **Flask** and **SQLAlchemy**, integrating specialized services for PDF parsing, NLP, and AI-driven analysis.

### Data Flow Pipeline
1. **Upload**: A PDF resume is uploaded via the `/api/resume/upload` endpoint.
2. **Parsing**: `pdf_parser.py` extracts raw text and identifies structural sections.
3. **Extraction**: `nlp_engine.py` uses spaCy and a predefined skills database to identify technical skills and entities.
4. **Scoring**: `ats_scorer.py` applies a weighted algorithm to calculate the ATS compatibility score.
5. **AI Insight**: `ai_analyzer.py` sends the parsed text to Groq AI (Llama 3.3) to generate qualitative insights.
6. **Persistence**: The analysis results and raw text are stored in the SQLite database.

---

## 🎯 Job Matching Logic

The Job Matching feature allows users to compare their existing resume against a specific job description to identify gaps and opportunities for optimization.

### 🛠️ Implementation Details
The matching logic is implemented in `backend/services/job_matcher.py` and exposed via the `POST /api/resume/match-job` endpoint.

### 🧠 AI-Driven Comparison Process
Instead of simple keyword counting, the system uses **Large Language Model (LLM) Reasoning** via the Groq API:

1. **Input Preparation**: 
   - The system retrieves the raw text of the specified resume.
   - It takes the user-provided job description.
   - Both are truncated (Resume: 5000 chars, JD: 3000 chars) to fit the model's context window efficiently.

2. **Prompt Engineering**:
   The AI is prompted as an "Expert ATS and Career Advisor". The prompt strictly enforces a **JSON output format** to ensure programmatic reliability.

3. **Analysis Dimensions**:
   The AI evaluates the following:
   - **Match Percentage**: A holistic score (0-100) representing how well the candidate's profile fits the role.
   - **Matching Skills**: A list of requirements from the JD that are explicitly or implicitly present in the resume.
   - **Missing Skills**: Critical requirements from the JD that are absent from the resume.
   - **Improvement Suggestions**: 3-5 actionable, specific tips to better align the resume with the JD.

4. **Alternative Role Suggestions**:
   - **The 40% Rule**: If the `match_percentage` is less than 40%, the system assumes the candidate is not a good fit for this specific role.
   - In such cases, the AI suggests 3-5 alternative job titles that better match the candidate's current skill set.
   - For matches $\ge 40\%$, this list is returned empty to keep the focus on the target job.

### 📊 Output Schema
The result is returned as a structured JSON object:
```json
{
    "match_percentage": 75,
    "matching_skills": ["Python", "React", "AWS"],
    "missing_skills": ["Kubernetes", "Terraform"],
    "improvement_suggestions": [
        "Quantify your experience with AWS by mentioning specific cost-saving metrics.",
        "Add a project demonstrating Kubernetes orchestration to fill the missing skill gap.",
        "Highlight your leadership experience in the professional summary."
    ],
    "alternative_jobs": []
}
```
