'''
Cycle finding exercise
'''

def longest_distance(elements):
    '''
    Find the length of the longest distance between two equal elements in the
    given list.
    For example:
    >>> longest_distance([1,2,3,1,4])
    3

    Params:
      input (list): A list of hashable elements.

    Returns:
      int: The length of the longest distance. Note, this could be zero.
    '''

    mapping = {} 

    maxDict = 0
    for i in range(len(elements)): 
        if elements[i] not in mapping.keys():
            mapping[elements[i]] = 1

        else: 
            maxDict = max(maxDict, i - mapping[elements[i]]) 
  
    return maxDict 

def test_documentation():
    '''
    Test from documentation
    '''
    assert longest_distance([1,2,3,1,4]) == 3

def test_starts_later():
    '''
    The longest distance doesn't include the first element in the list
    '''
    assert longest_distance([1,2,3,4,2,5]) == 3

def test_two_non_zero_distances():
    '''
    The distance between 2 and 2 is longest so its length is returned
    '''
    assert longest_distance([1,2,1,3,4,2]) == 4

def test_unique():
    '''
    All elements are unique, so the only distances are between the elements and
    themselves
    '''
    assert longest_distance([1,2,3,4]) == 0