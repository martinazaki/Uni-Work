''' Auth Helper Functions.'''

# Written by Martina Zaki, z5264835 and Richard Zhang z5118085.

# Python Libraries
import re
import hashlib
from copy import deepcopy
import jwt

# Project Files
import helpers
from database import get_data
from error import InputError, AccessError

SECRET = 'chaoscoding'

TOKENS = []
PASSWORD_MIN_LEN = 6
NAME_MAX_LEN = 50

PASSWORD_RESET_DATA = {
    'reset_codes': []
}


def verify_user(token):
    """Verify if the user is authorised in Slackr.

    Params:
    token (string): An authorisation hash.

    Returns:
    none
    """
    u_id = helpers.token_to_user(token)
    helpers.is_valid(token, u_id)


def get_users():
    """Gets user data.

    Params:
    none

    Returns:
    none
    """
    DATA_LIST = get_data()

    return DATA_LIST['users']


def id_from_token(token):
    """Gets user id from token.

    Params:
    token (string): An authorisation hash.

    Returns:
    none
    """
    get_id = jwt.decode(token, SECRET, algorithms=['HS256'])
    return get_id['u_id']


def password_valid(password):
    """Checks password length.
    Params:
    password (string): Password of the user.

    Returns:
    none
    """
    if len(password) < PASSWORD_MIN_LEN:
        raise InputError(description='Password too short')


def name_valid(name):
    """Checks name length.
    
    Params:
    name (string): Name of the user.

    Returns:
    none
    """
    if (len(name) < 1) or (len(name) > NAME_MAX_LEN):
        raise InputError(description='Name is not between 1-50 characters')


def email_valid(email):
    """Checks if email is valid.

    Params:
    email (string): Email of the user.

    Returns:
    none
    """
    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if not re.search(regex, email):
        raise InputError(description='Email is not valid')


def generate_token(payload):
    """Generates token.

    Params:
    payload (string): Payload of the user.

    Returns:
    none
    """

    new_token = jwt.encode(payload, SECRET, algorithm='HS256')
    TOKENS.append(new_token)
    return new_token.decode('UTF-8')    ## DECODED


def end_no(handle, users):
    """Checks handle count.

    Params:
    handle (string): Handle of the user.
    users (dictionary): Information about user.

    Returns:
    none
    """
    end = 0
    for user in users:
        if handle in user['handle_str']:
            end += 1
        if handle not in user['handle_str'] and end != 0:
            break

    return end


def id_generator():
    """Generates user ID.

    Params:
    none

    Returns:
    none
    """
    DATA_LIST = get_data()

    user_list = DATA_LIST['users']  # List of user dictionaries.

    if user_list == []: ## 1st registered user has u_id = 1.
        new_id = 1

    else:
        last_id = user_list[-1]['u_id']  ## New entry is last entry id + 1.
        new_id = last_id + 1

    return new_id


def email_in_use(email):
    """Checks if email is already registered.

    Params:
    email (string): Email of the user.

    Returns:
    none
    """
    DATA_LIST = get_data()

    for user in DATA_LIST['users']:
        if user['email'] == email:
            raise InputError(description='Email is already in use')


def email_registered(email):
    """Checks if email belongs to a registered user.
    
    Params:
    email (string): Email of the user.

    Returns:
    none
    """
    DATA_LIST = get_data()

    flag = False
    for user in DATA_LIST['users']:
        if user['email'] == email:
            flag = True
            break

    if not flag:
        raise AccessError(description='Email does not belong to a registed user')


def add_to_password_reset_database(email, reset_code):
    """Adds password reset code to reset_data.

    Params:
    email (string): Email of the user.
    reset_code (string): Reset code to validate user.

    Returns:
    none
    """

    reset_data = {
        "email": '',
        "reset_code": ''
    }

    reset_data_copy = deepcopy(reset_data)

    reset_data_copy.update({"email": email})
    reset_data_copy.update({"reset_code": reset_code})

    PASSWORD_RESET_DATA["reset_codes"].append(reset_data_copy)


def return_email_if_reset_code_valid(reset_code):
    """Return corresponding email if reset_code is found.

    Params:
    reset_code (string): Reset code to validate user.

    Returns:
    none
    """

    flag = False
    for user in PASSWORD_RESET_DATA['reset_codes']:
        if user['reset_code'] == reset_code:
            flag = True
            return user['email']

    if not flag:
        raise InputError(description='Invalid reset code.')


def set_password(email, password):
    """Changes password.

    Params:
    email (string): Email of the user.
    password (string): Password of the user.

    Returns:
    none
    """
    DATA_LIST = get_data()

    encoded_password = hashlib.sha256(password.encode()).hexdigest()

    for user in DATA_LIST['users']:
        if user['email'] == email:
            user['password'] = encoded_password
