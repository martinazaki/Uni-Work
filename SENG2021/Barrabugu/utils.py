import bcrypt
import jwt
import sqlite3
from errors import *
from flask import g, current_app
from secrets import jwt_secret


def encode_to_jwt(obj):
    return jwt.encode(obj, jwt_secret, algorithm="HS256")


def decode_to_jwt(string):
    return jwt.decode(string, jwt_secret, algorithms=["HS256"])


# https://stackoverflow.com/a/23768422/6164984
def hash_password(plain_text):
    plain_text = bytes(plain_text, encoding="utf-8")
    return bcrypt.hashpw(plain_text, bcrypt.gensalt())


def check_password(plain_text, hashed):
    plain_text = bytes(plain_text, encoding="utf-8")
    return bcrypt.checkpw(plain_text, hashed)


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(current_app.config["DATABASE"])
    return db


########################################################################
##                      Data Validation Functions                     ##
########################################################################


def check_valid_student(user_id):
    cur = get_db().cursor()
    # Check valid student
    cur.execute(
        """
        SELECT * FROM enrolments WHERE user_id = ?
        """,
        (user_id,),
    )
    if not cur.fetchone():
        raise ValueError("Student doesn't exist")


def check_valid_team(team_id):
    cur = get_db().cursor()
    # Check valid team
    cur.execute(
        """
        SELECT * FROM teams WHERE id = ?
        """,
        (team_id,),
    )
    if not cur.fetchone():
        raise ValueError("team doesn't exists")


def check_valid_course(course_id):
    cur = get_db().cursor()
    # Check valid course
    cur.execute(
        """
        SELECT * FROM courses WHERE id = ?
        """,
        (course_id,),
    )
    if not cur.fetchone():
        raise ValueError("course doesn't exists")


def auth_admin(token):
    # Get ID from token and check if a valid admin
    cur = get_db().cursor()
    course_admin_id = decode_to_jwt(token)["id"]
    cur.execute(
        """
        SELECT * FROM course_admins WHERE user_id = ?
        """,
        (course_admin_id,),
    )
    if not cur.fetchone():
        raise ValueError("not an admin for the course")


########################################################################
##                     Team Application Functions                     ##
########################################################################


def get_user_course_team(user_id, course_id):
    """ Returns None if user doesn't have a team, otherwise it returns the team id """
    cur = get_db().cursor()

    cur.execute(
        """
        SELECT team_id
        FROM enrolments
        WHERE user_id=?
        AND course_id=?
        """,
        (user_id, course_id),
    )

    team_id = cur.fetchone()
    if team_id:
        return team_id[0]
    else:
        return None


def has_user_already_applied(user_id, team_id):
    cur = get_db().cursor()

    cur.execute(
        """
        SELECT id
        FROM applications
        WHERE from_student_id=?
        AND target_team_id=?
        """,
        (user_id, team_id),
    )

    if cur.fetchone():
        return True
    else:
        return False


def check_user_team_leader(user_id, team_id):
    cur = get_db().cursor()

    cur.execute(
        """
        SELECT leader_id
        FROM teams
        WHERE id=?
        """,
        (team_id,),
    )

    if cur.fetchone()[0] != user_id:
        raise AccessError("You are unable to perform this action in your team")


########################################################################
##                    Permission Checking Functions                   ##
########################################################################


def is_user_student_and_in_course(cur, user_id, course_id):
    # TODO Optimise perms with more specific query to prevent for loop
    cur.execute(
        """
        SELECT course_id
        FROM enrolments
        WHERE user_id=?
        """,
        (user_id,),
    )

    for course in cur.fetchall():
        if course[0] == course_id:
            return True
    return False


# Check if user is an administrator of the given course
def is_user_course_admin(cur, user_id, course_id):
    # TODO Optimise perms with more specific query to prevent for loop
    cur.execute(
        """
        SELECT course_id
        FROM course_admins
        WHERE user_id=?
        """,
        (user_id,),
    )
    for course in cur.fetchall():
        if course[0] == course_id:
            return True
    return False


# Checks if user is a system administrator
def is_user_sys_admin(cur, user_id):
    # TODO Optimise perms with more specific query to prevent for loop
    cur.execute(
        """
        SELECT is_sys_admin
        FROM users
        WHERE id=?
        """,
        (user_id,),
    )
    for course in cur.fetchall():
        if course[0] == 1:
            return True
    return False


def check_user_is_course_student(user_id, course_id):
    # students can not use this
    # course administrator can use this for THEIR COURSE
    # sysadmin

    cur = get_db().cursor()

    in_course = (
        is_user_student_and_in_course(cur, user_id, course_id)
        and not is_user_course_admin(cur, user_id, course_id)
        and not is_user_sys_admin(cur, user_id)
    )

    if not in_course:
        raise AccessError("This function is currently locked to students!")


def check_admin_course_access(user_id, course_id):
    # students can not use this
    # course administrator can use this for THEIR COURSE
    # sysadmin

    cur = get_db().cursor()

    in_course = (
        not is_user_student_and_in_course(cur, user_id, course_id)
        or is_user_course_admin(cur, user_id, course_id)
        or is_user_sys_admin(cur, user_id)
    )

    if not in_course:
        raise AccessError(
            "You are unable to use this function! Check permissions and try again"
        )


def check_user_course_access(user_id, course_id):

    cur = get_db().cursor()

    # Check whether this user is a student enrolled in this course
    # Check whether this user is an administrator for this course
    # Check whether this user is an administrator for this course

    in_course = (
        is_user_student_and_in_course(cur, user_id, course_id)
        or is_user_course_admin(cur, user_id, course_id)
        or is_user_sys_admin(cur, user_id)
    )

    if not in_course:
        raise AccessError("You are not able to see the members of this course!")


def check_user_edit_perms(user_id, student_id, course_id):

    cur = get_db().cursor()

    # Check whether this user is a student enrolled in this course
    # Check whether this user is an administrator for this course
    # Check whether this user is an administrator for this course

    in_course = (
        (
            is_user_student_and_in_course(cur, user_id, course_id)
            and user_id == student_id
        )
        or is_user_course_admin(cur, user_id, course_id)
        or is_user_sys_admin(cur, user_id)
    )

    if not in_course:
        raise AccessError("You do not have permission to edit this user in this course")
