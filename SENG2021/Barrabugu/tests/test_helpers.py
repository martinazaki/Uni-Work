import tempfile
import pytest
import db

# some fancy magic because Matthew really wants the server to be in the root folder
import sys, os

sys.path.append(os.path.dirname(__file__))

# now we can import server.py
import server


@pytest.fixture
def client():
    fd, server.app.config["DATABASE"] = tempfile.mkstemp()
    with server.app.test_client() as client:
        with server.app.app_context():
            db.initialize()
        yield client

    os.close(fd)
    os.unlink(server.app.config["DATABASE"])  # remove the file


def send(
    client, *args, expected_status_code=200, expected_response_type="success", **kwargs
):
    """
    Sends a request and makes sure we get a 200 response, with body['type'] == 'success'.
    if 'json' is specified, then a post request is sent.
    if 'params' is specified, then a get request is sent.
    """

    if "json" in kwargs and "params" in kwargs:
        raise ValueError(
            "can't have both json and params, don't know which method to use"
        )

    if "json" in kwargs:
        method = "POST"
    elif "params" in kwargs:
        method = "GET"
        # behave like requests!
        kwargs["query_string"] = kwargs["params"]
        del kwargs["params"]
    elif "query_string" in kwargs:
        method = "GET"

    response = client.open(*args, method=method, **kwargs)

    assert (
        response.status_code == expected_status_code
    ), f"wrong status code, got {response.status_code} not {expected_status_code} ({response.json})"

    body = response.json

    assert (
        body["type"] == expected_response_type
    ), f"wrong status type, got {body['type']}, not {expected_response_type}"

    return body


def create_test_user(client, email, password):
    return send(
        client,
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "name": email,
        },
    )["token"]


def create_test_course(client, admin_token, slug, name):
    return send(
        client,
        "/api/admin/create-course",
        json={
            "token": admin_token,
            "slug": slug,
            "name": name,
        },
    )["course_id"]


def create_test_meeting(
    client, admin_token, course_id, start_utc, duration_minutes, description
):
    return send(
        client,
        "/api/admin/create-meeting",
        json={
            "token": admin_token,
            "course_id": course_id,
            "start_utc": start_utc,
            "duration_minutes": duration_minutes,
            "description": description,
        },
    )["meeting_id"]


def register_test_users(client, admin_token, student_emails, course_id):
    """ Returns the list of user id that were imported """
    users_to_register = []
    for email in student_emails:
        users_to_register.append({"name": email, "email": email, "description": None})

    # Add student 1 and 2 to course 1
    return send(
        client,
        "/api/admin/import",
        json={
            "token": admin_token,
            "course_id": course_id,
            "overwrite": False,
            "student_info": users_to_register,
        },
    )["user_ids"]


def create_test_team(client, token, team_name, course_id):
    return send(
        client,
        "/api/students/create-team",
        json={
            "token": token,
            "team_name": team_name,
            "course_id": course_id,
        },
    )["team_id"]
