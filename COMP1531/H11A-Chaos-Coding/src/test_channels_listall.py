"""
 COMP1531 T1 Project (Backend) 
 This file contains tests for channels_listall function
 This was wirtten by Maria Cuyutupa Garcia (z5223865)
"""

import pytest
from workspace_admin import workspace_reset
from channels import channels_listall, channels_create
from auth import auth_register
from workspace_admin import workspace_reset

# This resets the database
workspace_reset()

"""
These tests assume that auth_register and channels_create functions work

Assumption:
* All type of channels are displayed, either public or private.
"""

# Tests  
def test_channels_listall_type():
    """
    This test checks whether the function generates the correct output (dict type)
    """
    register_data1 = auth_register("davidjohn5@ad.unsw.edu.au", "K**h@$njsiJ137bj", "David", "John") # User 1
    register_data2 = auth_register("lauraeilish@ad.unsw.edu.au", "LSw787eb7468yet", "Laura", "Eilish") # User 2
    register_data3 = auth_register("walterjackson@ad.unsw.edu.au", "bvwCBDJir367", "Walter", "Jackson") # User 3
    register_data4 = auth_register("tomothygreen@ad.unsw.edu.au", "64732hfebUT6", "Timothy", "Green") # User 4
    register_data5 = auth_register("hiromisato@ad.unsw.edu.au", "478h3682bds!@#", "Hiromi", "Sato") # User 5

    dict_data1 = channels_listall(register_data1["token"])
    dict_data2 = channels_listall(register_data2["token"])
    dict_data3 = channels_listall(register_data3["token"])
    dict_data4 = channels_listall(register_data4["token"])
    dict_data5 = channels_listall(register_data5["token"])

    assert type(dict_data2) is dict
    assert type(dict_data3) is dict
    assert type(dict_data1) is dict
    assert type(dict_data4) is dict
    assert type(dict_data5) is dict

"""
These tests check if the function is working and have an output
"""
def test_channel_listall_1():
    workspace_reset()

    register_data1 = auth_register("davidjohn5@ad.unsw.edu.au", "K**h@$njsiJ137bj", "David", "John") # User 1
    register_data2 = auth_register("lauraeilish@ad.unsw.edu.au", "LSw787eb7468yet", "Laura", "Eilish") # User 2

    # User 1 channels' id
    channel_id1 = channels_create(register_data1["token"], "channel_1", True)
    channel_id2 = channels_create(register_data1["token"], "channel_2", True)

    # User 2 channels' id
    channel_id3 = channels_create(register_data2["token"], "channel_3", False)
    channel_id4 = channels_create(register_data2["token"], "channel_4", True)
    channel_id5 = channels_create(register_data2["token"], "channel_5", False)

    # Displays all the lists that were created
    assert channels_listall(register_data1["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "channel_1"},
        {"channel_id": channel_id2["channel_id"], "name" : "channel_2"},
        {"channel_id": channel_id3["channel_id"], "name" : "channel_3"},
        {"channel_id": channel_id4["channel_id"], "name" : "channel_4"},
        {"channel_id": channel_id5["channel_id"], "name" : "channel_5"}]
    }

    assert channels_listall(register_data2["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "channel_1"},
        {"channel_id": channel_id2["channel_id"], "name" : "channel_2"},
        {"channel_id": channel_id3["channel_id"], "name" : "channel_3"},
        {"channel_id": channel_id4["channel_id"], "name" : "channel_4"},
        {"channel_id": channel_id5["channel_id"], "name" : "channel_5"}]
    }

def test_channel_listall_2():
    workspace_reset()

    register_data3 = auth_register("walterjackson@ad.unsw.edu.au", "bvwCBDJir367", "Walter", "Jackson") # User 3
    register_data4 = auth_register("tomothygreen@ad.unsw.edu.au", "64732hfebUT6", "Timothy", "Green") # User 4

    # User 3 channel's id
    channel_id1 = channels_create(register_data3["token"], "Fantastic 4", True)
    channel_id2 = channels_create(register_data3["token"], "ChaosCoding Notices", False)

    # User 4 channel id
    channel_id3 = channels_create(register_data4["token"], "music", True)

    # Display all the lists that were created
    assert channels_listall(register_data3["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "Fantastic 4"},
        {"channel_id": channel_id2["channel_id"], "name" : "ChaosCoding Notices"},
        {"channel_id": channel_id3["channel_id"], "name" : "music"}],
    }

    assert channels_listall(register_data4["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "Fantastic 4"},
        {"channel_id": channel_id2["channel_id"], "name" : "ChaosCoding Notices"},
        {"channel_id": channel_id3["channel_id"], "name" : "music"}],
    }

def test_channel_listall_3():
    workspace_reset()

    register_data1 = auth_register("davidjohn5@ad.unsw.edu.au", "K**h@$njsiJ137bj", "David", "John") # User 1
    register_data5 = auth_register("hiromisato@ad.unsw.edu.au", "478h3682bds!@#", "Hiromi", "Sato") # User 5

    # User 1
    channel_id1 = channels_create(register_data1["token"], "new channel", True)

    # User 5
    channel_id2 = channels_create(register_data5["token"], "entrepreneurs", False)
    channel_id3 = channels_create(register_data5["token"], "folks", True)

    # Display all the lists that were created
    assert channels_listall(register_data1["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "new channel"},
        {"channel_id": channel_id2["channel_id"], "name" : "entrepreneurs"},
        {"channel_id": channel_id3["channel_id"], "name" : "folks"}],
    }

    assert channels_listall(register_data5["token"]) == {"channels" : [
        {"channel_id": channel_id1["channel_id"], "name" : "new channel"},
        {"channel_id": channel_id2["channel_id"], "name" : "entrepreneurs"},
        {"channel_id": channel_id3["channel_id"], "name" : "folks"}],
    }





