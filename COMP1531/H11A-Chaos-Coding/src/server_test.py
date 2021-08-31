import json
import requests
import urllib
from database import get_data

global_data = get_data()

BASE_URL = 'http://127.0.0.1:8080'

def test_system():

    r = requests.post(f"{BASE_URL}/message/send", json={
        'token': 'thisisatoken',
        'channel_id': 1,
        'message': 'Hello world!'
    })
    payload = r.json()

    assert payload['token'] == 'thisisatoken'
    assert payload['channel_id'] == 1
    assert payload['message'] == 'Hello world!'

