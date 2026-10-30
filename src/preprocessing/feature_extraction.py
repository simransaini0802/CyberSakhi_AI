"""Feature extraction utilities will be added with the trained model phase."""

def word_count(text: str) -> int:
    return len((text or "").split())
