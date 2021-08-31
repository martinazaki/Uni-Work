# Written by Maria Cuyutupa Garcia z5223865 in March 2020.
"""
 This file contains helper functions for channels.
"""

from database import get_data
from helpers import is_valid, token_to_user
from error import InputError

# Parameter for the name of channel
MAX_NAME_LENGHT = 20

# This variable links to the database.
DATA = get_data()

"""
 This check if the name of the channel is more than 20 characters and
 raises and error if that is the case.
"""
def name_error(name):
    """Error raised when name length does not fit criteria.

    Params:
    name (string): Name of channel.

    Returns:
    none
    """

    if len(name) > MAX_NAME_LENGHT:
        raise InputError(description="Name cannot be more than 20 characters long")


# This validates the user by checking the token and the User ID.
def user_validation(token):
    """Validates the user.

    Params:
    token (string): An authorisation hash.

    Returns:
    none
    """
    u_id = token_to_user(token)     # Finds the u_id if the token is valid
    is_valid(token, u_id)           # Check if the user is valid

# Generates Channels' ID
def id_generator():
    """Generates user ID.

    Params:
    none

    Returns:
    none
    """

    channels_list = DATA["channels"]       # Gets the list of channels from server.

    if channels_list == []:                # If channel_id is implemented for the first time
        new_id = 1
    else:                                  # Otherwise just adds one to the last counter.
        last_id = channels_list[-1]["channel_id"]
        new_id = last_id + 1

    return new_id
