import re

def clean_text(text: str) -> str:
    """Lightweight normalization; preserves words and URLs for analysis."""
    text = (text or "").lower()
    text = re.sub(r"\s+", " ", text).strip()
    return text
