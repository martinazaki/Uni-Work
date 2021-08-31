from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    register_test_users,
    create_test_team,
    send,
)

from errors import *
import pytest
import utils


def test_admin_move_student(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_id1 = utils.decode_to_jwt(student_token1)["id"]
    student_token2 = create_test_user(client, "joe@bloggs.com", "joebloggs123")
    student_id2 = utils.decode_to_jwt(student_token2)["id"]
    student_token3 = create_test_user(client, "joey@bloggs.com", "joeybloggs123")
    student_id3 = utils.decode_to_jwt(student_token3)["id"]

    course_id1 = create_test_course(
        client, admin_token, "COMP1000", "Introduction to Test Data"
    )
    course_id2 = create_test_course(
        client, admin_token, "COMP1001", "Further Test Data"
    )

    register_test_users(
        client,
        admin_token,
        ["jane@doe.com", "joe@bloggs.com", "joey@bloggs.com"],
        course_id1,
    )
    register_test_users(
        client, admin_token, ["jane@doe.com", "joe@bloggs.com"], course_id2
    )

    team1_id = create_test_team(client, student_token1, "Team1", course_id1)
    team2_id = create_test_team(client, student_token3, "Team2", course_id1)
    team3_id = create_test_team(client, student_token2, "Team3", course_id2)

    # Move student1 to Team2
    send(
        client,
        "/api/admin/move",
        json={
            "token": admin_token,
            "course_id": course_id1,
            "source_team_id": team1_id,
            "dest_team_id": team2_id,
            "student_id": student_id1,
        },
    )

    # Fail Move student1 to Team3
    send(
        client,
        "/api/admin/move",
        json={
            "token": admin_token,
            "course_id": course_id1,
            "source_team_id": team2_id,
            "dest_team_id": team3_id,
            "student_id": student_id1,
        },
        expected_status_code=400,
        expected_response_type="input error",
    )

    # Check that all students are in teams
    assert send(
        client,
        "/api/students/teamless",
        params={
            "token": student_token1,
            "course_id": course_id1,
            "page": 1,
            "count": 10,
        },
    )["teamless"] == {
        "3": {"description": None, "email": "joe@bloggs.com", "name": "joe@bloggs.com"}
    }

    # Check student 1 is now in team 2
    assert send(
        client,
        "api/students/teams",
        params={"token": admin_token, "course_id": course_id1, "page": 1, "count": 10},
    )["teams"] == {
        str(team2_id): {
            "leader_id": student_id3,
            "members": {
                str(student_id1): {
                    "description": None,
                    "email": "jane@doe.com",
                    "name": "jane@doe.com",
                },
                str(student_id3): {
                    "description": None,
                    "email": "joey@bloggs.com",
                    "name": "joey@bloggs.com",
                },
            },
            "name": "Team2",
        }
    }
