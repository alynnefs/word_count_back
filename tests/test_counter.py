from app.counter import count_words


def test_empty_string():
    assert count_words("") == 0


def test_only_spaces():
    assert count_words("   ") == 0


def test_only_newlines():
    assert count_words("\n\n") == 0


def test_multiple_spaces_between_words():
    assert count_words("hello   world") == 2


def test_leading_and_trailing_spaces():
    assert count_words("  hello world  ") == 2


def test_newline_between_words():
    assert count_words("hello\nworld") == 2


def test_tab_between_words():
    assert count_words("hello\tworld") == 2


def test_accented_words():
    assert count_words("café coração ação") == 3


def test_duplicates_counted_once():
    assert count_words("hello hello hello") == 1


def test_at_size_limit():
    text = "a " * 50000  # 100000 chars, 50000 palavras únicas não — só "a"
    assert count_words(text) == 1
