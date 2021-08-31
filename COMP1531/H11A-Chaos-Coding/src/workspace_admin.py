# Written by Kimberly Sufangga, z5257053
'''
Contains workspace_reset and admin_userpermission_change functions
'''
# Import functions
from database import get_data
from helpers import is_valid, token_to_user
from error import InputError, AccessError

# Links to the main database
DATA = get_data()

# resets the workspace and database by clearing all fields
def workspace_reset():
    DATA["n_users"] = 0
    DATA["users"].clear()
    DATA["n_channels"] = 0
    DATA["channels"].clear()
    DATA["n_messages"] = 0

    return {}

# changes the global permissions of a user
def admin_userpermissions_change(token, u_id, permission_id):
# user_id is the person who is attempting to change permissions, u_id is the person whose permissions we are trying to change
# since we're not given channel_id, this is about changing global permissions.

    user_id = token_to_user(token)
    is_valid(token, user_id)    # check that the user attempting to change permissions is valid
    # check if u_id of person being invited refers to a valid user
    if u_id > DATA["n_users"]:
        raise InputError(description="u_id does not refer to a valid user")

    if not permission_id in (1, 2):      # check if the permission id is valid
        raise InputError(description="The permission_id isn't valid")

    for user in DATA["users"]:
        if user["u_id"] == user_id:         # find the user who is editing the permissions
            if user["global_permissions"] != 1:   # if they are a global owner, they can edit anyone's permissions
                raise AccessError(description="The authorised user is not an admin or owner")

    # by now user must be a global owner and the permission_id must be valid
    for item in DATA["users"]:    # loop through list of users to find the user we are editing the permissions of
        if item["u_id"] == u_id:
            item["global_permissions"] = permission_id      # change the permissions
    return {}
