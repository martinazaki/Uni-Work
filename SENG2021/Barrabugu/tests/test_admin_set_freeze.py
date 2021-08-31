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


def test_admin_set_freeze(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_id1 = utils.decode_to_jwt(student_token1)["id"]
    student_token2 = create_test_user(client, "joe@bloggs.com", "joebloggs123")
    student_id2 = utils.decode_to_jwt(student_token2)["id"]

    course_id1 = create_test_course(
        client, admin_token, "COMP1000", "Introduction to Test Data"
    )

    register_test_users(
        client, admin_token, ["jane@doe.com", "joe@bloggs.com"], course_id1
    )

    team1_id = create_test_team(client, student_token1, "Team1", course_id1)
    team2_id = create_test_team(client, student_token2, "Team2", course_id1)

    send(
        client,
        "/api/admin/set-freeze",
        json={"token": admin_token, "frozen": True, "course_id": course_id1},
    )
