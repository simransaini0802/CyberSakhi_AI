# Test cases

- Empty message is rejected.
- Typical prize/urgency phrases trigger a heuristic indicator.
- Plain neutral text does not trigger configured phrase patterns.
- Home and scanner routes return HTTP 200.
- URLs are extracted but never fetched or opened.
- Long input above 10,000 characters is rejected.
