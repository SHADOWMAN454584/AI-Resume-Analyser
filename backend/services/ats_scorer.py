"""
ATS (Applicant Tracking System) scoring engine.
Evaluates resumes on multiple criteria and generates improvement suggestions.
"""
import re


def calculate_ats_score(text, skills, sections):
    """
    Calculate an ATS compatibility score for a resume.

    Args:
        text: Full resume text.
        skills: List of extracted skill dicts (from nlp_engine.extract_skills).
        sections: Dict of resume sections (from pdf_parser.extract_sections).

    Returns:
        Dict with 'overall_score' (0-100) and 'breakdown' of category scores.
    """
    breakdown = {
        'contact_info': _score_contact_info(text, sections.get('contact', '')),
        'formatting': _score_formatting(text, sections),
        'skills_keywords': _score_skills(skills),
        'experience': _score_experience(text, sections.get('experience', '')),
        'education': _score_education(text, sections.get('education', ''), sections.get('certifications', ''))
    }

    # Weighted overall score
    weights = {
        'contact_info': 0.10,
        'formatting': 0.20,
        'skills_keywords': 0.30,
        'experience': 0.25,
        'education': 0.15
    }

    overall = sum(breakdown[cat]['score'] * weights[cat] for cat in weights)
    overall = round(min(max(overall, 0), 100), 1)

    suggestions = generate_suggestions(breakdown)

    return {
        'overall_score': overall,
        'breakdown': breakdown,
        'suggestions': suggestions
    }


# ---------------------------------------------------------------------------
# Category scoring functions
# ---------------------------------------------------------------------------

def _score_contact_info(text, contact_section):
    """Score contact information presence (0-100)."""
    score = 0
    details = []
    search_text = (contact_section + '\n' + text[:2000]).lower()

    # Email (35 pts)
    email_pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    if re.search(email_pattern, search_text):
        score += 35
        details.append('Email found')
    else:
        details.append('Missing email address')

    # Phone (30 pts)
    phone_pattern = r'(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)?\d{3}[-.\s]?\d{4}'
    phone_matches = re.findall(phone_pattern, search_text)
    valid_phones = [p for p in phone_matches if len(re.sub(r'\D', '', p)) >= 10]
    if valid_phones:
        score += 30
        details.append('Phone number found')
    else:
        details.append('Missing phone number')

    # LinkedIn (20 pts)
    if 'linkedin' in search_text:
        score += 20
        details.append('LinkedIn profile found')
    else:
        details.append('Missing LinkedIn profile')

    # Name detection – usually at top (15 pts)
    lines = text.strip().split('\n')
    if lines and len(lines[0].strip()) > 2 and not re.match(r'^[\d()+\-.\s]+$', lines[0].strip()):
        score += 15
        details.append('Name appears present')
    else:
        details.append('Name may be missing or unclear')

    return {'score': min(score, 100), 'max_score': 100, 'details': details, 'weight': '10%'}


def _score_formatting(text, sections):
    """Score resume formatting quality (0-100)."""
    score = 0
    details = []

    # Section headers present (30 pts)
    important_sections = ['experience', 'education', 'skills']
    sections_found = sum(1 for s in important_sections if sections.get(s, '').strip())
    section_score = int((sections_found / len(important_sections)) * 30)
    score += section_score
    if sections_found == len(important_sections):
        details.append('All key sections present')
    else:
        missing = [s.title() for s in important_sections if not sections.get(s, '').strip()]
        details.append(f'Missing sections: {", ".join(missing)}')

    # Bullet points usage (20 pts)
    bullet_patterns = [r'[•●○◦▪▸►\-\*]', r'^\d+[.)]\s']
    bullet_count = 0
    for line in text.split('\n'):
        stripped = line.strip()
        for pat in bullet_patterns:
            if re.match(pat, stripped):
                bullet_count += 1
                break
    if bullet_count >= 10:
        score += 20
        details.append(f'Good use of bullet points ({bullet_count} found)')
    elif bullet_count >= 5:
        score += 12
        details.append(f'Some bullet points found ({bullet_count}), consider using more')
    elif bullet_count >= 1:
        score += 6
        details.append(f'Few bullet points ({bullet_count}), add more for readability')
    else:
        details.append('No bullet points detected – use bullets to highlight achievements')

    # Resume length (25 pts)
    word_count = len(text.split())
    if 300 <= word_count <= 1200:
        score += 25
        details.append(f'Good length ({word_count} words)')
    elif 200 <= word_count < 300:
        score += 15
        details.append(f'Resume may be too short ({word_count} words)')
    elif 1200 < word_count <= 1800:
        score += 18
        details.append(f'Resume is slightly long ({word_count} words)')
    elif word_count > 1800:
        score += 10
        details.append(f'Resume is too long ({word_count} words), consider condensing')
    else:
        score += 5
        details.append(f'Resume is very short ({word_count} words)')

    # Consistency – check for date formats (15 pts)
    date_pattern = r'\b(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4}|\d{4})\b'
    dates = re.findall(date_pattern, text)
    if len(dates) >= 2:
        score += 15
        details.append('Date formatting detected')
    elif len(dates) == 1:
        score += 8
        details.append('Limited date information')
    else:
        details.append('No dates found – add dates to experience entries')

    # No excessive special characters (10 pts)
    special_ratio = len(re.findall(r'[^a-zA-Z0-9\s.,;:\-!?\'\"()/&@#+•●]', text)) / max(len(text), 1)
    if special_ratio < 0.02:
        score += 10
        details.append('Clean formatting with minimal special characters')
    elif special_ratio < 0.05:
        score += 5
        details.append('Some unusual characters detected')
    else:
        details.append('Too many special characters – may confuse ATS parsers')

    return {'score': min(score, 100), 'max_score': 100, 'details': details, 'weight': '20%'}


def _score_skills(skills):
    """Score skills/keywords presence (0-100)."""
    score = 0
    details = []
    skill_count = len(skills) if skills else 0

    # Number of skills (50 pts)
    if skill_count >= 15:
        score += 50
        details.append(f'Excellent skill coverage ({skill_count} skills)')
    elif skill_count >= 10:
        score += 40
        details.append(f'Good skill coverage ({skill_count} skills)')
    elif skill_count >= 6:
        score += 28
        details.append(f'Moderate skill coverage ({skill_count} skills)')
    elif skill_count >= 3:
        score += 15
        details.append(f'Limited skills detected ({skill_count}), add more relevant keywords')
    elif skill_count >= 1:
        score += 8
        details.append(f'Very few skills detected ({skill_count})')
    else:
        details.append('No skills detected – add a dedicated skills section')

    # Category diversity (30 pts)
    if skills:
        categories = set(s.get('category', '') for s in skills)
        cat_count = len(categories)
        if cat_count >= 5:
            score += 30
            details.append(f'Diverse skill categories ({cat_count} categories)')
        elif cat_count >= 3:
            score += 20
            details.append(f'Good category diversity ({cat_count} categories)')
        elif cat_count >= 2:
            score += 12
            details.append(f'Limited category diversity ({cat_count} categories)')
        else:
            score += 5
            details.append('Skills are from a single category – broaden your skill set')
    else:
        details.append('No skill categories to evaluate')

    # Technical vs soft skills balance (20 pts)
    if skills:
        soft = sum(1 for s in skills if s.get('category') == 'Soft Skills')
        technical = skill_count - soft
        if technical > 0 and soft > 0:
            score += 20
            details.append(f'Good balance of technical ({technical}) and soft ({soft}) skills')
        elif technical > 0:
            score += 12
            details.append('Only technical skills found – consider adding soft skills')
        elif soft > 0:
            score += 8
            details.append('Only soft skills found – add technical skills')
    else:
        details.append('Cannot evaluate skill balance')

    return {'score': min(score, 100), 'max_score': 100, 'details': details, 'weight': '30%'}


def _score_experience(text, experience_section):
    """Score work experience detail (0-100)."""
    score = 0
    details = []
    search_text = experience_section if experience_section else text

    # Presence of experience section (20 pts)
    if experience_section and len(experience_section.strip()) > 50:
        score += 20
        details.append('Experience section found')
    elif experience_section and experience_section.strip():
        score += 10
        details.append('Experience section is thin – add more detail')
    else:
        details.append('No dedicated experience section found')

    # Quantifiable achievements (30 pts)
    number_patterns = [
        r'\d+\s*%',       # percentages
        r'\$[\d,.]+',     # dollar amounts
        r'\b\d{2,}\b',    # numbers (2+ digits)
    ]
    quant_count = 0
    for pat in number_patterns:
        quant_count += len(re.findall(pat, search_text))

    if quant_count >= 8:
        score += 30
        details.append(f'Strong quantifiable achievements ({quant_count} metrics)')
    elif quant_count >= 4:
        score += 20
        details.append(f'Some quantifiable achievements ({quant_count} metrics)')
    elif quant_count >= 1:
        score += 10
        details.append(f'Few quantifiable metrics ({quant_count}) – add numbers to show impact')
    else:
        details.append('No quantifiable achievements – use numbers to demonstrate impact')

    # Action verbs (25 pts)
    action_verbs = [
        'led', 'managed', 'developed', 'built', 'designed', 'implemented',
        'created', 'improved', 'increased', 'reduced', 'delivered',
        'achieved', 'launched', 'optimized', 'streamlined', 'mentored',
        'coordinated', 'established', 'drove', 'generated', 'resolved',
        'spearheaded', 'orchestrated', 'engineered', 'architected',
        'automated', 'deployed', 'migrated', 'refactored', 'integrated',
        'collaborated', 'analyzed', 'executed', 'transformed'
    ]
    search_lower = search_text.lower()
    verbs_found = sum(1 for v in action_verbs if re.search(r'\b' + v + r'\b', search_lower))
    if verbs_found >= 8:
        score += 25
        details.append(f'Excellent use of action verbs ({verbs_found} found)')
    elif verbs_found >= 4:
        score += 18
        details.append(f'Good use of action verbs ({verbs_found} found)')
    elif verbs_found >= 2:
        score += 10
        details.append(f'Some action verbs ({verbs_found}), use more strong verbs')
    else:
        details.append('Few/no action verbs – start bullet points with strong verbs')

    # Job titles (15 pts)
    title_patterns = [
        r'(?i)\b(?:software|senior|junior|lead|staff|principal|intern|associate|manager|director|vp|head|chief)\b',
        r'(?i)\b(?:engineer|developer|architect|analyst|consultant|designer|administrator|specialist|coordinator)\b'
    ]
    title_found = any(re.search(pat, search_text) for pat in title_patterns)
    if title_found:
        score += 15
        details.append('Job titles/roles detected')
    else:
        details.append('No clear job titles found – include your role titles')

    # Company mentions (10 pts)
    company_indicators = [r'(?i)\b(?:inc|corp|llc|ltd|co\.|company|technologies|solutions|systems|group|enterprises)\b']
    if any(re.search(pat, search_text) for pat in company_indicators):
        score += 10
        details.append('Company names appear present')
    else:
        score += 3
        details.append('Company names may be missing or unclear')

    return {'score': min(score, 100), 'max_score': 100, 'details': details, 'weight': '25%'}


def _score_education(text, education_section, certifications_section):
    """Score education and certifications (0-100)."""
    score = 0
    details = []
    search_text = education_section + '\n' + certifications_section + '\n' + text

    # Degree mentions (50 pts)
    degree_patterns = [
        r'(?i)\b(?:bachelor|master|doctorate|ph\.?d|b\.?s\.?|m\.?s\.?|b\.?a\.?|m\.?a\.?|b\.?e\.?|m\.?e\.?|b\.?tech|m\.?tech|mba|bca|mca|bsc|msc)\b',
        r'(?i)\b(?:degree|diploma|graduate|post\s*graduate|undergraduate)\b'
    ]
    degree_found = any(re.search(pat, search_text) for pat in degree_patterns)
    if degree_found:
        score += 50
        details.append('Educational degree detected')
    else:
        details.append('No degree or diploma mentioned')

    # University / institution (20 pts)
    institution_patterns = [
        r'(?i)\b(?:university|college|institute|school|academy|polytechnic)\b'
    ]
    if any(re.search(pat, search_text) for pat in institution_patterns):
        score += 20
        details.append('Educational institution mentioned')
    else:
        details.append('No institution name detected')

    # Certifications (20 pts)
    cert_patterns = [
        r'(?i)\b(?:certified|certification|certificate|credential|licensed|accredited)\b',
        r'(?i)\b(?:AWS\s+Certified|PMP|CPA|CFA|CISSP|CompTIA|CCNA|CCNP|Azure\s+Certified|Google\s+Certified|Scrum\s+Master|TOGAF)\b'
    ]
    if any(re.search(pat, search_text) for pat in cert_patterns):
        score += 20
        details.append('Certifications detected')
    else:
        details.append('No certifications found – consider adding relevant ones')

    # GPA / Honours (10 pts)
    gpa_patterns = [
        r'(?i)\b(?:gpa|cgpa|grade|honors|honours|cum laude|magna|summa|distinction|first class|dean.s list)\b'
    ]
    if any(re.search(pat, search_text) for pat in gpa_patterns):
        score += 10
        details.append('Academic honours or GPA mentioned')
    else:
        details.append('No GPA or honours mentioned')

    return {'score': min(score, 100), 'max_score': 100, 'details': details, 'weight': '15%'}


# ---------------------------------------------------------------------------
# Suggestion generator
# ---------------------------------------------------------------------------

def generate_suggestions(breakdown):
    """
    Generate actionable improvement suggestions based on the scoring breakdown.

    Args:
        breakdown: Dict of category score results.

    Returns:
        List of suggestion strings.
    """
    suggestions = []

    # Contact info suggestions
    contact = breakdown.get('contact_info', {})
    if contact.get('score', 0) < 70:
        for detail in contact.get('details', []):
            if 'Missing' in detail or 'missing' in detail:
                suggestions.append(f"Contact: {detail}. Add it to the top of your resume.")

    # Formatting suggestions
    formatting = breakdown.get('formatting', {})
    if formatting.get('score', 0) < 60:
        suggestions.append("Use clear section headers (Experience, Education, Skills) so ATS systems can parse your resume.")
    for detail in formatting.get('details', []):
        if 'Missing sections' in detail:
            suggestions.append(f"Add the following sections: {detail.split(': ', 1)[-1]}")
        if 'bullet' in detail.lower() and ('few' in detail.lower() or 'no' in detail.lower()):
            suggestions.append("Use bullet points to list your achievements – aim for 3-5 per role.")
        if 'too long' in detail.lower():
            suggestions.append("Keep your resume to 1-2 pages. Remove outdated or irrelevant information.")
        if 'too short' in detail.lower() or 'very short' in detail.lower():
            suggestions.append("Your resume is too brief. Expand on your experience, projects, and skills.")

    # Skills suggestions
    skills = breakdown.get('skills_keywords', {})
    if skills.get('score', 0) < 50:
        suggestions.append("Add a dedicated 'Skills' section listing your technical and soft skills.")
        suggestions.append("Include keywords from the job description you are targeting.")
    for detail in skills.get('details', []):
        if 'single category' in detail.lower():
            suggestions.append("Diversify your skills – include tools, frameworks, and soft skills alongside core technologies.")
        if 'only technical' in detail.lower():
            suggestions.append("Add soft skills like Leadership, Communication, or Project Management.")
        if 'only soft' in detail.lower():
            suggestions.append("Add technical skills relevant to your field.")

    # Experience suggestions
    experience = breakdown.get('experience', {})
    if experience.get('score', 0) < 60:
        suggestions.append("Strengthen your experience section with specific achievements and metrics.")
    for detail in experience.get('details', []):
        if 'quantifiable' in detail.lower() and ('few' in detail.lower() or 'no' in detail.lower()):
            suggestions.append("Quantify your impact: use numbers, percentages, and dollar amounts (e.g., 'Reduced load time by 40%').")
        if 'action verbs' in detail.lower() and ('few' in detail.lower() or 'some' in detail.lower()):
            suggestions.append("Start bullet points with strong action verbs: Led, Built, Optimized, Deployed, etc.")
        if 'job titles' in detail.lower() and 'no' in detail.lower():
            suggestions.append("Clearly state your job title for each position.")

    # Education suggestions
    education = breakdown.get('education', {})
    if education.get('score', 0) < 50:
        suggestions.append("Include your educational background with degree, institution, and graduation year.")
    for detail in education.get('details', []):
        if 'no certifications' in detail.lower() or 'no certification' in detail.lower():
            suggestions.append("Consider adding relevant industry certifications to strengthen your profile.")

    # Generic high-level tips if overall is low
    if not suggestions:
        suggestions.append("Your resume is well-structured. Keep it updated with your latest achievements!")

    return suggestions
