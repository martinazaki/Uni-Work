"""
 COMP1531 20T1 Chaos Coding                                             # Subject, term and team name.
 This file contains ...                                                 # Purpose of the file.
 Written by Maria Cuyutupa Garcia z5223865 in March 2020.               # Name, zID and date.
"""
# Avoid: from math import * unless it actually uses all the functions from that file
from flask import Flask            

# Use either app or APP 
app = Flask(__name__)

data = {
    'random' : [],
}

"""
 Always comment out what the function does and explain if necessary.
"""
def get_data():
    global data
    return data

app.route('/sample')
def silly_function():          
    # Meaningful names to variables and function name.
    # Use either snake_case or camelCase, but never both at the same time.
    return 'This is a sample code'

# For Iteration 2, this part will be important
if __name__ == '__main__':
    app.run()
