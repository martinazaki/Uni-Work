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


def test_student_create_team(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_id1 = utils.decode_to_jwt(student_token1)["id"]

    course_id1 = create_test_course(
        client, admin_token, "COMP1000", "Introduction to Test Data"
    )
    course_id2 = create_test_course(
        client, admin_token, "COMP1001", "Further Test Data"
    )

    register_test_users(client, admin_token, ["jane@doe.com"], course_id1)
    register_test_users(client, admin_token, ["jane@doe.com"], course_id2)

    # Create a course 1 team for student 1
    send(
        client,
        "/api/students/create-team",
        json={
            "token": student_token1,
            "team_name": "Barrabugu",
            "course_id": course_id1,
        },
    )

    # Create a course 2 team for student 1
    send(
        client,
        "/api/students/create-team",
        json={
            "token": student_token1,
            "team_name": "Barrabugu 2.0",
            "course_id": course_id2,
        },
    )

    assert send(
        client,
        "/api/students/teams",
        params={
            "token": student_token1,
            "course_id": course_id1,
            "page": 1,
            "count": 10,
        },
    )["teams"] == {
        "1": {
            "leader_id": 2,
            "members": {
                "2": {
                    "description": None,
                    "email": "jane@doe.com",
                    "name": "jane@doe.com",
                }
            },
            "name": "Barrabugu",
        }
    }

    assert send(
        client,
        "/api/students/teams",
        params={
            "token": student_token1,
            "course_id": course_id2,
            "page": 1,
            "count": 10,
        },
    )["teams"] == {
        "2": {
            "leader_id": 2,
            "members": {
                "2": {
                    "description": None,
                    "email": "jane@doe.com",
                    "name": "jane@doe.com",
                }
            },
            "name": "Barrabugu 2.0",
        }
    }
