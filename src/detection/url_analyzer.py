"""URL analysis currently lives in message_detector.py; no URLs are fetched."""
from src.detection.message_detector import URL_RE

def extract_urls(text: str) -> list[str]:
    return URL_RE.findall(text or "")
