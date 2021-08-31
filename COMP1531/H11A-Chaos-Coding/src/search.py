# Written by Kimberly Sufangga, z5257053
'''
Search function
'''
# Import functions
import operator
from database import get_data
from helpers import is_valid, token_to_user

# Links to the main database
DATA = get_data()

# Searches all the user's channels for messages that match the query string
def search(token, query_str):
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check if the user is valid
    result = []

    for user in DATA["users"]:     # find the user doing the search
        if user["u_id"] == user_id:
            for i in user["channels"]:    # for each channel dictionary in the user's list of channels
                for channel in DATA["channels"]:   # loop through the database's list of channels
                    if i["channel_id"] == channel["channel_id"]:    # find the channel in the database which has this channel_id
                        for message in channel["messages"]:     # loop through each message in the list of messages
                            if query_str in message["message"]:     # if the message matches our search
                                result.append(message) # add each message's dictionary entry to our result list

    result.sort(key=operator.itemgetter("time_created"))    # sort our list of results by time created
    return {"messages": result} # return dictionary with list of dictionaries
