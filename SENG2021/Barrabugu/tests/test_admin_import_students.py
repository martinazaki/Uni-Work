from test_helpers import client, create_test_user, create_test_course, send

from errors import *
import pytest
import utils


def test_admin_import_students(client):
    admin_token = create_test_user(client, "john@doe.com", "johndoe123")

    course_id = create_test_course(
        client, admin_token, "COMP1000", "Introduction to Test Data"
    )

    student_token1 = create_test_user(client, "jane@doe.com", "janedoe123")
    student_id1 = utils.decode_to_jwt(student_token1)["id"]

    send(
        client,
        "/api/admin/import",
        json={
            "token": admin_token,
            "course_id": course_id,
            "overwrite": False,
            "student_info": [
                {"name": "Jane Doe", "email": "jane@doe.com", "description": None},
                {"name": "Joe Bloggs", "email": "joe@bloggs.com", "description": None},
            ],
        },
    )

    assert send(
        client,
        "/api/students/teamless",
        params={"token": admin_token, "course_id": course_id, "page": 1, "count": 10},
    )["teamless"] == {
        "2": {"description": None, "email": "jane@doe.com", "name": "jane@doe.com"},
        "3": {"description": None, "email": "joe@bloggs.com", "name": "Joe Bloggs"},
    }
