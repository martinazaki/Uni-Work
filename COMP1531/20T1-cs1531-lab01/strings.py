'''
TODO Complete this file by following the instructions in the lab exercise.
'''

strings = ['This', 'list', 'is', 'now', 'all', 'together']

new_string = ""
for string in strings:
    new_string = new_string + string + " "
    
print(new_string[:-1])   
print(' '.join(strings))
