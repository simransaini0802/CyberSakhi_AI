from src.detection.message_detector import analyze_message

def test_urgent_prize_message_has_indicators():
    result = analyze_message("Congratulations! You have won a prize. Claim your prize immediately.")
    assert result["indicators"]
    assert result["score"] > 0

def test_plain_message_has_no_phrase_indicators():
    result = analyze_message("Your appointment is scheduled for tomorrow at noon.")
    assert result["indicators"] == []
