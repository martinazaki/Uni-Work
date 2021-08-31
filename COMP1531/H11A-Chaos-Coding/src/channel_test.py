# Written by Kimberly Sufangga, z5257053
'''
tests for channel functions
'''
# import functions
import pytest
from error import InputError, AccessError
from auth import auth_register
from channels import channels_create
from channel import channel_invite, channel_details, channel_messages, channel_leave, channel_join
from message import message_send
from workspace_admin import workspace_reset, admin_userpermissions_change
from database import get_data

# Links to the main database
DATA = get_data()

## channel_invite tests
# assume that auth_register, channels_create, and channel_join work
# channels create automatically adds the creator as a member of the channel
# channel_invite takes in the token of the user inviting, the channel name, and the u_id of the user being invited
def test_invite_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup
    flag_user_channels = False
    flag_channel_members = False

    # user 1 invites user 2 into public channel
    print (user_1["token"])
    print (channel_public["channel_id"])
    print (user_2["u_id"])
    channel_invite(user_1["token"], channel_public["channel_id"], user_2["u_id"])

    # check that the channel_id is now in user 2's list of channel ids
    for user in DATA["users"]:
        if user["u_id"] == user_2["u_id"]:
            for item in user["channels"]:
                if item["channel_id"] == channel_public["channel_id"]:
                    flag_user_channels = True

    # check that user 2 is now in the channel's list of members
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for member in channel["members"]:
                if member["u_id"] == user_2["u_id"]:
                    flag_channel_members = True
    # assert True
    assert flag_user_channels
    assert flag_channel_members

def test_invite_success_slackr_owner():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    admin_userpermissions_change(user_1["token"], user_2["u_id"], 1)    # change user_2 to a global owner
    # End of setup
    flag_user_channels = False
    flag_channel_members = False

    # user 1 invites user 2 into public channel
    channel_invite(user_1["token"], channel_public["channel_id"], user_2["u_id"])

    # check that the channel_id is now in user 2's list of channel ids
    for user in DATA["users"]:
        if user["u_id"] == user_2["u_id"]:
            for item in user["channels"]:
                if item["channel_id"] == channel_public["channel_id"]:
                    flag_user_channels = True

    # check that user 2 is now in the channel's list of members
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for member in channel["members"]:
                if member["u_id"] == user_2["u_id"]:
                    assert member["channel_permissions"] == 1   # check that the global owner is also invited as a channel owner
                    flag_channel_members = True
    # assert True
    assert flag_user_channels
    assert flag_channel_members
# error when channel_id does not refer to a valid channel that the authorised user is part of
def test_invite_invalid_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    invalid_channel_id = 10     # there are only 2 channels, so 10 is an invalid channel_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_invite(user_1["token"], invalid_channel_id, user_2["u_id"])

# error when u_id of user being invited does not refer to a valid user
def test_invite_invalid_user():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    invalid_u_id = 10   # there are only 2 users, so 10 is an invalid u_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_invite(user_1["token"], channel_public["channel_id"], invalid_u_id)

# error when the user doing the inviting is not already a member of the channel
def test_invite_not_member():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    user_3 = auth_register("ThirdUser@unsw.edu.au", "password333", "Third", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup

    with pytest.raises(AccessError) as e:
        channel_invite(user_2["token"], channel_public["channel_id"], user_3["u_id"])

# error when inviting a user who is already in the channel
def test_invite_already_in_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    channel_join(user_2["token"], channel_public["channel_id"])
    # End of setup

    with pytest.raises(InputError) as e:
        channel_invite(user_1["token"], channel_public["channel_id"], user_2["u_id"])

## channel_details tests
# takes in token of user requesting details and channel id.
# assume that auth_register, channels_create, and channel_join work

def test_details_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup

    assert channel_details(user_1["token"], channel_public["channel_id"]) == {"name":"Public Channel", "owner_members": [{"u_id":1, "name_first":"First", "name_last":"User"}], "all_members":[{"u_id":1, "name_first":"First", "name_last":"User"}]}

# error when channel id is not a valid channel
def test_details_invalid_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    invalid_channel_id = 10     # there are only 2 channels, so 10 is an invalid channel_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_details(user_1["token"], invalid_channel_id)

# error when authorised user is not a member of channel with channel_id
def test_details_not_member():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup

    with pytest.raises(AccessError) as e:
        channel_details(user_2["token"], channel_public["channel_id"])

## channel_messages tests
# takes in token of authorised user searching for messages, channel_id that this user is part of, and index "start"
# assume that auth_register, channels_create, and channel_join work

def test_messages_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    message_1 = message_send(user_1["token"], channel_public["channel_id"], "a message")
    time_1 = 0
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for message in channel["messages"]:
                if message["message_id"] == message_1["message_id"]:
                    time_1 = message["time_created"]
    # End of setup

    assert channel_messages(user_1["token"], channel_public["channel_id"], 0) == {"messages": [
        {
            "message_id":message_1["message_id"],
            "u_id":1,
            "message":"a message",
            "time_created":time_1,
            "reacts":[],
            "is_pinned":False
            }],
                                                                                  "start":0,
                                                                                  "end":-1}

# error when channel_id is not a valid channel
def test_messages_invalid_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    invalid_channel_id = 10     # there are only 2 channels, so 10 is an invalid channel_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_messages(user_1["token"], invalid_channel_id, 0)

# error when start is greater than the total number of messages in the channel
# refer to assumptions
def test_messages_start_greater():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup


    with pytest.raises(InputError) as e:
        channel_messages(user_1["token"], channel_public["channel_id"], 999)

# error when authorised user is not a member of channel with channel_id
def test_messages_not_member():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup

    with pytest.raises(AccessError) as e:
        channel_messages(user_2["token"], channel_public["channel_id"], 0)

## channel_leave tests
# assume that auth_register, channels_create, and channel_join work

def test_leave_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    flag = False
    # End of setup

    channel_leave(user_1["token"], channel_public["channel_id"])

    # check that the channel_id is now out of user 1's list of channel ids
    for user in DATA["users"]:
        if user["u_id"] == user_1["u_id"]:
            assert channel_public["channel_id"] not in user["channels"]

    # check that user 1 is now out of the channel's list of members
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for member in channel["members"]:
                if member["u_id"] == user_1["u_id"]:
                    flag = True

    assert flag == False

# error when channel id is not a valid channel
def test_leave_invalid_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    invalid_channel_id = 10     # there are only 2 channels, so 10 is an invalid channel_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_leave(user_1["token"], invalid_channel_id)

def test_leave_not_member():
# error when authorised user is not a member of channel with channel_id
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    # End of setup

    with pytest.raises(AccessError) as e:
        channel_leave(user_2["token"], channel_public["channel_id"])


## channel_join tests
# assume that auth_register, and channels_create work

def test_join_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    flag_user_channels = False
    flag_channel_members = False
    # End of setup

    channel_join(user_2["token"], channel_public["channel_id"])

    # check that the channel_id is now in user 2's list of channel ids
    for user in DATA["users"]:
        if user["u_id"] == user_2["u_id"]:
            for item in user["channels"]:
                if item["channel_id"] == channel_public["channel_id"]:
                    flag_user_channels = True

    # check that user 2 is now in the channel's list of members
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for member in channel["members"]:
                if member["u_id"] == user_2["u_id"]:
                    flag_channel_members = True
    # assert True
    assert flag_user_channels
    assert flag_channel_members

def test_join_slackr_owner():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    admin_userpermissions_change(user_1["token"], user_2["u_id"], 1)    # change user_2 to a global owner
    flag_user_channels = False
    flag_channel_members = False
    # End of setup

    channel_join(user_2["token"], channel_public["channel_id"])

    # check that the channel_id is now in user 2's list of channel ids
    for user in DATA["users"]:
        if user["u_id"] == user_2["u_id"]:
            for item in user["channels"]:
                if item["channel_id"] == channel_public["channel_id"]:
                    flag_user_channels = True

    # check that user 2 is now in the channel's list of members
    for channel in DATA["channels"]:
        if channel["channel_id"] == channel_public["channel_id"]:
            for member in channel["members"]:
                if member["u_id"] == user_2["u_id"]:
                    assert member["channel_permissions"] == 1   # assert that slackr owner has joined as channel owner
                    flag_channel_members = True
    # assert True
    assert flag_user_channels
    assert flag_channel_members

# error when channel id is not a valid channel
def test_join_invalid_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    invalid_channel_id = 10     # there are only 2 channels, so 10 is an invalid channel_id
    # End of setup

    with pytest.raises(InputError) as e:
        channel_leave(user_1["token"], invalid_channel_id)

# error when channel id refers to a channel that is private (when the authorised user is not an admin)
def test_join_private_channel():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_private = channels_create(user_1["token"], "Private Channel", False)
    # End of setup

    with pytest.raises(AccessError) as e:
        channel_leave(user_2["token"], channel_private["channel_id"])
