from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    create_test_team,
    register_test_users,
    send,
)

from errors import *
import pytest
import utils


def test_student_apply_team(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_token2 = create_test_user(client, "joe@bloggs.com", "joebloggs123")

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

    team1_id = create_test_team(client, student_token1, "Team1", course_id1)
    create_test_team(client, student_token1, "Team2", course_id2)

    send(
        client,
        "/api/students/apply",
        json={
            "token": student_token2,
            "team_id": team1_id,
            "course_id": course_id1,
        },
    )

    send(
        client,
        "/api/students/retract-application",
        json={
            "token": student_token2,
            "team_id": team1_id,
            "course_id": course_id1,
        },
    )

    send(
        client,
        "/api/students/retract-application",
        json={
            "token": student_token2,
            "team_id": team1_id,
            "course_id": course_id2,
        },
        expected_status_code=400,
        expected_response_type="input error",
    )

    send(
        client,
        "/api/students/retract-application",
        json={
            "token": student_token1,
            "team_id": team1_id,
            "course_id": course_id2,
        },
        expected_status_code=400,
        expected_response_type="input error",
    )

    send(
        client,
        "/api/students/apply",
        json={
            "token": student_token2,
            "team_id": team1_id,
            "course_id": course_id1,
        },
    )

    # TODO test that the user applications are not accidentally applying to both courses
