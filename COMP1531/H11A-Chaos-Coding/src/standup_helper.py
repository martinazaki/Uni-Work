# Written by Maria Cuyutupa Garcia z5223865 in March 2020.
"""
 This file contains helper functions for standup
"""
#pylint: disable=pointless-string-statement

# Python Libraries
from datetime import datetime, timezone
from copy import deepcopy

# Project files
from database import get_data
from helpers import token_to_user, is_valid, is_channel
from error import AccessError, InputError
from message_helpers import message_id_generator

# These links to the database
DATA = get_data()

MESSAGE = {
    "message_id": "",
    "u_id": "",
    "message": "",
    "time_created": 1,
    "reacts" : [],
    "is_pinned" : False
    }

# This validates the user by checking the token and the user id.
def user_channel_validation(token, channel_id):
    """Validates user's channel.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.

    Returns:
    none
    """

    u_id = token_to_user(token)     # Finds the u_id if the token is valid
    is_valid(token, u_id)           # Check if the user is valid
    is_channel(channel_id)          # Check if the channel exists

# The authorised user is not a member of the channel that the message is within
def is_member(token, channel_id):
    """Checks if user is a memeber.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.

    Returns:
    none
    """

    u_id = token_to_user(token)
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:     # Finds for channel id
            for member in channel["members"]:       # Loop through members
                if u_id not in member["u_id"]:
                    # if u_id is not found in the member's list it raises an error
                    raise AccessError(description="User is not a member of the channel")

# Check if that channel is currently running a standup
def is_active(channel_id):
    """Checks if channel is active.

    Params:
    channel_id (int): ID of channel used to start standup.

    Returns:
    none
    """

    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:    # Finds the channel
            if channel["standup"]["is_active"]:    # Checks if is active
                raise InputError(description="An active standup is currently running in this channel")  #pylint: disable=line-too-long

# Generates the final time which the standup will finish.
def get_time_finish(length):
    """Final time when standup will finish.

    Params:
    length (int): Length of standup.

    Returns:
    none
    """

    return datetime.now().replace(tzinfo=timezone.utc).timestamp() + length

# Sends the message to the channel
def message_send(token, channel_id, packed_message, finish_time):
    """Sends message to channel.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.
    packed_message (string): Message in channel.
    finish_time (int): Time of finished standup.

    Returns:
    none
    """

    message_id = message_id_generator() # Generates the message_id
    message_copy = deepcopy(MESSAGE)

    # Updates the data
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            message_copy.update({"message_id" : message_id})
            message_copy.update({"u_id" : token_to_user(token)})
            message_copy.update({"message" : packed_message})
            message_copy.update({"time_created" : finish_time})

        channel["messages"].append(message_copy)  # Appends it to the database
        DATA["n_messages"] += 1 # Increments the number of messages on the database
