from src.utils.validators import validate_message

def test_empty_message_rejected():
    assert validate_message("")[0] is False

def test_valid_message_accepted():
    assert validate_message("Hello there")[0] is True
