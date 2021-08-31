import db
import utils
import sqlite3
from errors import *


def convert_student_to_course_admin(token, student_id, course_id):
    cur = utils.get_db().cursor()

    if not utils.decode_to_jwt(token)["is_sys_admin"]:
        raise AccessError("must be sys admin")

    # Promote user to
    cur.execute(
        """
        INSERT INTO course_admins (user_id, course_id)
        VALUES (?, ?);
        """,
        (
            student_id,
            course_id,
        ),
    )

    cur.execute(
        """
        DELETE FROM students WHERE student_id
        IN (?)
        """,
        (student_id,),
    )

    utils.get_db().commit()

    return {
        "type": "success",
    }


def delete_student(token, student_id):
    cur = utils.get_db().cursor()
    auth_admin(token)
    check_valid_student(student_id)

    # Execute Operation
    cur.execute(
        """
        DELETE FROM users WHERE id = %d
        """,
        (student_id),
    )

    utils.get_db().commit()
