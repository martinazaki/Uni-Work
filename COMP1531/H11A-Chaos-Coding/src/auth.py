''' Auth Functions.'''

# Written by Martina Zaki, z5264835 and Richard Zhang z5118085.

# Python Libraries
import hashlib
import smtplib
import uuid
from copy import deepcopy
from datetime import datetime

# Project Files
import auth_helpers
from database import get_data, data
from error import InputError

DATA = get_data()
TOKENS = []


# Auth_Login
def auth_login(email, password):
    """User login.

    Params:
    email (string): Email of the user.
    password (string): Password of the user.

    Returns:
    token (string): An authorisation hash.
    u_id (int): A number which identifies the user. Belongs to the user who is being invited.
    """
    DATA = get_data()

    auth_helpers.email_valid(email)

    # Check if email and password match
    found = False
    for user in DATA['users']:
        if user['email'] == email:
            found = True
            u_id = user['u_id']
            if user['password'] != hashlib.sha256(password.encode()).hexdigest():
                raise InputError(description='Password is incorrect')
            else:
                token = user['token']

    if not found:
        raise InputError(description='Email is unused')

    return {
        'u_id': u_id,
        'token': token
    }


# Auth_Logout
def auth_logout(token):
    """User logout.

    Params:
    token (string): An authorisation hash.

    Returns:
    is_success (dictionary): Returns successful logout
    """
    flag = False

    if token in TOKENS:
        flag = True
        TOKENS.remove(token)

    return {
        'is_success': flag
    }


# Auth_Register
def auth_register(email, password, name_first, name_last):
    """User registration.

    Params:
    email (string): Email of the user.
    password (string): Password of the user. 
    name_first (string): First name of the user.
    name_first (string): Last name of the user.

    Returns:
    token (string): An authorisation hash.
    u_id (int): A number which identifies the user. Belongs to the user who is being invited.
    """
    DATA = get_data()

    auth_helpers.email_valid(email)
    auth_helpers.email_in_use(email)
    auth_helpers.password_valid(password)
    auth_helpers.name_valid(name_first)
    auth_helpers.name_valid(name_last)

    new_user = {
        'u_id': 0,
        'token': '',
        'email': '',
        'password': '',
        'name_first': '',
        'name_last': '',
        'handle_str': '',
        'channels': [],
        'global_permissions': 2,
    }

    # Copy of new_user dictionary to append to global data.
    new_user_copy = deepcopy(new_user)

    # Get new user ID
    u_id = auth_helpers.id_generator()
    new_user_copy.update({'u_id': u_id})

    # First user is an owner with global_permission == 1,
    # everyone else is member.
    if u_id == 1:
        new_user_copy.update({'global_permissions': 1})

    # New token
    payload = {'u_id': new_user_copy['u_id'], 'login time': str(datetime.now())}
    token = auth_helpers.generate_token(payload)
    new_user_copy.update({'token': token})

    # New user details
    new_user_copy.update({'email': email})
    encoded_password = hashlib.sha256(password.encode()).hexdigest()
    new_user_copy.update({'password': encoded_password})
    new_user_copy.update({'name_first': name_first})
    new_user_copy.update({'name_last': name_last})

    if DATA['users'] == []:
        new_user_copy.update({'global_permissions': 1})

    # Creating handle
    handle = name_first.lower() + name_last.lower()

    end = auth_helpers.end_no(handle, DATA['users'])

    while (len(handle) + len(str(end))) > 20:
        handle = handle[:-1]
        end = auth_helpers.end_no(handle, DATA['users'])

    if end == 0:
        new_user_copy.update({'handle_str': handle})
    else:
        new_user_copy.update({'handle_str': handle + str(end - 1)})

    DATA['users'].append(new_user_copy)
    DATA['n_users'] += 1

    return {
        'u_id': u_id,
        'token': token
    }


# Auth_Passwordreset_Request
def auth_passwordreset_request(email):
    """Sends an email with a reset code.

    Params:
    email (string): Email of the user.

    Returns:
    none (empty dictionary)
    """

    auth_helpers.email_registered(email)

    sender = 'richard.zhang37@gmail.com'
    receiver = [email]

    reset_code = str(uuid.uuid4())

    subject = "Password reset code"
    name = "Slackr"
    text = "The password reset code for {} is {}.".format(email, reset_code)

    message = "Subject: {}\n\n{}".format(subject, text)

    auth_helpers.add_to_password_reset_database(email, reset_code)

    # Login to Google's SMTP server.
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # Identify yourself to a server.
    server.ehlo()
    # Tells email server that an email client wants to turn exisiting insecure
    # connection into secure one.
    server.starttls()
    server.ehlo()
    # Login to sender gmail account with app password.
    server.login('richard.zhang37@gmail.com', 'xcyrybkvfglqdycv')
    server.sendmail(sender, receiver, message)

    return {}


# Auth_Passwordreset_Reset
def auth_passwordreset_reset(reset_code, new_password):
    """Updates password if reset_code and new_password are valid.

    Params:
    reset_code (string): Reset code to validate user.
    new_password (string): New password generated to user.

    Returns:
    none (empty dictionary).
    """

    email = auth_helpers.return_email_if_reset_code_valid(reset_code)
    auth_helpers.password_valid(new_password)

    auth_helpers.set_password(email, new_password)

    return {}
