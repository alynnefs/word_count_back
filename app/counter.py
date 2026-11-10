def count_words(text: str) -> int:
    text = text.strip()
    if not text:
        return 0
    tokens = text.split()
    return len(list(dict.fromkeys(filter(None, tokens))))
