'''
Written by Martina Zaki, z5264835
'''

import pytest
from auth import auth_register
import user
from error import InputError
from database import get_data

DATA_LIST = get_data()
USERS = DATA_LIST['users']
#TOKENS = []

# User Profile
def user_profile_success():
    '''Returns info about user'''
    auth_register("isthis_valid1@gmail.com", "validpassword1", "firstname1", "lastname1")
    assert USERS[0]['token'] == 'token'
    assert USERS[0]['u_id'] == 'u_id'

def test_user_invalid_uid():
    '''User id is invalid'''
    login1 = auth_register("isthis_valid1@gmail.com", "validpassword1", "firstname1", "lastname1")
    login2 = auth_register("isthis_valid2@gmail.com", "validpassword12", "firstname2", "lastname2")
    user.user_profile(login1['token'], login1['u_id'])
    with pytest.raises(InputError):
        assert user.user_profile(login2['token'], 'oisjdf')


# User Profile Set Name
def test_username_success():
    '''Successfully updates username'''
    auth_register("isthis_valid123@gmail.com", "Password", "FirstName", "LastName")

def test_user_long_first_name():
    '''First name is too long'''
    with pytest.raises(InputError):
        assert auth_register("isthis_valid1@gmail.com", "Passssword", "m" * 51, "Matthews")

def test_user_long_last_name():
    '''Last name is too long'''
    with pytest.raises(InputError):
        assert auth_register("isthis_valid1@gmail.com", "Passwrodd", "Shawn", "m" * 51)

def test_register_long_names():
    '''Both last and first names are too long'''
    with pytest.raises(InputError):
        assert auth_register("isthis_valid1@gmail.com", "Passswordd", "m" * 51, "m" * 51)


# User Profile Set Email
def test_useremail_success():
    '''Email updated successfully'''
    auth_register("isthis_valid123@gmail.com", "Password", "FirstName", "LastName")

def test_user_email_in_use():
    '''Email in use by another user'''
    login1 = auth_register("isthis_valid1@gmail.com", "Passsworddd", "First", "Last")
    login2 = auth_register("second_email@gmail.com", "Passswordd", "First1", "Last1")
    user.user_profile_setemail(login1['token'], "mynewemail@gmail.com")
    with pytest.raises(InputError):
        assert user.user_profile_setemail(login2['token'], "mynewemail@gmail.com")

def test_user_invalid_email():
    '''Email entered is invalid'''
    with pytest.raises(InputError):
        assert auth_register("isthis_valid.com", "Passsworddd!", "Shawn", "Matthews")


# User Profile Set Handle
def test_userhandle_success():
    '''Handle updated successfully'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], "FirstLastName")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], 'FirstLastName')

def test_user_handle_in_use():
    '''Handle entered is used by another user'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], "FirstLast")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], 'FirstLast')

def test_user_empty():
    '''Handle entered is empty'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], " ")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], ' ')

def test_user_one_character():
    '''Handle entered is one character'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], "A")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], 'A')

def test_user_two_characters():
    '''Handle entered is two characters'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], "AB")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], 'AB')

def test_user_too_long():
    '''Handle entered is too long (in this example 21 characters)'''
    login1 = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    login2 = auth_register("isthis_valid1234@gmail.com", "Passwordd", "First2", "Last2")
    user.user_profile_sethandle(login1['token'], "AnnasimoneEmilyWatson")
    with pytest.raises(InputError):
        assert user.user_profile_sethandle(login2['token'], 'AnnasimoneEmilyWatson')

# User Profile Upload Photo
def test_user_success_photo():
    '''Photo is successfully uploaded'''
    login = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    photograph = "https://i.kym-cdn.com/entries/icons/original/000/031/575/pankcake.jpg"
    user.user_profile_uploadphoto(login['token'], photograph, 0, 0, 200, 200)
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(login['token'], photograph, 0, 0, 200, 200)

def test_user_invalid_url():
    '''Url is not valid'''
    login = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    invalid_photograph = 'https://i.kym-cdn.com/entries/icons/original/000/031/575/pancake.jpg'
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(login['token'], invalid_photograph, 0, 0, 0, 0)

def test_user_invalid_dimensions():
    '''Dimensions are invalid'''
    login = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    photograph = "https://i.kym-cdn.com/entries/icons/original/000/031/575/pankcake.jpg"
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(login['token'], photograph, 0, 0, 900, 900)

def test_user_not_jpg():
    '''Photograph is not type jpg'''
    login = auth_register("isthis_valid123@gmail.com", "Password", "First1", "Last1")
    photograph_url = "https://png.pngtree.com/element_our/sm/20180327/sm_5aba147bcacf2.png"
    with pytest.raises(InputError):
        assert user.user_profile_uploadphoto(login['token'], photograph_url, 0, 0, 100, 150)

# Users All
def test_users_all():
    '''Returns list of all users'''
    return
