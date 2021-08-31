from flask import Flask, request
from json import dumps

app = Flask(__name__)
    
names = []

def getNames():
    global names
    return names

@app.route('/names', methods=['GET'])
def get():
    data = getNames()
    return dumps({
        'names' : data,
    })

@app.route('/name/add', methods=['POST'])
def post():
    data = getNames()
    data.append(request.form.get('name'))
    return dumps({})

@app.route('/name/remove', methods=['DELETE'])
def delete():
    data = getNames()
    data.remove(request.form.get('name'))
    return dumps({})

if __name__ == '__main__':
    app.run()
