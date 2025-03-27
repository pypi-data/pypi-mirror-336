import re

def clean_text(text):
    """Remove special characters and extra spaces."""
    return text.strip().lower()

def remove_numbers(text):
    """Remove all numbers from the text."""
    return re.sub(r'\d+', '', text)

def remove_extra_spaces(text):
    """Remove multiple spaces and replace with a single space."""
    return re.sub(r'\s+', ' ', text).strip()
