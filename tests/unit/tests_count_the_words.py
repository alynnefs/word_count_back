from app.counter import count_words


def test_without_words():
    assert count_words("") == 0


def test_only_with_space():
    assert count_words(" ") == 0


def test_one_word():
    assert count_words("apple") == 1


def test_two_words():
    assert count_words("an apple") == 2


def test_duplicate_word():
    assert count_words("hello word word") == 2


def test_space_start_and_end():
    assert count_words(" an apple ") == 2


def test_multiple_spaces_between_words():
    assert count_words("an    apple") == 2


def test_many_words():
    assert count_words(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        + "do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
        + "enim ad minim veniam, quis nostrud exercitation ullamco "
        + "laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
        + "irure dolor in reprehenderit in voluptate velit esse cillum "
        + "dolore eu fugiat nulla pariatur."
    ) == 48
