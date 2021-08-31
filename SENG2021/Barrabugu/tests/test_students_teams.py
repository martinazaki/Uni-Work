from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    create_test_team,
    send,
    register_test_users,
)

from errors import *
import pytest
import utils


def test_students_teams(client):
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
    register_test_users(client, admin_token, ["joe@bloggs.com"], course_id2)

    team1_id = create_test_team(client, student_token1, "Team1", course_id1)
    team2_id = create_test_team(client, student_token2, "Team2", course_id1)
    team3_id = create_test_team(client, student_token2, "Team3", course_id2)

    # Add student 1 and 2 to course

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
        str(team1_id): {
            "leader_id": student_id1,
            "members": {
                str(student_id1): {
                    "description": None,
                    "email": "jane@doe.com",
                    "name": "jane@doe.com",
                }
            },
            "name": "Team1",
        },
        str(team2_id): {
            "leader_id": student_id2,
            "members": {
                str(student_id2): {
                    "description": None,
                    "email": "joe@bloggs.com",
                    "name": "joe@bloggs.com",
                }
            },
            "name": "Team2",
        },
    }

    assert (
        send(
            client,
            "/api/students/teamless",
            params={
                "token": student_token1,
                "course_id": course_id1,
                "page": 1,
                "count": 10,
            },
        )["teamless"]
        == {}
    )

    send(
        client,
        "/api/students/teams",
        params={
            "token": student_token1,
            "course_id": course_id2,
            "page": 1,
            "count": 10,
        },
        expected_status_code=403,
        expected_response_type="access error",
    )

    send(
        client,
        "/api/students/teamless",
        params={
            "token": student_token1,
            "course_id": course_id2,
            "page": 1,
            "count": 10,
        },
        expected_status_code=403,
        expected_response_type="access error",
    )

    # Assert teams and teamless for course 2
    assert send(
        client,
        "/api/students/teams",
        params={
            "token": student_token2,
            "course_id": course_id2,
            "page": 1,
            "count": 10,
        },
    )["teams"] == {
        str(team3_id): {
            "leader_id": student_id2,
            "members": {
                str(student_id2): {
                    "description": None,
                    "email": "joe@bloggs.com",
                    "name": "joe@bloggs.com",
                }
            },
            "name": "Team3",
        }
    }

    assert (
        send(
            client,
            "/api/students/teamless",
            params={
                "token": student_token2,
                "course_id": course_id2,
                "page": 1,
                "count": 10,
            },
        )["teamless"]
        == {}
    )
