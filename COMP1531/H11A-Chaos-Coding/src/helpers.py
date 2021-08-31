# Written by Kimberly Sufangga, z5257053
'''
helper functions used by many slackr functions
'''
# import functions
from database import get_data
from error import InputError, AccessError

# Links to the main database
DATA = get_data()

MAX_LENGTH_MESSAGE = 1000

# helper functions
# given a user's token, this function returns the u_id of that user
def token_to_user(token):
    for user in DATA["users"]:
        if user["token"] == token:
            return user["u_id"]
    raise AccessError("Token passed in is not a valid token")

# check if the user is valid, raise InputError if they are not
def is_valid(token, user_id):
    if (token is not None) and (user_id <= DATA["n_users"]):
        return
    else:
        raise InputError(description="User is not valid")

# check if the channel exists, raise InputError if the channel_id doesn't belong to any channel
def is_channel(channel_id):
    if int(channel_id) <= DATA["n_channels"]:
        return
    else:
        raise InputError(description="Channel id is not valid")

# check if the user is in the channel (by checking if the channel_id is in the user's list of channel ids)
def in_channel(user_id, channel_id):
    flag = False
    for user in DATA["users"]:
        if user["u_id"] == user_id:         # find the user in our database of users
            for item in user["channels"]:
                if item["channel_id"] == int(channel_id):      # check if the given channel_id is in their list of channels
                    flag = True
    if flag == False:
        raise AccessError(description="Authorised user is not a member of channel with channel_id")
    else:
        return

# Check the length of the message and raises an error if the message is greater than 1000 characters.
def message_length(message):
    if len(message) > MAX_LENGTH_MESSAGE:
        raise InputError(description="Message must be less than or equal to 1000 characters")

# Generates ID by checking the last ID stored in the data field.
'''
def id_generator(data):
    data_list = DATA[f"{data}"]                # Gets the list of the data that is implemented from server.
    last_data_id = data_list[-1][f"{data}"]    # Gets the last id stored from that data list.

    if last_data_id is None:        # If data_id is implemented for the first time, it will set to start from 1.
        last_data_id = 1
    else:                           # Otherwise just adds one to the last counter.
        last_data_id += 1

    return last_data_id
    '''
'''
Alternative option to validate a channel, however not considered because it is not efficcient:

def channel_valid(channel_id):
    flag = False
    for channel in GLOBAL_DATA["channels"]:
        if channel["channel_id"] == channel_id:
            flag = True

    if flag == False:
        raise InputError("Channel ID is not a valid channel")
'''
