'''
A flask server for the backend of the 'helpr' application.

GET routes are passed arguments as URL parameters. POST and DELETE routes are
passed arguments as JSON data in the body of the request. All routes return data
as JSON.
'''

from flask import Flask, request

from werkzeug.exceptions import BadRequest

from json import dumps

import config
import helpr

APP = Flask(__name__)

zid = ''
description = ''

@APP.route('/make_request', methods=['POST'])
def make_request():
    '''
    A route for helpr.make_request()

    Params: {"zid", "description"}

    Raises: BadRequest if helpr.make_request() raises a KeyError or ValueError.

    Returns: {}
    '''
    global zid, description
    try:
        payload = request.get_json()
        zid = payload['zid']
        description = payload['description']

    except (ValueError or KeyError):
        raise BadRequest

    return {}

@APP.route('/queue', methods=['GET'])
def queue():
    '''
    A route for helpr.queue()

    Returns: A list in the same format as helpr.queue()
    '''
    global zid, description
    
    payload = request.get_json()
    zid = payload['zid']
    description = payload['description']

    return dumps({
        'zid': payload['zid'],
        'description': payload['description'],
        'status': payload['status'],
    })


@APP.route('/remaining', methods=['GET'])
def remaining():
    '''
    A route for helpr.remaining()

    Params: ("zid")

    Raises: BadRequest if helpr.remaining() raises a KeyError.

    Returns: { 'remaining': n } where n is an integer
    '''
    global zid
    
    try:
        payload = request.get_json()
        zid = payload['zid']

    except (KeyError):
        raise BadRequest

    return dumps({
        'remaining': helpr.remaining['count'],
    })

@APP.route('/help', methods=['POST'])
def help():
    '''
    A route for helpr.help()

    Params: {"zid"}

    Raises: BadRequest if helpr.help() raises a KeyError.

    Returns: {}
    '''
    global zid
    
    try:
        payload = request.get_json()
        zid = payload['zid']
    
    except (KeyError):
        raise BadRequest

    return {}

@APP.route('/resolve', methods=['DELETE'])
def resolve():
    '''
    A route for helpr.resolve()

    Params: {"zid"}

    Raises: BadRequest if helpr.resolve() raises a KeyError.

    Returns: {}
    '''
    global zid
    
    try: 
        payload = request.get_json()
        zid = payload['zid']

    except (KeyError):
        raise BadRequest

    return {}

@APP.route('/cancel', methods=['DELETE'])
def cancel():
    '''
    A route for helpr.cancel()

    Params: {"zid"}

    Raises: BadRequest if helpr.cancel() raises a KeyError.

    Returns: {}
    '''
    global zid
    
    try:
        payload = request.get_json()
        zid = payload['zid']

    except (KeyError):
        raise BadRequest
        
    return {}

@APP.route('/revert', methods=['POST'])
def revert():
    '''
    A route for helpr.revert()

    Params: {"zid"}

    Raises: BadRequest if helpr.revert() raises a KeyError.

    Returns: {}
    '''
    global zid
    
    try:
        payload = request.get_json()
        zid = payload['zid']

    except (KeyError):
        raise BadRequest

    return {}

@APP.route('/reprioritise', methods=['POST'])
def reprioritise():
    '''
    A route for helpr.reprioritise()

    Returns: {}
    '''
    return {}

@APP.route('/end', methods=['DELETE'])
def end():
    '''
    A route for helpr.end()

    Returns: {}
    '''
    return {}

if __name__ == "__main__":
    # Do NOT change the port below. If you need to change the port number do so
    # by changing the value in config.py
    APP.run(port=config.PORT, debug=True)