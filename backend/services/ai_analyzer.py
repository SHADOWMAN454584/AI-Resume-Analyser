"""
AI Analyzer module using Groq API for resume assessment and recommendations.
"""
import os
import json
from groq import Groq

def analyze_resume_with_ai(resume_text):
    """
    Sends the resume text to the Groq API to extract insights and recommendations.
    Returns a dictionary containing the extracted insights.
    """
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {"error": "Groq API key not configured"}
        
    client = Groq(api_key=api_key)
    
    # We truncate the resume text slightly if it's too huge, but typical resumes are fine.
    text_to_analyze = resume_text[:6000] 
    
    prompt = f"""
    You are an expert ATS and recruitment AI. 
    Analyze the following resume text and provide exactly a JSON object in this format (no markdown, just raw JSON):
    {{
        "candidate_summary": "A short 2-sentence summary of the candidate's profile.",
        "key_strengths": ["Strength 1", "Strength 2", "Strength 3"],
        "areas_for_improvement": ["Improvement 1", "Improvement 2"],
        "ai_recommendation": "A short paragraph with actionable advice for the candidate to improve their resume."
    }}

    Resume Text:
    ---
    {text_to_analyze}
    ---
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert ATS. You must ONLY output a valid JSON object. No explanation, no markdown tags."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1024,
            response_format={"type": "json_object"}
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Strip potential markdown formatting if the model still includes it
        if response_text.startswith("```"):
            # find first newline or end of the first line
            newline_idx = response_text.find("\n")
            if newline_idx != -1:
                response_text = response_text[newline_idx+1:]
            
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        result = json.loads(response_text.strip())
        return result
    except Exception as e:
        print(f"Error calling Groq API: {str(e)}")
        return {
            "error": "Failed to generate AI analysis.",
            "details": str(e)
        }
