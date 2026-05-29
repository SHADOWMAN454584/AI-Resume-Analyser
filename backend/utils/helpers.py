"""
Utility helper functions.
"""
import os
import re
import uuid
from datetime import datetime


ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """
    Check if a filename has an allowed extension.

    Args:
        filename: Original filename string.

    Returns:
        True if the file extension is in ALLOWED_EXTENSIONS.
    """
    if not filename or '.' not in filename:
        return False
    ext = filename.rsplit('.', 1)[1].lower()
    return ext in ALLOWED_EXTENSIONS


def generate_unique_filename(filename):
    """
    Generate a unique filename preserving the original extension.

    Args:
        filename: Original filename string.

    Returns:
        Unique filename string (UUID-based with timestamp prefix).
    """
    if not filename or '.' not in filename:
        ext = 'pdf'
    else:
        ext = filename.rsplit('.', 1)[1].lower()

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    unique_id = uuid.uuid4().hex[:8]
    return f"{timestamp}_{unique_id}.{ext}"


def sanitize_text(text):
    """
    Sanitize text by removing potentially harmful content.

    Args:
        text: Input text string.

    Returns:
        Sanitized text string.
    """
    if not text:
        return ''

    # Remove null bytes
    text = text.replace('\x00', '')

    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)

    # Remove script-like content
    text = re.sub(r'(?i)<script[^>]*>.*?</script>', '', text, flags=re.DOTALL)

    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()
