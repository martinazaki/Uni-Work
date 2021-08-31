import operator
from functools import reduce

def product(iterable):
    return reduce(operator.mul, iterable, 1)

if __name__ == '__main__':
    letters = ['a', 'b', 'c', 'd', 'e']
    inputs = []
    for i in range(len(letters)):
        inputs.append(int(input(f"Enter {letters[i]}: ")))

    print("Minimum: " + str(min(inputs)))
    print("Product of first 4 numbers: ")
    print(product(inputs[0:4]))
    print("Product of last 4 numbers: ")
    print(product(inputs[1:5]))
