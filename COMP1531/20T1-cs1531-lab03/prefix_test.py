from prefix import prefix_search
import pytest

def test_documentation():
    assert prefix_search({"ac": 1, "ba": 2, "ab": 3}, "a") == { "ac": 1, "ab": 3}

def test_exact_match():
    assert prefix_search({"category": "math", "cat": "animal"}, "cat") == {"category": "math", "cat": "animal"}

def test_empty():
    assert prefix_search({"abc": 3, "def": 4}, "") == {"abc": 3, "def": 4}