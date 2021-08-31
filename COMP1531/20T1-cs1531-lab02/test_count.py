from count import count_char

def test_empty():
    assert count_char("") == {}

def test_simple():
    assert count_char("abc") == {"a": 1, "b": 1, "c": 1}

def test_double():
    assert count_char("aa") == {"a": 2}

def test_triple():
    assert count_char("bbb") == {"b": 3}

def test_bitdifficult():
    assert count_char("Hello eel") == {"H": 1, "e": 3, "l": 3, "o": 1}

def test_complex():
    assert count_char("I like uni") == {"I": 1, "l": 1, "i": 2, "k": 1, "e": 1, "u": 1, "n": 1}   