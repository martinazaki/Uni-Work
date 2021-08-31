# Written by Kimberly Sufangga, z5257053

# Import functions
import sys
import json
from json import dumps
from flask import Flask, request
from database import get_data

DATA = get_data()

# Save function to make sure that data is saved even when the server is shut down
def save():
    with open("server_data.json",'w') as FILE:
        json.dump(DATA, FILE, indent = 4, sort_keys=False)
