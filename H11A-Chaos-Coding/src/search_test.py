# Written by Martina Zaki, z5264835
# Written by Kimberly Sufangga, z5257053
'''
Tests for search function
'''
# Import functions
import time
import pytest
from auth import auth_register
from channels import channels_create
from workspace_admin import workspace_reset
from message import message_send
from search import search
from database import get_data

# Links to the main database
DATA = get_data()

# Search Tests
def test_search():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    channel_private = channels_create(user_1["token"], "Private Channel", False)
    message_1 = message_send(user_1["token"], channel_public["channel_id"], "a message")
    message_2 = message_send(user_1["token"], channel_private["channel_id"], "a private channel message")
    time_1 = 0
    time_2 = 0
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for message in channel["messages"]:
                if message["message_id"] == message_1["message_id"]:
                    time_1 = message["time_created"]

    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_private["channel_id"]:
            for message in channel["messages"]:
                if message["message_id"] == message_2["message_id"]:
                    time_2 = message["time_created"]

    # End of setup

    assert search(user_1["token"], "message") == {"messages": [
        {
            "message_id": message_1["message_id"],
            "u_id": 1,
            "message": "a message",
            "time_created": time_1,
            "reacts" : [],
            "is_pinned" : False
        },
        {
            "message_id": message_2["message_id"],
            "u_id": 1,
            "message": "a private channel message",
            "time_created": time_2,
            "reacts" : [],
            "is_pinned" : False
        }]
                                                }
