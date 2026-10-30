"""Explainable, rule-based scam-message screening (not a trained ML model)."""
import re
from src.preprocessing.text_cleaner import clean_text

# Each category is scored once, even if several phrases from that category match.
# Scores are heuristic indicators, not calibrated probabilities.
CATEGORY_RULES = {
    "Urgency or pressure": {
        "weight": 20,
        "patterns": [
            r"\burgent\b", r"\bimmediately\b", r"\bact now\b", r"\bwithin\s+\d+\s*(?:minutes?|hours?|days?)\b",
            r"\blast warning\b", r"\b(?:account|card)\s+(?:will be\s+)?(?:blocked|suspended|closed|disabled)\b",
            r"\b(?:today|right away)\b",
        ],
    },
    "Banking or KYC warning": {
        "weight": 25,
        "patterns": [
            r"\bbank\s+account\b", r"\bkyc\b", r"\bverification\s+(?:has\s+)?expired\b",
            r"\baccount\s+(?:verification|details)\b", r"\baccount\s+suspension\b",
            r"\bpan\s+(?:card\s+)?verification\b", r"\bdebit\s+card\b", r"\bcredit\s+card\b",
        ],
    },
    "Sensitive information request": {
        "weight": 30,
        "patterns": [
            r"\b(?:share|send|provide|enter|submit|confirm|verify)\b.{0,70}\b(?:otp|password|pin|cvv|passcode|banking details|account details|card details)\b",
            r"\b(?:otp|password|pin|cvv|passcode|banking details|account details|card details)\b.{0,70}\b(?:share|send|provide|enter|submit|confirm|verify)\b",
            r"\benter\s+(?:your\s+)?(?:personal|bank|account|card)\s+(?:information|details)\b",
        ],
    },
    "Unexpected reward or prize": {
        "weight": 20,
        "patterns": [
            r"\byou have won\b", r"\bclaim your prize\b", r"\bcongratulations\b.{0,60}\b(?:won|winner|prize)\b",
            r"\bfree gift\b", r"\blottery\b", r"\bclaim your reward\b", r"\b(?:win|won|claim)\b.{0,50}₹\s*[\d,]+",
            r"₹\s*[\d,]+.{0,50}\b(?:reward|prize|claim|won|winner)\b",
        ],
    },
    "Payment or money pressure": {
        "weight": 20,
        "patterns": [
            r"\bpay\s+(?:(?:a|the)\s+)?(?:\₹\s*[\d,]+\s*)?(?:fee|now|immediately|charges?|registration fee|processing fee|redelivery charges?)\b", r"\btransfer\s+(?:money|funds)\b",
            r"\bprocessing fee\b", r"\brefund pending\b", r"\bsend\s+(?:money|payment)\b",
            r"\bpayment\s+(?:required|pending|failed)\b",
            r"\bpay\b.{0,50}\b(?:registration fee|refundable fee|processing fee|redelivery charges?)\b",
        ],
    },
    "Job or employment offer": {
        "weight": 20,
        "patterns": [
            r"\bwork[- ]from[- ]home\\b", r"\bjob offer\\b", r"\bselected for (?:a|the) job\\b",
            r"\bregistration fee\\b", r"\blimited vacancies\\b", r"\bconfirm your position\\b",
            r"\brefundable (?:registration )?fee\\b", r"\bsalary of\s*₹?\s*[\d,]+",
        ],
    },
    "Delivery or parcel issue": {
        "weight": 15,
        "patterns": [
            r"\bparcel delivery has failed\\b", r"\bfailed delivery\\b", r"\bincomplete address\\b",
            r"\bupdate your delivery details\\b", r"\bredelivery charges?\\b", r"\bdelivery fee\\b",
        ],
    },
}

URL_RE = re.compile(r"(https?://[^\s<>\"']+|www\.[^\s<>\"']+)", re.I)
SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "cutt.ly", "rb.gy", "goo.gl", "ow.ly"}


def analyze_message(message: str) -> dict:
    original = message or ""
    text = clean_text(original)
    indicators = []
    score = 0

    for category, config in CATEGORY_RULES.items():
        matches = []
        for pattern in config["patterns"]:
            if re.search(pattern, text, flags=re.I):
                matches.append(pattern)
        if matches:
            score += config["weight"]
            indicators.append({
                "category": category,
                "details": f"Detected {len(matches)} matching warning pattern(s); heuristic contribution: +{config['weight']} points.",
            })

    urls = URL_RE.findall(original)
    url_warnings = []
    for url in urls:
        host = re.sub(r"^https?://", "", url, flags=re.I).split("/")[0].lower().rstrip(".,);]}")
        reasons = []
        if host in SHORTENERS:
            reasons.append("URL shortener hides the final destination")
        if "@" in host:
            reasons.append("contains an @ symbol in the host portion")
        if host.startswith("xn--") or ".xn--" in host:
            reasons.append("contains an internationalized/punycode domain label")
        if re.match(r"\d{1,3}(?:\.\d{1,3}){3}$", host):
            reasons.append("uses an IP address as the host")
        if not reasons:
            reasons.append("URL found; destination has not been verified")
        url_warnings.append({"url": url, "reasons": reasons})

    # Any URL adds a small caution; stronger URL red flags add extra points.
    if url_warnings:
        score += 10
        risky_url_count = sum(any(reason != "URL found; destination has not been verified" for reason in item["reasons"]) for item in url_warnings)
        score += min(10, risky_url_count * 5)
        indicators.append({
            "category": "Link present",
            "details": f"Found {len(url_warnings)} URL(s). A link is not automatically malicious, but its destination has not been verified; heuristic contribution: +{10 + min(10, risky_url_count * 5)} points.",
        })

    score = min(100, score)
    if score >= 60:
        risk, prediction = "High", "Potentially suspicious"
    elif score >= 30:
        risk, prediction = "Medium", "Review carefully"
    else:
        risk, prediction = "Low indicator count", "No strong indicators detected"

    if not indicators:
        recommendation = "No configured warning patterns were detected. This does not prove the message is safe."
    else:
        recommendation = "Do not click suspicious links or share OTPs, passwords, PINs or banking details. Verify independently using an official app or a website you type manually."

    return {
        "prediction": prediction,
        "risk": risk,
        "score": score,
        "indicators": indicators,
        "urls": url_warnings,
        "recommendation": recommendation,
        "method": "Transparent rule-based heuristic (not a trained ML probability)",
    }
