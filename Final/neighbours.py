'''
Generalised neighbours
'''

def neighbours(n, iterable):
    '''
    A generator, that, given an iterable, yields the "neighbourhood" of each
    element. The neighbourhood is a tuple containing the element itself as well
    as up to n elements before and up to n elements after. For example,
    >>> list(neighbours(2, [1,2,3,4,5,6]))
    [(1,2,3), (1,2,3,4), (1,2,3,4,5), (2,3,4,5,6), (3,4,5,6), (4,5,6)]

    Note that toward the start and end of the input there are fewer components
    in each tuple.

    Params:
      iterable (iterable): The iterable being processed. In the event it's empty,
      this generator should not yield anything.

    Yields:
      (tuple) : The neighbourhood of the current element.

    Raises:
      ValueError : if n < 0
    '''
    pass

def test_documentation():
    '''
    A simple test from the documentation
    '''
    assert list(neighbours(2, [1,2,3,4,5,6])) == [(1,2,3), (1,2,3,4), (1,2,3,4,5), (2,3,4,5,6), (3,4,5,6), (4,5,6)]