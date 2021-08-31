import sqlite3
import db
import utils
from errors import *
from utils import (
    check_user_course_access,
    check_user_edit_perms,
    check_valid_student,
    check_valid_course,
    check_valid_team,
    check_admin_course_access,
)


########################################################################
##                    Student Interaction Functions                   ##
########################################################################


def move(token, course_id, source_team_id, dest_team_id, student_id):
    admin_id = utils.decode_to_jwt(token)["id"]

    check_admin_course_access(admin_id, course_id)

    check_valid_student(student_id)

    check_valid_team(source_team_id)
    check_valid_team(dest_team_id)

    cur = utils.get_db().cursor()

    cur.execute(
        """
        SELECT course_id
        FROM enrolments
        WHERE team_id = ?
        """,
        (source_team_id,),
    )

    record = cur.fetchone()

    source_team_course_id = record[0]

    cur.execute(
        """
        SELECT course_id
        FROM enrolments
        WHERE team_id = ?
        """,
        (dest_team_id,),
    )

    record = cur.fetchone()

    dest_team_course_id = record[0]

    # TODO: Delete team if no more members in team
    # TODO: Reassign leadership if leader is moved and there are still members in the team

    if (
        source_team_course_id == dest_team_course_id
        and source_team_course_id == course_id
    ):
        # Execute Operation
        cur.execute(
            """
            UPDATE enrolments SET team_id = ? WHERE user_id = ?
            """,
            (
                dest_team_id,
                student_id,
            ),
        )

        utils.get_db().commit()
    else:
        raise InputError("Cannot move student between teams in different courses")


def edit_student(token, student_id, description, course_id):
    # TODO ability to change email (course_admin??)
    user_id = utils.decode_to_jwt(token)["id"]

    # Verify whether the user is allowed to edit this student
    check_user_edit_perms(user_id, student_id, course_id)

    cur = utils.get_db().cursor()

    cur.execute(
        """
        UPDATE enrolments
        SET description = ?
        WHERE user_id = ? AND course_id = ?
        """,
        (description, student_id, course_id),
    )
    utils.get_db().commit()


########################################################################
##                  Course Administration Functions                   ##
########################################################################


# Student details is a list of lists consisting of {name, email, description}
def import_students(token, course_id, clear, student_details):
    admin_id = utils.decode_to_jwt(token)["id"]
    cur = utils.get_db().cursor()

    check_admin_course_access(admin_id, course_id)

    # Check whether should clear enrolments prior to import
    if clear is True:
        try:
            cur.execute(
                """
                    DELETE FROM enrolments WHERE course_id = ?
                """,
                (course_id,),
            )
            utils.get_db().commit()
        except error:
            raise InputError("Something went wrong when clearing enrolments.")

    user_ids = []
    # Iterate over every student that is being imported
    for student in student_details:

        # Check if this student's email is already in the system
        cur.execute(
            """
            SELECT id FROM users WHERE email = ?
            """,
            (student["email"],),
        )

        record = cur.fetchone()
        # Only automatically register the student in the check above was not successful
        if not record:
            # Register the student with default info
            cur.execute(
                """
                INSERT INTO users (name, email) VALUES (?, ?)
                """,
                (
                    student["name"],
                    student["email"],
                ),
            )
            utils.get_db().commit()
            user_id = cur.lastrowid
        else:
            # Get existing user id if user already exists
            user_id = record[0]

        # Insert into enrolments
        cur.execute(
            """
            INSERT INTO enrolments (user_id, course_id, description) VALUES (?, ?, ?)
            """,
            (
                user_id,
                course_id,
                student["description"],
            ),
        )
        utils.get_db().commit()
        user_ids.append(user_id)
    return user_ids


def organise_teamless(token, course_id):
    cur = utils.get_db().cursor()
    admin_id = utils.decode_to_jwt(token)["id"]
    check_admin_course_access(admin_id, course_id)
    check_valid_course(course_id)

    try:
        cur.execute(
            """
                SELECT * FROM enrolments WHERE course_id = ? AND team_id IS NULL
            """,
            (course_id),
        )
    except error:
        raise InputError("Something went wrong when getting teamless students.")

    teamless_students = cur.fetchall()

    try:
        cur.execute(
            """
                SELECT team_id, COUNT(*)
                FROM enrolments
                WHERE course_id = ? AND team_id IS NOT NULL
                GROUP BY team_id
                HAVING COUNT(*) < (SELECT team_cap FROM courses WHERE id = ?)
            """,
            (course_id, course_id),
        )
    except error:
        raise InputError("Something went wrong when getting unfilled teams in course.")

    unfilled_teams = cur.fetchall()

    utils.get_db().commit()


def set_freeze(token, frozen, course_id):
    cur = utils.get_db().cursor()
    admin_id = utils.decode_to_jwt(token)["id"]
    check_admin_course_access(admin_id, course_id)
    check_valid_course(course_id)
    # Execute Operation
    cur.execute(
        """
        UPDATE courses SET frozen = ? WHERE id = ?
        """,
        (frozen, course_id),
    )

    utils.get_db().commit()


def remove_student_from_course(token, student_id, course_id):
    admin_id = utils.decode_to_jwt(token)["id"]
    cur = utils.get_db().cursor()

    check_admin_course_access(admin_id, course_id)

    check_valid_student(student_id)
    check_valid_course(course_id)

    cur.execute(
        """
        DELETE FROM enrolments WHERE user_id = ? AND course_id = ?
        """,
        (
            student_id,
            course_id,
        ),
    )

    utils.get_db().commit()


########################################################################
##                          Meeting Functions                         ##
########################################################################


def create_meeting(token, course_id, start_utc, duration_minutes, description):
    user_id = utils.decode_to_jwt(token)["id"]

    # TODO: check if the course exists
    # TODO: check if user_id is a course admin for that course

    cur = utils.get_db().cursor()

    # TODO
    # if not course_exists(course_id):
    #     raise InputError(f"course {course_id} doesn't exists")

    cur.execute(
        """
        INSERT INTO meetings (
            course_id,
            start_utc,
            duration_minutes,
            description
        )
        VALUES (?, ?, ?, ?)
        """,
        (course_id, start_utc, duration_minutes, description),
    )
    utils.get_db().commit()

    return cur.lastrowid


def edit_meeting(token, meeting_id, start_utc, duration_minutes, description):
    user_id = utils.decode_to_jwt(token)["id"]
    # check_user_edit_perms(user_id, student_id, course_id)

    cur = utils.get_db().cursor()

    cur.execute(
        """
        UPDATE meetings
        SET description = ?, start_utc = ?, duration_minutes = ?
        WHERE id = ? 
        """,
        (description, start_utc, duration_minutes, meeting_id),
    )
    utils.get_db().commit()
    return cur.lastrowid


def remove_meeting(token, course_id, meeting_id):
    user_id = utils.decode_to_jwt(token)["id"]

    cur = utils.get_db().cursor()

    cur.execute(
        """
        DELETE FROM meetings  
        WHERE id = ? AND course_id = ?
        """,
        (meeting_id, course_id),
    )
    utils.get_db().commit()


########################################################################
##                          Misc Functions                            ##
########################################################################


def create_course(token, name, slug):
    user_id = utils.decode_to_jwt(token)["id"]

    # TODO: check if user_id is a course admin or a sys admin

    cur = utils.get_db().cursor()
    try:
        cur.execute(
            """
            INSERT INTO courses (name, slug) VALUES (?, ?)
            """,
            (name, slug),
        )
    except sqlite3.IntegrityError:
        raise InputError("slug or name already used")
    utils.get_db().commit()

    return cur.lastrowid  # returns the course id


def create_team(token, name, course_id, leader_id):
    """ Returns the team id """
    id = utils.decode_to_jwt(token)["id"]

    utils.check_admin_course_access(id, course_id)
    utils.check_valid_course(course_id)
    utils.check_user_is_course_student(leader_id, course_id)

    # if utils.get_user_course_team(leader_id, course_id):
    #     raise MessageError("This student already belongs to a team")

    cur = utils.get_db().cursor()
    try:
        cur.execute(
            """
            INSERT INTO teams (name, course_id, leader_id) VALUES (?, ?, ?)
            """,
            (name, course_id, leader_id),
        )
    except sqlite3.IntegrityError as e:
        raise InputError("Name is already taken ({e})")
    team_id = cur.lastrowid

    cur.execute(
        """
        UPDATE enrolments
        SET team_id = ?
        WHERE user_id = ? AND course_id = ?
        """,
        (team_id, leader_id, course_id),
    )

    utils.get_db().commit()
    return team_id
