import utils
import sqlite3 as sql
from errors import *
from utils import *


########################################################################
##                       Team Movement Functions                      ##
########################################################################


def create_team(token, team_name, course_id):
    user_id = utils.decode_to_jwt(token)["id"]

    cur = utils.get_db().cursor()

    # TODO check user is not already the leader of another team
    # TODO admin/sysadmin creating team doesn't insert them as leader

    check_user_course_access(user_id, course_id)

    cur.execute(
        """
        INSERT INTO teams (name, leader_id, course_id) 
        VALUES (?, ?, ?)
        """,
        (
            team_name,
            user_id,
            course_id,
        ),
    )
    utils.get_db().commit()

    team_id = cur.lastrowid

    cur.execute(
        """
        UPDATE enrolments
        SET team_id = ?
        WHERE user_id = ? AND
              course_id = ?
        """,
        (team_id, user_id, course_id),
    )
    utils.get_db().commit()

    return team_id


def apply(token, team_id, course_id):
    # TODO endpoint to retract application
    user_id = utils.decode_to_jwt(token)["id"]

    check_user_is_course_student(user_id, course_id)

    cur = utils.get_db().cursor()

    # Check if already applied to team

    if get_user_course_team(user_id, course_id) != None:
        raise InputError("Leave your current team before applying for a new one!")

    # Check if already applied to tea

    if has_user_already_applied(user_id, team_id):
        raise InputError("You have already applied to this team!")

    cur.execute(
        """
        INSERT INTO applications
        (target_team_id, from_student_id, seen) 
        VALUES (?, ?, ?)
        """,
        (team_id, user_id, False),
    )
    utils.get_db().commit()


def apply(token, team_id, course_id):
    # TODO endpoint to retract application
    user_id = utils.decode_to_jwt(token)["id"]

    check_user_is_course_student(user_id, course_id)

    cur = utils.get_db().cursor()

    # Check if already applied to team

    if get_user_course_team(user_id, course_id) != None:
        raise InputError("Leave your current team before applying for a new one!")

    # Check if already applied to tea

    if has_user_already_applied(user_id, team_id):
        raise InputError("You have already applied to this team!")

    cur.execute(
        """
        INSERT INTO applications
        (target_team_id, from_student_id, seen) 
        VALUES (?, ?, ?)
        """,
        (team_id, user_id, False),
    )
    utils.get_db().commit()


def retract_application(token, team_id, course_id):
    # TODO endpoint to retract application
    user_id = utils.decode_to_jwt(token)["id"]

    check_user_is_course_student(user_id, course_id)

    cur = utils.get_db().cursor()

    # Check if user has filed an application for this team

    if not has_user_already_applied(user_id, team_id):
        raise InputError("You cannot retract an application if you haven't applied!")

    # TODO add limit 1 in all applicable cases across the code
    cur.execute(
        """
        DELETE FROM applications
        WHERE target_team_id = ?
        AND from_student_id = ?
        """,
        (
            team_id,
            user_id,
        ),
    )
    utils.get_db().commit()


def accept(token, student_id, course_id):
    pass


def invite(token, student_email, course_id):
    pass


def leave(token, team_id, course_id):
    pass


# TODO Move admin edit into this
def edit_description(token, student_id, description):
    pass


########################################################################
##                    Team Organisation Functions                     ##
########################################################################


##
# RETURNED JSON FORMAT
# {
#     <student.id>: {"name" : "foo",
#                    "description" : "foobar",
#                    "email" : "bar"}, ...
# }
##
def teamless(token, course_id, page, count):
    # TODO Pagination
    user_id = utils.decode_to_jwt(token)["id"]

    cur = utils.get_db().cursor()

    utils.check_user_course_access(user_id, course_id)

    cur.execute(
        """
         SELECT user_id, name, description, email
         FROM enrolments
         JOIN users ON users.id = enrolments.user_id
         WHERE course_id = ?
         AND team_id IS NULL
         ORDER BY
         user_id ASC
        """,
        # JOIN teams ON teams.id = students.team_id
        (course_id,),
    )

    # TODO Add student to teams in test
    # TODO Properly get team name in query
    teamless = {}
    for row in cur.fetchall():
        teamless[row[0]] = {
            "name": row[1],
            "description": row[2],
            "email": row[3],
        }

    return teamless


##
# RETURNED JSON FORMAT
# {<teamid>: {
#             "name" : "Barrabugu",
#             "members" : {
#                         <student.id> : {"name" : "John Doe",
#                                         "description" : "foobar",
#                                         "email" : "john@doe.com.au"}, ...
#                        },
#             "leader_id" : 1
#            }, ...
# }
##
def teams(token, course_id, page, count):
    # TODO Pagination
    user_id = utils.decode_to_jwt(token)["id"]

    cur = utils.get_db().cursor()

    utils.check_user_course_access(user_id, course_id)

    cur.execute(
        """
         SELECT teams.id AS team_id, teams.name AS team_name, leader_id, user_id, users.name AS user_name, description, email
         FROM enrolments
         JOIN teams ON teams.id = enrolments.team_id
         JOIN users ON users.id = enrolments.user_id
         WHERE enrolments.course_id = ?
         AND team_id IS NOT NULL
         ORDER BY
         team_id ASC
        """,
        (course_id,),
    )

    teams = {}
    for row in cur.fetchall():
        if row[0] not in teams:
            teams[row[0]] = {}
            teams[row[0]]["name"] = row[1]
            teams[row[0]]["members"] = {}
            teams[row[0]]["leader_id"] = row[2]

        teams[row[0]]["members"][row[3]] = {
            "name": row[4],
            "description": row[5],
            "email": row[6],
        }

    return teams


def filter_teams(token, team_name, pattern):
    pass


########################################################################
##                          Meeting Functions                         ##
########################################################################


def rank_meetings(token, student_id, meeting_ranks):
    pass


def list_meetings(token, course_id):
    """
    {
        <meeting id>: {
            "id": <meeting id>,
            "start_utc": string datetime,
            "duration_minutes": int,
            "description": string,
        }
    }
    """
    user_id = utils.decode_to_jwt(token)["id"]

    # TODO: check if user_id is a valid user id AND he is enroled in course id

    cur = utils.get_db().cursor()

    cur.execute(
        """
        SELECT id, start_utc, duration_minutes, description
        FROM meetings
        WHERE course_id=?
        """,
        (course_id,),
    )

    meetings = []
    for row in cur.fetchall():
        meetings.append(
            {
                "id": row[0],
                "start_utc": row[1],
                "duration_minutes": row[2],
                "description": row[3],
            }
        )

    return meetings
