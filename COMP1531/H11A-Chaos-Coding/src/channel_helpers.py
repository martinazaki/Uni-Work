# Written by Kimberly Sufangga, z5257053
'''
helper functions for channel.py
'''
# Import functions
from database import get_data
from error import InputError, AccessError

# Links to the main database
DATA = get_data()

# helper functions
# check if the user is already in the channel (for purposes of invite and join)
def already_in_channel(user_id, channel_id):
    for user in DATA["users"]:
        if user["u_id"] == user_id:         # find the user in our database of users
            for channel in user["channels"]:
                if channel["channel_id"] == channel_id:      # check if the given channel_id is in their list of channels
                    raise InputError(description="User cannot join the channel because they are already in the channel")
                else:
                    return

# Check that the owner is a slackr owner or an owner of that channel
def is_owner(channel_id, user_id):
    # Get the global permission from the user
    global_permissions = 2
    for user in DATA["users"]:      # loop through users 
        if user["u_id"] == user_id:
            global_permissions = user["global_permissions"]

    # Checks if the user is an owner of the channel
    if global_permissions != 1:                            # If user is not a slackr woner
        for channel in DATA["channels"]:
            if channel["channel_id"] == channel_id:
                for member in channel["members"]:          # loop through members list
                    if member["channel_permissions"] == 1: # checks that user is an owner
                        break
                    else:
                        raise AccessError(description="User not an owner of this channel") 
    elif global_permissions == 1:                          # User is slackr owner
        return
    