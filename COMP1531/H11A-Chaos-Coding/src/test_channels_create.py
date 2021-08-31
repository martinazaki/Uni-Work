"""
 COMP1531 T1 Project (Backend) 
 This file contains tests for the channels_create function.
 This was wirtten by Maria Cuyutupa Garcia (z5223865).
"""

import pytest
from channels import channels_create
from auth import auth_register
from error import InputError
from workspace_admin import workspace_reset



# Tests
def test_channel_id_type():
    workspace_reset() # This resets the database

    # Users
    register_data1 = auth_register("z5223865@ad.unsw.edu.au", "Kebh@$njsiJ137bj", "Maria", "Cuyutupa") 
    register_data2 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    register_data3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller") 
    register_data4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez") 
    register_data5 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson")
    """
    This test checks whether the function generates the correct output (int type)
    """
    # Channels' id for all the Users
    channel_id1 = channels_create(register_data1["token"], "stand-up", True) 
    channel_id2 = channels_create(register_data2["token"],"list to do", True)
    channel_id3 = channels_create(register_data3["token"], "general 2", False)
    channel_id4 = channels_create(register_data4["token"], "entrepreneurs", False)
    channel_id5 = channels_create(register_data5["token"], "folks", True)

    # Checking type output function
    assert type(channel_id1["channel_id"]) is int 
    assert type(channel_id2["channel_id"]) is int
    assert type(channel_id3["channel_id"]) is int
    assert type(channel_id4["channel_id"]) is int
    assert type(channel_id5["channel_id"]) is int

def test_extra_channels_same_user():
    """
    This test checks if the function is generating different ids for different 
    channels although all of them are created by the same user
    """
    workspace_reset() # This resets the database

    # Users
    register_data1 = auth_register("z5223865@ad.unsw.edu.au", "Kebh@$njsiJ137bj", "Maria", "Cuyutupa") 
    register_data2 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    register_data3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller") 

    # User 1 channels' id
    channel_id1 = channels_create(register_data1["token"], "stand-up", True)
    channel_id2 = channels_create(register_data1["token"], "general 2", True)
    channel_id3 = channels_create(register_data1["token"], "i love cats", False)

    # User 2 channesls' id
    channel_id4 = channels_create(register_data2["token"], "notes for myself", False)
    channel_id5 = channels_create(register_data2["token"], "great mates", False)

    # User 3 channels' id
    channel_id6 = channels_create(register_data3["token"], "Fantastic 4", True)
    channel_id7 = channels_create(register_data3["token"], "Chaos Coding Notices", True)
    channel_id8 = channels_create(register_data3["token"], "Public", True)
    channel_id9 = channels_create(register_data3["token"], "List", False)
    channel_id10 = channels_create(register_data3["token"], "Git for gab", True)

    # Verifying channels' id for User 1
    assert channel_id1["channel_id"] != channel_id2["channel_id"]
    assert channel_id2["channel_id"] != channel_id3["channel_id"]
    assert channel_id3["channel_id"] != channel_id1["channel_id"]

    # Verifying channels' id for User 2
    assert channel_id4["channel_id"] != channel_id5["channel_id"]

    # Verifying channels' id for User 3
    assert channel_id6["channel_id"] != channel_id7["channel_id"]
    assert channel_id6["channel_id"] != channel_id8["channel_id"]
    assert channel_id6["channel_id"] != channel_id9["channel_id"]
    assert channel_id6["channel_id"] != channel_id10["channel_id"]
    assert channel_id7["channel_id"] != channel_id8["channel_id"]
    assert channel_id7["channel_id"] != channel_id9["channel_id"]
    assert channel_id7["channel_id"] != channel_id10["channel_id"]
    assert channel_id8["channel_id"] != channel_id9["channel_id"]
    assert channel_id8["channel_id"] != channel_id10["channel_id"]
    assert channel_id9["channel_id"] != channel_id10["channel_id"]

"""
These tests checks whether the input name is a string which length is less than or equal to
20 char, otherwise it raises an error. 
"""
def test_name_error1():
    workspace_reset() # This resets the database
    register_data1 = auth_register("z5223865@ad.unsw.edu.au", "Kebh@$njsiJ137bj", "Maria", "Cuyutupa") 

    with pytest.raises(InputError) as e:
        channels_create(register_data1["token"], "This line contains more than 20 chars", True)

def test_name_error2():
    workspace_reset() # This resets the database
    register_data2 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 

    with pytest.raises(InputError) as e:
        channels_create(register_data2["token"], "This line has 22 chars", False)
    

def test_name_error3():
    workspace_reset() # This resets the database
    register_data3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller")

    with pytest.raises(InputError) as e:
        channels_create(register_data3["token"], "a"*21, True)
   

def test_name_error4():
    workspace_reset() # This resets the database
    register_data4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez")

    with pytest.raises(InputError) as e:
        channels_create(register_data4["token"], "eenie meenie miney mo", True)
    

def test_name_error5():
    workspace_reset() # This resets the database
    register_data5 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson")

    with pytest.raises(InputError) as e:
        channels_create(register_data5["token"], "keep calm and code :)", False)
    

 

