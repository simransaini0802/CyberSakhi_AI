from src.detection.message_detector import PATTERNS
import re

def find_suspicious_phrases(text: str) -> list[dict]:
    findings = []
    for category, patterns in PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text or "", flags=re.I):
                findings.append({"category": category, "pattern": pattern})
    return findings
