import re

def tokenize(text: str) -> list[str]:
    """Simple regex tokenizer, no external corpus download required."""
    return re.findall(r"[a-zA-Z]+(?:'[a-zA-Z]+)?|₹?\d+(?:[.,]\d+)*|https?://\S+|www\.\S+", text.lower())
