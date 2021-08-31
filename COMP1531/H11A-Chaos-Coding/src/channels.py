"""
 Written by Maria Cuyutupa Garcia z5223865 in March 2020.
 This file contains channels_list, channels_listall and channels_create functions.
"""

# Python Libraries
from copy import deepcopy

# Project files
from helpers import token_to_user
from database import get_data
import channels_helpers as helper

# This dictionary is appended to the database.
CHANNELS = {
    "channel_id" : 0,
    "name" : " ",
    "members" : [],
    "messages" : [],
    "is_public" : True,
    "standup" : {
        "is_active" : False,
        "time_finish" : None,
        "messages" : []
    }
}

# This dictionary is appended to CHANNELS
MEMBERS_CHANNEL = {
    "u_id" : 0,
    "channel_permissions" : 1,
}

# This variable links to the database.
DATA = get_data()

# Provide a list of all channels that the authorised user is part of.
def channels_list(token):
    """Lists all channels assoiated with user.

    Params:
    token (string): An authorisation hash.

    Returns:
    channels (dictionary): Dictionary of all channels with user.
    """

    helper.user_validation(token)  # Checks if the User is authorised

    channels_user = []
    # Loop through the channels from the User and collects channel_is and name.
    for user in DATA["users"]:
        if user["u_id"] == token_to_user(token):
            channels_user = user["channels"]

    return {
        "channels" : channels_user
    }

# Provide a list of all channels.
def channels_listall(token):
    """Lists all channels assoiated with user.

    Params:
    token (string): An authorisation hash.

    Returns:
    channels (dictionary): Dictionary of all channels.
    """

    helper.user_validation(token)  # Checks if the User is authorised

    channels_info = []
    # Loop through the channels and collects channel_is and name.
    for channel in DATA["channels"]:
        channels_info.append({
            "channel_id" : channel["channel_id"],       # Channel ID
            "name" : channel["name"],                   # Name of Channel
        })

    return {
        "channels" : channels_info      # Return list of channels.
    }

# Creates a new channel with that name that is either a public or private channel
def channels_create(token, name, is_public):
    """ Creates channel.

    Params:
    token (string): An authorisation hash.
    name (string): Name of channel.
    is_public (string): Public or private channel

    Returns:
    channel_id (int): ID of channel created.
    """

    helper.user_validation(token)  # Checks if the user is authorised
    helper.name_error(name)        # Checks if the name of the channel is more than 20 characteres.
    channel_id = helper.id_generator()  # Generates the Channel ID

    # Modify the number of channels
    n_channels = DATA["n_channels"]
    DATA["n_channels"] = n_channels + 1

    # Adds the name of the channel and channel ID to the database
    channels_data_copy = deepcopy(CHANNELS)
    channels_data_copy.update({"channel_id" : channel_id})
    channels_data_copy.update({"name" : name})              # Name of channel
    channels_data_copy.update({"is_public" : is_public})    # Permissions of channel

    # Adds the member of the channel
    members_data_copy = deepcopy(MEMBERS_CHANNEL)
    members_data_copy.update({             # User that created the channel is added in members.
        "u_id" : token_to_user(token),     # Adds the token to the database
        "channel_permissions" : 1,        # User is an owner of channel because they create it.
        })

    # The member is added to the list of members.
    channels_data_copy["members"].append(members_data_copy)
    # The channel created is added to the list of channels from the database
    DATA["channels"].append(channels_data_copy)
    # Appends the channel to the channel's list of the user
    for user in DATA["users"]:
        if user["token"] == token:
            user["channels"].append({
                "channel_id" : channel_id,
                "name" : name
            })

    return {
        "channel_id" : channel_id
    }
