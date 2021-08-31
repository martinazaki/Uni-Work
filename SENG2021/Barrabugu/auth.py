import db
import utils
import sqlite3
from errors import *

# Connects to the database and registers a user with given information
def register(email, password, name):
    """ returns the token to give to the front end """
    cur = utils.get_db().cursor()
    try:
        cur.execute(
            """
            INSERT INTO users (email, password, name)
            VALUES (?, ?, ?)
            """,
            (
                email,
                utils.hash_password(password),
                name,
            ),
        )
    except sqlite3.IntegrityError as e:
        # constraint requiring unique emails failed
        # ie. email already used
        raise InputError(f"Email already used {e} {email!r}")

    is_sys_admin = False
    if cur.lastrowid == 1:
        is_sys_admin = True
        # If you are the first user to sign up to the system - make admin
        cur.execute(
            """
            UPDATE users
            SET is_sys_admin=true
            WHERE id=1
            """
        )

    utils.get_db().commit()

    return utils.encode_to_jwt(
        {
            "id": cur.lastrowid,
            "email": email,
            "is_sys_admin": is_sys_admin,
            "name": name,
        }
    )


def login(email, password):
    cur = utils.get_db().cursor()
    cur.execute(
        """
        SELECT id, email, is_sys_admin, password, name
        FROM users
        WHERE email=?
        """,
        (email,),
    )
    row = cur.fetchone()

    if row is None or not utils.check_password(plain_text=password, hashed=row[3]):
        raise AccessError("invalid (email, password) pair")

    return utils.encode_to_jwt(
        {
            "id": row[0],
            "email": row[1],
            "is_sys_admin": row[2],
            "name": row[4],
        }
    )


def logout(token):
    pass


def passwordreset_request(email):
    pass


def passwordreset_reset(reset_token):
    pass


def change_name(token, new_name):
    pass
