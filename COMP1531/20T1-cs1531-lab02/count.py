
def count_char(input):
    '''
    Counts the number of occurrences of each character in a string. The result should be a dictionary where the key is the character and the dictionary is its count.

    For example,
    >>> count_char("HelloOo!")
    {'H': 1, 'e': 1, 'l': 2, 'o': 2, 'O': 1, '!': 1}
    '''

    result = {}
    for m in input:
        result[m] = result.get(m,0) + 1
    return result

    pass