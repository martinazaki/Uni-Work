# This was wirtten by Maria Cuyutupa Garcia (z5223865)
"""
 COMP1531 T1 Project (Backend) 
 This file contains tests for channel_addowner function
"""

#pylint: disable=trailing-whitespace
#pylint: disable=missing-function-docstring 
#pylint: disable=unused-variable
#pylint: disable=invalid-name

# Python libraries
from random import randint
import pytest

# Project Files
from channels import channels_create
from channel import channel_addowner, channel_invite
from auth import auth_register
from error import InputError, AccessError
from workspace_admin import workspace_reset

"""
Assumption:
The user created is alredy login
The User that creates that channel automatically becomes a owner.
"""

# Tests

# These tests raise an error when user with user id u_id is already an owner of the channel
def test_user_already_owner1():
    # Resets the data
    workspace_reset()

    # Users
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    user2 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez") 

    # Creates channel, invite other users
    channel_id = channels_create(user1["token"], "general 2", False)
    channel_invite(user1["token"], channel_id["channel_id"], user2["u_id"])

    # Add an owner
    channel_addowner(user1["token"], channel_id["channel_id"], user2["u_id"])
    
    # Raises error because user is already an owner
    with pytest.raises(InputError) as e: 
        channel_addowner(user1["token"], channel_id["channel_id"], user2["u_id"])

# Case when the User that created the channel try to add itself
def test_user_already_owner2():
    # Resets the data
    workspace_reset()

    # User
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 

    # Create the channel
    channel_id = channels_create(user1["token"], "stand-up", True) 

    # Raises error because user is already an owner
    with pytest.raises(InputError) as e:
        channel_addowner(user1["token"], channel_id["channel_id"], user1["u_id"])


# These tests raise an error if the Channel ID is not a valid channel. 
"""
Assumption:
All the numbers generated by randint do not match with any Channel IDs since the range of this 
is from 10000 to 100000.
"""
def test_channel_id_error1():
    # Resets the data
    workspace_reset()

    # Users
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    user2 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller")

    # Create the channel and invite user
    channel_id = channels_create(user1["token"], "random_name", True)
    channel_invite(user1["token"], channel_id["channel_id"], user2["u_id"])

    # Raises an error because channel id is not valid
    with pytest.raises(InputError) as e:
        assert channel_id["channel_id"] != randint(10000, 100000)
        channel_addowner(user1["token"], randint(10000, 100000), user2["u_id"])

def test_channel_id_error2():
    # Resets the data
    workspace_reset()

    # Users
    user2 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    user5 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson")

    # Create the channel and invite the user
    channel_id = channels_create(user2["token"], "new_channel", False)
    channel_invite(user2["token"], channel_id["channel_id"], user5["u_id"])

    # Raises an error because channel id is not valid
    with pytest.raises(InputError) as e:
        assert channel_id["channel_id"] != randint(10000, 100000)
        channel_addowner(user2["token"], randint(10000, 100000), user5["u_id"])

def test_channel_id_error3():
    # Resets the data
    workspace_reset()

    # Users
    user4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez")
    user3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller")

    # Create the channel and invite the user
    channel_id = channels_create(user3["token"], "new_general", False)
    channel_invite(user3["token"], channel_id["channel_id"], user4["u_id"])

    # Raises an error because channel id is not valid
    with pytest.raises(InputError) as e:
        assert channel_id["channel_id"] != randint(10000, 100000)
        channel_addowner(user3["token"], randint(10000, 100000), user4["u_id"])

"""
AccessError
These tests raise an error when the authorised user is not an owner of the slackr, or an owner of this channel
"""
# Not an owner of the channel or slarck
def test_user_not_member1():
    # Resets the data
    workspace_reset()

    # Users 
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson")
    user4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez")
    user2 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson") 

    # Creates channel
    channel_id = channels_create(user2["token"], "The noobs", False)

    # Raises an error because user is not an owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user4["token"], channel_id["channel_id"], user1["u_id"])

def test_user_not_member2():
    # Resets the data
    workspace_reset()

    # Users
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson")
    user3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller") 
    user4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez")
    user2 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson") 


    # Creates channel, invite other users
    channel_id = channels_create(user3["token"], "C lovers", False)
    channel_invite(user3["token"], channel_id["channel_id"], user4["u_id"])
    channel_invite(user3["token"], channel_id["channel_id"], user2["u_id"])

    # Raises an error because user is not an owner
    with pytest.raises(AccessError) as e:
        channel_addowner(user2["token"], channel_id["channel_id"], user1["u_id"])

# Owner of slackr
def test_user_owner3():
    # Resets the data
    workspace_reset()

    # Users
    user1 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    user2 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson") 
    user3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller") 
 
    # Creates channel
    channel_id = channels_create(user2["token"], "general 2", True)
    channel_invite(user2["token"], channel_id["channel_id"], user3["u_id"])

    # Should not raise an error because user is an owner of slackr
    channel_addowner(user1["token"], channel_id["channel_id"], user3["u_id"])





