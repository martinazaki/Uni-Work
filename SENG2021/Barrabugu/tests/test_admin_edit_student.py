from test_helpers import client, create_test_user, create_test_course, send

from errors import *
import pytest
import utils


def test_admin_edit_student(client):
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

    # Add student 1 and 2 to course 1
    send(
        client,
        "/api/admin/import",
        json={
            "token": admin_token,
            "course_id": course_id1,
            "overwrite": False,
            "student_info": [
                {"name": "Jane Doe", "email": "jane@doe.com", "description": None},
                {"name": "Joe Bloggs", "email": "joe@bloggs.com", "description": None},
            ],
        },
    )

    # Add student 1 and 2 to course 2
    send(
        client,
        "/api/admin/import",
        json={
            "token": admin_token,
            "course_id": course_id2,
            "overwrite": False,
            "student_info": [
                {"name": "Jane Doe", "email": "jane@doe.com", "description": None},
                {"name": "Joe Bloggs", "email": "joe@bloggs.com", "description": None},
            ],
        },
    )

    # Edit student 1 in course 1
    send(
        client,
        "/api/admin/edit-student",
        json={
            "token": student_token1,
            "student_id": student_id1,
            "description": "Hello World!",
            "course_id": course_id1,
        },
    )

    # Fail to edit student 1 in course 1
    send(
        client,
        "/api/admin/edit-student",
        json={
            "token": student_token2,
            "student_id": student_id1,
            "description": "Goodbye World!",
            "course_id": course_id1,
        },
        expected_status_code=403,
        expected_response_type="access error",
    )

    # Edit student 2 as admin in course 1
    send(
        client,
        "/api/admin/edit-student",
        json={
            "token": admin_token,
            "student_id": student_id2,
            "description": "Hello Mars!",
            "course_id": course_id1,
        },
    )

    # Edit student 1 in course 2
    send(
        client,
        "/api/admin/edit-student",
        json={
            "token": student_token1,
            "student_id": student_id1,
            "description": "Goodbye Saturn!",
            "course_id": course_id2,
        },
    )

    # Check that all edits from above have affected course 1 correctly
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
        "2": {
            "description": "Hello World!",
            "email": "jane@doe.com",
            "name": "jane@doe.com",
        },
        "3": {
            "description": "Hello Mars!",
            "email": "joe@bloggs.com",
            "name": "joe@bloggs.com",
        },
    }

    # Check edits have not affected course 2

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
        "2": {
            "description": "Goodbye Saturn!",
            "email": "jane@doe.com",
            "name": "jane@doe.com",
        },
        "3": {"description": None, "email": "joe@bloggs.com", "name": "joe@bloggs.com"},
    }
