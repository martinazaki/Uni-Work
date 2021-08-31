"""
 COMP1531 T1 Project (Backend) 
 This file contains tests for channels_list function
 This was wirtten by Maria Cuyutupa Garcia (z5223865)
"""

import pytest
from channels import channels_list, channels_create
from auth import auth_register
from workspace_admin import workspace_reset

# Tests
def test_channels_list_type():
    workspace_reset()   # This resets the database

    # Users
    register_data1 = auth_register("z5223865@ad.unsw.edu.au", "Kebh@$njsiJ137bj", "Maria", "Cuyutupa") 
    register_data2 = auth_register("smithjohnson@gmail.com", "LSweb7468yet", "Smith", "Johnson") 
    register_data3 = auth_register("wilsonmiller@gmail.com", "bvwir367", "Wilson", "Miller") 
    register_data4 = auth_register("margaretrodriguez@outlook.com", "6473286", "Margaret", "Rodriguez") 
    register_data5 = auth_register("taylorrob3103@hotmail.com", "478hds!@#", "Taylor", "Robinson")

    """
    This test checks whether the function generates the correct output (dict type)
    """
    dict_data1 = channels_list(register_data1["token"])
    dict_data2 = channels_list(register_data2["token"])
    dict_data3 = channels_list(register_data3["token"])
    dict_data4 = channels_list(register_data4["token"])
    dict_data5 = channels_list(register_data5["token"])

    assert type(dict_data2) is dict
    assert type(dict_data3) is dict
    assert type(dict_data1) is dict
    assert type(dict_data4) is dict
    assert type(dict_data5) is dict

"""
These tests check if the function is working and have an output
"""
# User 1
def test_channel_list1():
    workspace_reset()   # This resets the database
    register_data1 = auth_register("luisagarcia@ad.unsw.edu.au", "Kebh@$njsiJ3537bj", "Luisa", "Garcia")

    channel_id1 = channels_create(register_data1["token"], "new_channel", True)
    channel_id2 = channels_create(register_data1["token"], "list to do", True)
    channel_id3 = channels_create(register_data1["token"], "general 2", False)

    assert channels_list(register_data1["token"]) == {"channels": [
        {"channel_id": channel_id1["channel_id"], "name" : "new_channel"},
        {"channel_id": channel_id2["channel_id"], "name" : "list to do"}, 
        {"channel_id": channel_id3["channel_id"], "name" : "general 2"}],
        }

# User 2
def test_channel_list2():
    workspace_reset()   # This resets the database
    register_data2 = auth_register("luisagarcia@ad.unsw.edu.au", "Kebh@$njsiJ3537bj", "Luisa", "Garcia")

    channel_id1 = channels_create(register_data2["token"], "random", False)
    channel_id2 = channels_create(register_data2["token"], "notes for myself", False)
    
    assert channels_list(register_data2["token"]) == {"channels": [
        {"channel_id": channel_id1["channel_id"], "name" : "random"},
        {"channel_id": channel_id2["channel_id"], "name" : "notes for myself"}],
        }

# User 3
def test_channel_list3():
    workspace_reset()   # This resets the database

    register_data3 = auth_register("saralu@ad.unsw.edu.au", "LSwtu7468yet", "Sara", "Lu")

    channel_id1= channels_create(register_data3["token"], "coffee is love", True)
    channel_id2 = channels_create(register_data3["token"], "great mates", False)
    channel_id3 = channels_create(register_data3["token"], "Public", True)
    channel_id4 = channels_create(register_data3["token"], "Git for gab", True)

    assert channels_list(register_data3["token"]) == {"channels": [
        {"channel_id": channel_id1["channel_id"], "name" : "coffee is love"},
        {"channel_id": channel_id2["channel_id"], "name" : "great mates"},
        {"channel_id": channel_id3["channel_id"], "name" : "Public"},
        {"channel_id": channel_id4["channel_id"], "name" : "Git for gab"}],
        }

# User 4
def test_channel_list4():
    workspace_reset()   # This resets the database
    register_data4 = auth_register("tedchan@outlook.com", "647Muyr86", "Ted", "Chan")

    channel_id = channels_create(register_data4["token"], "code&happyness", True)

    assert channels_list(register_data4["token"]) == {"channels": [
        {"channel_id":channel_id["channel_id"], "name":"code&happyness"},]}

# User 5
def test_channel_list5():
    workspace_reset()   # This resets the database
    register_data5 = auth_register("michaelrobinson@hotmail.com", "478bvrb#", "Michael", "Robinson")

    channel_id1 = channels_create(register_data5["token"], "games", False)
    channel_id2 = channels_create(register_data5["token"], "notes", False)
    channel_id3 = channels_create(register_data5["token"], "mates", False)
    channel_id4 = channels_create(register_data5["token"], "new_channel", True)
    channel_id5 = channels_create(register_data5["token"], "LeagueOfLegends", True)
    channel_id6 = channels_create(register_data5["token"], "Not_Public", True)
    channel_id7 = channels_create(register_data5["token"], "Git", False)

    assert channels_list(register_data5["token"]) == {"channels": [
        {"channel_id": channel_id1["channel_id"], "name" : "games"},
        {"channel_id": channel_id2["channel_id"], "name" : "notes"},
        {"channel_id": channel_id3["channel_id"], "name" : "mates"},
        {"channel_id": channel_id4["channel_id"], "name" : "new_channel"},
        {"channel_id": channel_id5["channel_id"], "name" : "LeagueOfLegends"},
        {"channel_id": channel_id6["channel_id"], "name" : "Not_Public"},
        {"channel_id": channel_id7["channel_id"], "name" : "Git"}],
        }



