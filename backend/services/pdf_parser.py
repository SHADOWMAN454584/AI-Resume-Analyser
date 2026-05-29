"""
PDF parsing service using pdfplumber.
Extracts text and identifies resume sections.
"""
import re
import pdfplumber


def parse_pdf(file_path):
    """
    Extract text from a PDF file.

    Args:
        file_path: Absolute path to the PDF file.

    Returns:
        Cleaned extracted text as a string.

    Raises:
        ValueError: If the file cannot be parsed or contains no text.
    """
    try:
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        if not text_parts:
            raise ValueError("No readable text found in the PDF. The file may be image-based or empty.")

        raw_text = "\n".join(text_parts)
        return _clean_text(raw_text)

    except pdfplumber.pdfminer.pdfparser.PDFSyntaxError:
        raise ValueError("Invalid PDF file format.")
    except Exception as e:
        if isinstance(e, ValueError):
            raise
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def _clean_text(text):
    """
    Normalize whitespace and remove non-printable characters.

    Args:
        text: Raw extracted text.

    Returns:
        Cleaned text string.
    """
    # Remove non-printable characters (keep newlines, tabs, spaces)
    text = re.sub(r'[^\x20-\x7E\n\t]', ' ', text)
    # Normalize multiple spaces to single space
    text = re.sub(r'[ \t]+', ' ', text)
    # Normalize multiple newlines to double newline
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Strip leading/trailing whitespace from each line
    lines = [line.strip() for line in text.split('\n')]
    text = '\n'.join(lines)
    # Remove leading/trailing whitespace
    return text.strip()


def extract_sections(text):
    """
    Identify and extract common resume sections from text.

    Args:
        text: Cleaned resume text.

    Returns:
        Dictionary mapping section names to their content.
    """
    section_patterns = {
        'contact': [
            r'(?i)^(?:contact\s*(?:info(?:rmation)?)?|personal\s*(?:info(?:rmation)?|details))\s*[:\-]?\s*$'
        ],
        'summary': [
            r'(?i)^(?:(?:professional\s+|career\s+|executive\s+)?summary|(?:career\s+)?objective|profile|about\s*me)\s*[:\-]?\s*$'
        ],
        'experience': [
            r'(?i)^(?:(?:work|professional|employment)\s*(?:experience|history)|experience|work\s*history)\s*[:\-]?\s*$'
        ],
        'education': [
            r'(?i)^(?:education(?:al\s+(?:background|qualifications))?|academic\s*(?:background|qualifications|history))\s*[:\-]?\s*$'
        ],
        'skills': [
            r'(?i)^(?:(?:technical\s+|core\s+|key\s+|professional\s+)?skills|(?:areas\s+of\s+)?expertise|competencies|technologies|tech\s*stack)\s*[:\-]?\s*$'
        ],
        'projects': [
            r'(?i)^(?:(?:key\s+|notable\s+|personal\s+|academic\s+)?projects|portfolio)\s*[:\-]?\s*$'
        ],
        'certifications': [
            r'(?i)^(?:certifications?|licenses?\s*(?:&|and)?\s*certifications?|professional\s+(?:certifications?|development)|awards?\s*(?:&|and)?\s*(?:certifications?|achievements?)|achievements?)\s*[:\-]?\s*$'
        ]
    }

    lines = text.split('\n')
    sections = {
        'contact': '',
        'summary': '',
        'experience': '',
        'education': '',
        'skills': '',
        'projects': '',
        'certifications': '',
        'other': ''
    }

    current_section = 'contact'  # Default: content before first header is treated as contact
    section_contents = {key: [] for key in sections}

    for line in lines:
        stripped = line.strip()
        if not stripped:
            section_contents[current_section].append('')
            continue

        matched_section = None
        for section_name, patterns in section_patterns.items():
            for pattern in patterns:
                if re.match(pattern, stripped):
                    matched_section = section_name
                    break
            if matched_section:
                break

        if matched_section:
            current_section = matched_section
        else:
            section_contents[current_section].append(stripped)

    # Build final section text
    for key in sections:
        content = '\n'.join(section_contents[key]).strip()
        sections[key] = content

    # If no explicit contact section was found, try to extract contact info from the top
    if not sections['contact']:
        top_lines = lines[:10]
        sections['contact'] = '\n'.join(l.strip() for l in top_lines if l.strip())

    return sections
