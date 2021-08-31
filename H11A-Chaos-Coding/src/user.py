'''
Written by Martina Zaki, z5264835
'''

from PIL import Image
import auth_helpers
from database import get_data
from error import InputError

TOKENS = []

# User_Profile
def user_profile(token, u_id):
    """Returns information about user.

    Params:
    token (string): An authorisation hash.
    u_id (int): A number which identifies the user. Belongs to the user who is being invited.

    Returns:
    user (dictionary): Information about the user id, email, first name, last name, and handle.
    """

    auth_helpers.verify_user(token) # Verify is user is authorized

    users = auth_helpers.get_users()

    user = {}   
    for single_user in users:
        if single_user['u_id'] == u_id:
            user = single_user.copy()
            return {'user': user}

    raise InputError(description='Cannot find u_id')


# User_Profile_Setname
def user_profile_setname(token, name_first, name_last):
    """Updates user's name.

    Params:
    token (string): An authorisation hash.
    name_first (string): First name of the user.
    name_first (string): Last name of the user.

    Returns:
    none (empty dictionary).
    """

    auth_helpers.verify_user(token) # Verify is user is authorized
    data = get_data()

    # Checking if length of first and last name fits requirements
    for user in data['users']:
        if len(user['name_first']) <= 1 and len(user['name_first']) >= 50:
            raise InputError(description='First name is not between 1-50 characters')

        if len(user['name_last']) <= 1 and len(user['name_last']) >= 50:
            raise InputError(description='Last name is not between 1-50 characters')

    users = auth_helpers.get_users()
    u_id = auth_helpers.id_from_token(token)

    # Updating user's name
    for user in users:
        if user['u_id'] == u_id:
            user['name_first'] = name_first
            user['name_last'] = name_last

    return {}   #### Added this return

# User_Profile_Setemail
def user_profile_setemail(token, email):
    """Updates user's email.

    Params:
    token (string): An authorisation hash.
    email (string): Email of the user.

    Returns:
    none (empty dictionary)
    """
    auth_helpers.verify_user(token) # Verify is user is authorized
    users = auth_helpers.get_users()

    auth_helpers.email_valid(email)

    # Checking if email is already being used
    auth_helpers.email_in_use(email)

    # Updating email
    for user in users:
        if user['u_id'] == auth_helpers.id_from_token(token):
            user.update({'email': email})

    return {}   #### Added this return

# User_Profile_Sethandle
def user_profile_sethandle(token, handle_str):
    """Updates user's handle

    Params:
    token (string): An authorisation hash.
    handle (string): Handle of the user.

    Returns:
    none (empty dictionary)    
    """
    auth_helpers.verify_user(token) # Verify is user is authorized
    users = auth_helpers.get_users()

    # Check if handle is already being used
    for user in users:
        if user['handle_str'] == handle_str:
            raise InputError(description='Handle is already in use')

    # Check if handle length fits requirements
    for user in users:
        if len(user['handle_str']) <= 2 and len(user['handle_str']) >= 20:
            raise InputError(description='Handle is not in between 3-20 characters')

    # Updating handle
    for user in users:
        if user['u_id'] == auth_helpers.id_from_token(token):
            user.update({'handle_str': handle_str})

    return {} #### Added this return

# User_Profile_UploadPhoto
def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    """Upload's users photo.

    Params:
    token (string): An authorisation hash.
    img_url (string): URL of the photo for user.
    x_start (int) : Dimension of photo.
    y_start (int) : Dimension of photo.
    x_end (int) : Dimension of photo.
    y_end (int) : Dimension of photo.

    Returns:
    none (empty dictionary).
    """
    auth_helpers.verify_user(token) # Verify is user is authorized
    users = auth_helpers.get_users()

    # Checks if img is a jpg
    split_url = img_url.split('.')
    if split_url[-1] != 'jpg':
        raise InputError(description='Image uploaded is not a JPG')

    # Opens image
    img = Image.open(img_url)

    # Checks image dimensions are right as specified
    filename = 'photo.jpg'
    with Image.open(filename) as image:
        photo_width, photo_height = image.size

    if (x_end - x_start) > photo_width:
        raise InputError(description='Width is not within the dimensions of the image at the URL.')

    elif (y_end - y_start) > photo_height:
        raise InputError(description='Height is not within the dimensions of the image at the URL.')

    if x_start >= x_end:
        raise InputError(description='Start is not within the dimensions of the image at the URL.')

    if y_start >= y_end:
        raise InputError(description='Start is not within the dimensions of the image at the URL.')

    # Crops image
    area = (x_start, y_start, x_end, y_end)
    img = img.crop(area)

    #Saved in the same relative location
    img.save("cropped_photo.jpg")

    # Update photo
    for user in users:
        if user['u_id'] == auth_helpers.id_from_token(token):
            user[0]['img_url'] = 'http://http://localhost:8956/pic/' + str(user['u_id']) + '.jpg'

    return{}

# User_All
def users_all(token):
    """Gets list of all users and their details.

    Params:
    token (string): An authorisation hash.

    Returns:
    user (dictionary): Information about their user id, email, first name, last name, and handle.
    """

    auth_helpers.verify_user(token) # Verify is user is authorized
    users = auth_helpers.get_users()

    return {'users': users}
