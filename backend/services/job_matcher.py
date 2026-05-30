"""
Job Description Matcher — compares resume text against a job description
using Groq AI to produce match scores, missing skills, and alternative job suggestions.
"""
import os
import json
from groq import Groq


def match_resume_to_job(resume_text, job_description):
    """
    Compare resume_text against job_description using Groq AI.

    Returns a dict:
        match_percentage: int (0-100)
        matching_skills: list[str]
        missing_skills: list[str]
        improvement_suggestions: list[str]
        alternative_jobs: list[str]   (populated only when match < 40%)
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "Groq API key not configured"}

    client = Groq(api_key=api_key)

    # Truncate to stay within token budget
    resume_truncated = resume_text[:5000]
    jd_truncated = job_description[:3000]

    prompt = f"""
You are an expert ATS (Applicant Tracking System) and career advisor AI.

Compare the following RESUME with the JOB DESCRIPTION and produce ONLY a valid JSON object (no markdown, no explanation) in this exact format:

{{
    "match_percentage": <integer 0-100 — how well the resume matches the job description>,
    "matching_skills": ["skill1", "skill2", ...],
    "missing_skills": ["skill1", "skill2", ...],
    "improvement_suggestions": [
        "Specific actionable suggestion 1",
        "Specific actionable suggestion 2",
        "Specific actionable suggestion 3"
    ],
    "alternative_jobs": ["Job Title 1", "Job Title 2", "Job Title 3"]
}}

Rules:
- match_percentage must be an honest assessment of how well the resume fits the job.
- matching_skills: list every skill/technology/requirement from the JD that IS present in the resume.
- missing_skills: list every skill/technology/requirement from the JD that is NOT present in the resume.
- improvement_suggestions: give 3-5 specific, actionable improvements the candidate should make to their resume to better fit this job.
- alternative_jobs: suggest 3-5 job titles/roles that the candidate's current resume is BETTER suited for. Only populate this if match_percentage < 40. If match_percentage >= 40, set to an empty array [].

RESUME:
---
{resume_truncated}
---

JOB DESCRIPTION:
---
{jd_truncated}
---
"""

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS and career advisor. Output ONLY valid JSON. No markdown, no explanation."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500,
            response_format={"type": "json_object"}
        )

        response_text = completion.choices[0].message.content.strip()

        # Strip potential markdown fencing
        if response_text.startswith("```"):
            newline_idx = response_text.find("\n")
            if newline_idx != -1:
                response_text = response_text[newline_idx + 1:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]

        result = json.loads(response_text.strip())

        # Ensure all expected keys exist
        result.setdefault("match_percentage", 0)
        result.setdefault("matching_skills", [])
        result.setdefault("missing_skills", [])
        result.setdefault("improvement_suggestions", [])
        result.setdefault("alternative_jobs", [])

        # Enforce the 40% rule
        if result["match_percentage"] >= 40:
            result["alternative_jobs"] = []

        return result

    except Exception as e:
        print(f"Error in job matching (Groq): {str(e)}")
        return {
            "error": "Failed to match resume against job description.",
            "details": str(e)
        }
