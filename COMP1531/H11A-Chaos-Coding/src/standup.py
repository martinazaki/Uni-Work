"""
Written by Maria Cuyutupa Garcia z5223865 in March 2020.
This file contains standup_start, standup_active and standup_send functions.
"""

#pylint: disable=pointless-string-statement

# Python Libraries
from time import sleep

# Project files
import standup_helper as helper
from database import get_data
from helpers import message_length
from error import InputError

# This variable links to the database.
DATA = get_data()

"""
 Set the stand-up active for 'length' seconds. Once the stand-up finishes, packs all the
 messages sent during the stand-up into a single message and delivers it to the channel
 which the stand-up was held.
"""
def standup_start(token, channel_id, length):
    """Returns standup time finish.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.
    length (int): Length of standup in seconds.

    Returns:
    time_finish (int): Time of finsihed standup.
    """

    # Validates the channel and the user by checking the token and the user id.
    helper.user_channel_validation(token, channel_id)
    # Verify if the channel is already active
    helper.is_active(channel_id)
    # Sets the finish time of the stand-up.
    time_finish = helper.get_time_finish(length)

    packed_message = ""
    # Loop through the channels and sets the standup in mode 'on'.
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            channel["standup"]["is_active"] = True           # Setting stand-up in mode on
            channel["standup"]["time_finish"] = time_finish  # Changing the value of time_finished
            sleep(length)           # Pauses the program while the standup last
            # Packs the messages into a single message
            packed_message = "\n".join(channel["standup"]["messages"])
            channel["standup"] = {  # Resets the data
                "is_active" : False,
                "time_finish" : None,
                "messages" : []
            }

    # Sends the packed message to the channel
    helper.message_send(token, channel_id, packed_message, time_finish)

    return {
        "time_finish" : time_finish
    }

"""
 For a given channel, return whether a standup is active in it, and what 
 time the standup finishes. 
"""
def standup_active(token, channel_id):
    """Returns standup time finish and active status.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.

    Returns:
    is_active (string): Indicated whether standup is active or not.
    time_finish (int): Time of finsihed standup.
    """

    # Validates the channel and the user by checking the token and the user id.
    helper.user_channel_validation(token, channel_id)

    time_finish = None
    is_active = True
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:           # Finds channel
            if channel["standup"]["time_finish"] != None: #pylint: disable=singleton-comparison
                # Changes the value of the time_finish
                time_finish = channel["standup_active"]["time_finish"]
            else:
                is_active = False
    return {
        "is_active" : is_active,
        "time_finish" : time_finish,
    }

"""
 Sending a message to get buffered in the standup queue 
"""
def standup_send(token, channel_id, message):
    """Sends message to get buffered.

    Params:
    token (string): An authorisation hash.
    channel_id (int): ID of channel used to start standup.
    message (string): Messenge sent to get buffered in standup queue.

    Returns:
    none (empty dictionary)
    """

    # Validates the channel and the user by checking the token and the user id.
    helper.user_channel_validation(token, channel_id)
    # Check if the user is a member of channel
    helper.is_member(token, channel_id)
    # Verify if the message is more than 1000 characters.
    message_length(message)

    ## Buffers the message to standup["messages"] list while the standup is active. ##
    first_name = ""
    # Loop trough list of users and find the first name based on their token.
    for user in DATA["users"]:
        if user["token"] == token:
            first_name = user["name_first"]

    # Loop through channels
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            # Check if that channel is currently holding a standup.
            if channel["standup"]["is_active"] == True:     #pylint: disable=singleton-comparison
                # Append the message to the message's list as a string.
                channel["standup"]["messages"].append(f"{first_name}: {message}")
            else:
                raise InputError(description="An active standup is not currently running in this channel") #pylint: disable=line-too-long

    return {}
