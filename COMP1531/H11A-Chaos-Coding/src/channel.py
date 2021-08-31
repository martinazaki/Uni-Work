# Written by Kimberly Sufangga, z5257053
'''
channel functions including join, leave, invite, details, messages, addowner, and removeowner
'''
# import functions
import copy
from database import get_data
from helpers import is_valid, is_channel, token_to_user, in_channel
from channel_helpers import already_in_channel, is_owner
from error import InputError, AccessError

#pylint: disable=trailing-whitespace
#pylint: disable=missing-function-docstring 
#pylint: disable=no-else-raise

# Links to the main database
DATA = get_data()

# a user with token invites user with u_id into channel with channel_id, the user with u_id joins the channel
# user_id is person doing the inviting, u_id is the person being invited
def channel_invite(token, channel_id, u_id):
    is_channel(channel_id)  # check if the channel_id is valid
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check if the user (person doing the inviting) is valid
    in_channel(user_id, channel_id)     # check if the user (person doing the inviting) is in the channel
    already_in_channel(u_id, channel_id) # check if the user being invited to the channel is already in the channel

    # check if u_id of person being invited refers to a valid user
    if u_id > DATA["n_users"]:
        raise InputError(description="u_id does not refer to a valid user")


    for channel in DATA["channels"]:    # loop through channels
        if channel["channel_id"] == channel_id:
            for user in DATA["users"]:
                if user["u_id"] == u_id:       # find the user being invited
                    if user["global_permissions"] == 1: # if they are a global owner make them channel owner as well
                        channel["members"].append({"u_id": u_id, "channel_permissions": 1})     # add user to the channel's list of members
                        user["channels"].append({"channel_id":channel_id, "name":channel["name"]})     # add id and channel name to user's list of channels
                    else:   # they join as a member
                        channel["members"].append({"u_id": u_id, "channel_permissions": 2})
                        user["channels"].append({"channel_id":channel_id, "name":channel["name"]})
    return {}

# return some details of the channel, including name of channel, owners of channel, and all members of channel
def channel_details(token, channel_id):
    is_channel(channel_id)  # check if the channel_id is valid
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check if the user is valid
    in_channel(user_id, channel_id)     # check if the user is in the channel

    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            name = channel["name"]
            all_members = copy.deepcopy(channel["members"])     # create a copy to return, because assignment in python is a pointer and we are removing keys
            owner_members = []
            # members returns u_id, name_first and name_last
            for member in all_members:  # loop through all the members in the channel
                for user in DATA["users"]:
                    if user["u_id"] == member["u_id"]:      # find them in our database of users by matching their u_id
                        member.update({"name_first": user["name_first"], "name_last": user["name_last"]})     # update each entry with the required keys

            for item in all_members:
                if item["channel_permissions"] == 1:   # check if the user is an owner of the channel
                    del item["channel_permissions"]    # remove the key channel_permissions as we don't need to return it
                    owner_members.append(item)         # add the correct keys to owner_members
                else:
                    del item["channel_permissions"]
            return {"name": name, "owner_members": owner_members, "all_members": all_members}

# return up to 50 messages from a channel
def channel_messages(token, channel_id, start):

    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user is valid
    is_channel(channel_id)      # check that channel exists
    end = start + 50            # list slicing uses end - 1 to return the correct number of messages (50 messages)
    least_recent = False

    in_channel(user_id, channel_id)     # check if the user is in the channel

    for channel in DATA["channels"]:       # find the channel that the given channel_id refers to
        if channel["channel_id"] == channel_id:
            if start > len(channel["messages"]):
                raise InputError(description="Start is greater than the total number of messages in the channel")
            elif start == len(channel["messages"]):     ## if there are 0 messages or start = the last message
                result = channel["messages"]
                return {"messages": result, "start": start, "end": -1}
            else:
                result = channel["messages"][start:end]     # slice the list to get 50 messages from start to end (start and end are the list indexes here)
                times = [time["time_created"] for time in result]   # make a list of the times of each message
                for item in result:
                    if item["time_created"] == min(times):            # the smallest time integer (unix timestamp) is the oldest msg in that channel
                        least_recent = True

                if least_recent:
                    return {"messages": result, "start": start, "end": -1}      # if the least recent message was returned, return -1
                else:
                    return {"messages": result, "start": start, "end": (start + 49)}    # else just return start + 49


# leave a channel
def channel_leave(token, channel_id):
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user is valid
    is_channel(channel_id)      # check that channel exists

    in_channel(user_id, channel_id)     # check if the user is in the channel

    for channel in DATA["channels"]:    # iterate through list of channels
        if channel["channel_id"] == channel_id:
            for i in range(len(channel["members"])):    # iterate through list of members in this channel
                if channel["members"][i]["u_id"] == user_id:
                    del channel["members"][i]             # remove user from the list of members in this channel

    for user in DATA["users"]:      # iterate through list of users
        if user["u_id"] == user_id:
            for item in user["channels"]:      # iterate through the user's list of channels
                if item["channel_id"] == channel_id:     # find the matching channel in their list of channels
                    user["channels"].remove(item)     # remove channel dictionary from user's list of channels
    return {}

# join a channel
def channel_join(token, channel_id):
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user is valid
    is_channel(channel_id)      # check that channel exists
    already_in_channel(user_id, channel_id) # check if the user trying to join the channel is already in the channel

    for channel in DATA["channels"]:    # loop through channels
        if channel["channel_id"] == channel_id:
            if channel["is_public"] == False:       # if the channel is private
                for user in DATA["users"]:  # loop through users
                    if user["u_id"] == user_id:
                        if user["global_permissions"] == 2:  # if the user is not an owner/admin
                            raise AccessError(description="Only Owners can join a private channel. User is not an owner")  # they cannot join a private channel
                        else:                               # else, if the user is an owner/admin, they can join
                            channel["members"].append({"u_id": user_id, "channel_permissions": 1})
                            user["channels"].append({"channel_id": channel_id, "name": channel["name"]})     # add id and channel name to user's list of channels
            else:                                   # else, if the channel is public
                for user in DATA["users"]:  # loop through users
                    if user["u_id"] == user_id:
                        if user["global_permissions"] == 1: # if they are a global owner, they join as a channel owner
                            channel["members"].append({"u_id": user_id, "channel_permissions": 1})
                            user["channels"].append({"channel_id": channel_id, "name": channel["name"]})
                        else:
                            channel["members"].append({"u_id": user_id, "channel_permissions": 2})  # else they join as a member
                            user["channels"].append({"channel_id": channel_id, "name": channel["name"]})
    return {}
    
def channel_addowner(token, channel_id, u_id):
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user is valid
    is_channel(channel_id)      # check that channel exists
    is_owner(channel_id, user_id)  # check that the user is an owner 

    flag = 0
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_id:
            for member in channel["members"]:   # loop through members list
                if member["u_id"] == u_id:      # finds the user in the list
                    flag = 1
                    # user is already an owner of the channel
                    if member["channel_permissions"] == 1: 
                        raise InputError(description="User is already an owner of the channel")
                    # changes the permission of the user
                    else:
                        member["channel_permissions"] = 1 
    
    if flag == 0:
        raise AccessError(description="User is not a member of the channel")
          
    return {}

def channel_removeowner(token, channel_id, u_id):
    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user is valid
    is_channel(channel_id)      # check that channel exists
    is_owner(channel_id, user_id) # check that the user is an owner 

    flag = 0
    for channel in DATA["channels"]:   # loop through channels list
        if channel["channel_id"] == channel_id:
            for member in channel["members"]:   # loop through members list
                if member["u_id"] == u_id:      # find the user
                    flag = 1
                    if member["channel_permissions"] == 1: 
                        # changes the value if the owner is removed  
                        member["channel_permissions"] = 2 
                    # otherwise raises an error   
                    else:                                   
                        raise InputError(description="User is not an owner of the channel")
    if flag == 0:
        raise InputError(description="User is not a member of the channel")
    
    return {}
