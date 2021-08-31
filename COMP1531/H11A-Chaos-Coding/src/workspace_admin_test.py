# Written by Kimberly Sufangga, z5257053
'''
Tests for workspace_reset and admin_userpermission_change functions
'''
# Import functions
import pytest
from error import InputError, AccessError
from auth import auth_register
from channels import channels_create
from workspace_admin import workspace_reset, admin_userpermissions_change
from database import get_data

# Links to the main database
DATA = get_data()

# workspace_reset tests
# test function works
def test_workspace_reset():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    channel_public = channels_create(user_1["token"], "Public Channel", True)
    channel_private = channels_create(user_1["token"], "Private Channel", False)
    # End of setup
    workspace_reset()

    assert DATA["n_users"] == 0
    assert DATA["users"] == []
    assert DATA["n_channels"] == 0
    assert DATA["channels"] == []
    assert DATA["n_messages"] == 0

# admin_userpermissions_change tests
# test function works
def test_admin_userpermissions_change_success():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    # End of setup

    admin_userpermissions_change(user_1["token"], user_2["u_id"], 1)

    for user in DATA["users"]:
        if user["u_id"] == user_2["u_id"]:
            assert user["global_permissions"] == 1

# error when invalid user id (u_id doesn't refer to a valid user)
def test_admin_userpermissions_change_invalid_user():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    invalid_u_id = 10   # there are only 2 users, so 10 is an invalid u_id
    # End of setup

    with pytest.raises(InputError) as e:
        admin_userpermissions_change(user_1["token"], invalid_u_id, 1)

# error when permission id isn't valid
def test_admin_userpermissions_change_invalid_permission_id():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    # End of setup

    with pytest.raises(InputError) as e:
        admin_userpermissions_change(user_1["token"], user_2["u_id"], 3)     # the only permissions are 1 and 2, so 3 is invalid

# error when someone who is not a global owner tries to change global permissions
def test_admin_userpermissions_change_not_owner():
    # Set up database
    workspace_reset()
    user_1 = auth_register("FirstUser@unsw.edu.au", "password123", "First", "User")
    user_2 = auth_register("SecondUser@unsw.edu.au", "password321", "Second", "User")
    # End of setup

    with pytest.raises(AccessError) as e:
        admin_userpermissions_change(user_2["token"], user_1["u_id"], 2)
