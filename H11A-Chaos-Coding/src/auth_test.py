'''
Written by Richard Zhang, z5118085, March 2020.
Edited by Martina Zaki, z5264835
'''

import pytest
import auth
from error import InputError
from database import get_data
from workspace_admin import workspace_reset

DATA_LIST = get_data()
USERS = DATA_LIST['users']


## auth_register tests.
def test_register_success():
    '''User is able to register successfully'''
    workspace_reset() # Resets the data

    auth.auth_register("richard.zhang@gmail.com", "Abcd1234", "Richard", "Zhang")
    assert USERS[0]['email'] == "richard.zhang@gmail.com"
    assert USERS[0]['name_first'] == "Richard"
    assert USERS[0]['name_last'] == "Zhang"

def test_register_duplicate_email():
    '''Email entered already exists'''
    workspace_reset() # Resets the data

    auth.auth_register("richard.zhang@gmail.com", "Abcd1234", "Richard", "Zhang")
    with pytest.raises(InputError):
        assert auth.auth_register("richard.zhang@gmail.com", "sfoijsdfoij", "Steve", "Willdoit")

def test_register_invalid_email():
    '''Invalid email entered'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("valetrri.bottas.com", "WellDoneValtteri!", "Valtteri", "Bottas")

def test_register_short_password():
    '''Password is too short'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("daniel.ricciardo@gmail.com", "DR3", "Daniel", "Ricciardo")

def test_register_empty_firstname():
    '''No first name provided'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("sebastian.vettel@gmail.com", "GrazziRagazzi", "", "Vettel")

def test_register_long_first_name():
    '''First name is too long'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("carlos.sainz@gmail.com", "SmooooothOperator", "c" * 51, "Sainz")

def test_register_long_last_name():
    '''Last name is too long'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("carlos.sainz@gmail.com", "SmooooothOperator", "Carlos", "c" * 51)

def test_register_long_names():
    '''Both first and last names are too long'''
    workspace_reset() # Resets the data

    with pytest.raises(InputError):
        assert auth.auth_register("carlos.sainz@gmail.com", "SmooooothOperator", "c" * 51, " " * 51)

## auth_login tests.

def test_auth_login():
    '''User logged in successfully'''
    workspace_reset() # Resets the data

    rego1 = auth.auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login1 = auth.auth_login("max.verstappen@gmail.com", "OrangeArmy33")

    assert rego1['u_id'] == login1['u_id']

def test_auth_incorrect_password():
    '''Wrong password entered'''
    workspace_reset() # Resets the data
    auth.auth_register("israel.adesanya@gmail.com", "TheLastStyleBender185", "Israel", "Adesanya")

    with pytest.raises(InputError):
        assert auth.auth_login("israel.adesanya@gmail.com", "CityKickboxing")

def test_auth_invalid_email():
    '''Invalid email entered'''
    workspace_reset() # Resets the data
    with pytest.raises(InputError):
        assert auth.auth_login("valterri.bottas.com", "WellDoneValtteri!")

# Assume blank fields are invalid and raise exceptions.
def test_auth_blank_email():
    '''Empty email entered'''
    workspace_reset() # Resets the data
    with pytest.raises(InputError):
        assert auth.auth_login(" ", "WellDoneValtteri!")

def test_auth_blank_password():
    '''Empty password entered'''
    workspace_reset() # Resets the data
    with pytest.raises(InputError):
        assert auth.auth_login("valterri.bottas@gmail.com", " ")

def test_auth_blank_both():
    '''Both password and email enteries are empty'''
    workspace_reset() # Resets the data
    with pytest.raises(InputError):
        assert auth.auth_login(" ", " ")

# Assuming "nico.hulkenburg@gmail.com" does not belong to a user.
def test_email_nonexistent():
    '''Email does not exist'''
    workspace_reset() # Resets the data
    with pytest.raises(InputError):
        assert auth.auth_login("nico.hulkenburg@gmail.com", "LookingForAJob")

## auth_logout tests.

def test_logout_success():
    '''User logout successfully'''
    workspace_reset() # Resets the data
    auth.auth_register("max.verstappen@gmail.com", "OrangeArmy33", "Max", "Verstappen")
    login3 = auth.auth_login("max.verstappen@gmail.com", "OrangeArmy33")

    assert auth.auth_logout(login3['token'])

# Assuming "InvalidToken" is an invalid token.
def test_logout_fail():
    '''User was not able to logout'''
    workspace_reset() # Resets the data
    assert auth.auth_logout("InvalidToken")
