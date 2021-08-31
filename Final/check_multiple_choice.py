'''
Check the sanity of multiple choice answers
'''

if __name__ == "__main__":
    valid = dict([(n, {'A','B','C','D'})     for n in [1,3,7,8,9,10,11,13,14,15]] +
                 [(n, {'A','B','C','D','E'}) for n in [2,5,6,12]] +
                 [(n, {'A','B','C'})         for n in [4]])
    problem = False
    with open('multiple_choice.txt', 'r') as f:
        for l in f:
            if not l.strip():
                continue
            try:
                [q, a] = map(str.strip, l.split('.'))
                q = int(q)
                if q not in valid:
                    problem = True
                    print(f"You have a question {q} in your multiple_choice.txt, but no such question exists.")
                elif not a:
                    problem = True
                    print(f"You have not answered question {q}.")
                elif a not in valid[q]:
                    problem = True
                    print(f"You have given an answer of {a} to question {q}, but that's not one of the options.")
            except ValueError:
                print(f"This line does not appear to be in the right format: {l.strip()}")
    if problem:
        print("--------------------------------------------------------------------------------------------")
        print("It looks like there are problems with your answers. Please fix issues above.")
        exit(1)
    else:
        print("You have a complete set of answers. No problems identified.")