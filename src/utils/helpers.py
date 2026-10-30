def truncate(text: str, length: int = 120) -> str:
    text = text or ""
    return text if len(text) <= length else text[:length - 1] + "…"
