from app.main import count_the_words


def test_without_words():
    response = count_the_words("")
    assert "0" == response


def test_only_with_space():
    response = count_the_words(" ")
    assert "0" == response


def test_one_word():
    response = count_the_words("apple")
    assert "1" == response


def test_two_words():
    response = count_the_words("an apple")
    assert "2" == response


def test_duplicate_word():
    response = count_the_words("hello word word")
    assert "2" == response


def test_space_start_and_end():
    response = count_the_words(" an apple ")
    assert "2" == response


def test_multiple_spaces_between_words():
    response = count_the_words("an    apple")
    assert "2" == response


def test_many_words():
    response = count_the_words(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed "
        + "do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut "
        + "enim ad minim veniam, quis nostrud exercitation ullamco "
        + "laboris nisi ut aliquip ex ea commodo consequat. Duis aute "
        + "irure dolor in reprehenderit in voluptate velit esse cillum "
        + "dolore eu fugiat nulla pariatur."
    )

    assert "48" == response
