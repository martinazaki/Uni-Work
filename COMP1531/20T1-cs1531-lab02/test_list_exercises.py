from list_exercises import *

def test_reverse():
    l = ["how", "are", "you"]
    reverse_list(l)
    assert l == ["you", "are", "how"]

    l = [1, 2, 3]
    reverse_list(l)
    assert l == [3, 2, 1]

    #l = ["-3", "-2", "-1", "0", "1", "2", "3"]
    #reverse_list(l)
    #assert l == ["3", "2", "1", "0", "-1", "-2", "-3"]

    #l = ["0"]
    #reverse_list(l)
    #assert l == ["0"]


def test_min():
    assert minimum([1, 2, 3, -10]) == -10
    assert minimum([0]) == 0
    assert minimum([1, 2, 3, 4, 5]) == 1
    assert minimum([-3, -2, -1, 0, 1, 2, 3]) == -3

def test_sum():
    assert sum_list([7, 7, 7]) == 21
    assert sum_list([-3, -2, -1, 0, 1, 2, 3]) == 0
    assert sum_list([1, 2, 3, 4, 5]) == 15
    assert sum_list([1, 3, 5, 7, 9]) == 25
