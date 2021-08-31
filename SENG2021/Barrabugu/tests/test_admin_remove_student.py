from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    register_test_users,
    send,
)

from errors import *
import pytest
import utils


def test_admin_remove_student(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_id1 = utils.decode_to_jwt(student_token1)["id"]
    student_token2 = create_test_user(client, "joe@bloggs.com", "joebloggs123")
    student_id2 = utils.decode_to_jwt(student_token2)["id"]

    course_id1 = create_test_course(
        client, admin_token, "COMP1000", "Introduction to Test Data"
    )
    course_id2 = create_test_course(
        client, admin_token, "COMP1001", "Further Test Data"
    )

    register_test_users(
        client, admin_token, ["jane@doe.com", "joe@bloggs.com"], course_id1
    )
    register_test_users(
        client, admin_token, ["jane@doe.com", "joe@bloggs.com"], course_id2
    )

    # Remove student 1 from course 1
    send(
        client,
        "/api/admin/remove-student-from-course",
        json={"token": admin_token, "student_id": student_id1, "course_id": course_id1},
    )

    # Remove student 2 from course 2
    send(
        client,
        "/api/admin/remove-student-from-course",
        json={"token": admin_token, "student_id": student_id2, "course_id": course_id2},
    )

    # Check that student 1 has been removed from course 1
    assert send(
        client,
        "/api/students/teamless",
        params={
            "token": student_token2,
            "course_id": course_id1,
            "page": 1,
            "count": 10,
        },
    )["teamless"] == {
        "3": {"description": None, "email": "joe@bloggs.com", "name": "joe@bloggs.com"}
    }

    # Check student 2 has been removed from course 2
    assert send(
        client,
        "/api/students/teamless",
        params={
            "token": student_token1,
            "course_id": course_id2,
            "page": 1,
            "count": 10,
        },
    )["teamless"] == {
        "2": {"description": None, "email": "jane@doe.com", "name": "jane@doe.com"},
    }
