def validate_message(message: str) -> tuple[bool, str]:
    if not message or not message.strip():
        return False, "Message cannot be empty."
    if len(message) > 10000:
        return False, "Message must be 10,000 characters or fewer."
    return True, ""
