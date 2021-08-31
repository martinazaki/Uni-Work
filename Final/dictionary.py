'''
Dictionary question
'''

import pytest

def construct_dict(keys, values):
    '''
    Takes in two lists of equal length and returns a dictionary composed of keys
    from the first list and values from the second.

    For example:
    >>> l1 = ['a', 'b', 'c']
    >>> l2 = [1, 2, 3]
    >>> construct_dict(l1, l2))
    {'a': 1, 'b': 2, 'c': 3}

    If a key appears more than once in the first list, the LATEST value from the
    second list is used.

    For example,
    >>> construct_dict(['a', 'b', 'b'], [1, 2, 3])
    {'a': 1, 'b': 3}

    Params:
      keys (list): A list of hashable keys.

      values (list): A list of values

    Raises:
      ValueError: if the lists are not the same length
    '''

    if not len(keys) == len(values):
        raise ValueError

    return dict(zip(keys, values))  

def test_simple():
    '''
    Test from documentation
    '''
    assert construct_dict(['a', 'b', 'c'], [1, 2, 3]) == {'a': 1, 'b': 2, 'c':3}

def test_duplicate():
    '''
    Second test from documentation
    '''
    assert construct_dict(['a', 'b', 'b'], [1, 2, 3]) == {'a': 1, 'b': 3}

def test_unequal():
    '''
    Lists of unequal length should always give an error.
    '''
    with pytest.raises(ValueError):
        construct_dict(['a', 'b', 'c'], [1, 2, 3, 4])