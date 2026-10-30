from src.preprocessing.text_cleaner import clean_text
from src.preprocessing.tokenizer import tokenize

def test_clean_text_lowercases_and_normalizes_spaces():
    assert clean_text("  HELLO   World ") == "hello World".lower()

def test_tokenize_words():
    assert tokenize("Hello, WORLD!") == ["hello", "world"]
