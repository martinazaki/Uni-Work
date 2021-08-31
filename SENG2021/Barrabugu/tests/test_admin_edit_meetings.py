import pytest

from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    create_test_team,
    create_test_meeting,
    send,
)


def test_admin_edit_meetings(client):
    admin_token = create_test_user(client, "admin@gmail.com", "adminpass")

    course_ids = []
    meeting_ids = []

    course = create_test_course(
        client, admin_token, "SUBJ101", "Introduction To Subjects"
    )

    meet = create_test_meeting(
        client, admin_token, course, "2021-04-16 5:00:18+00:00", 27, "test meeting"
    )

    meeting_ids.append(meet)

    meetings_to_be_edited = [
        {
            "meeting_id": meeting_ids[0],
            "start_utc": "2021-04-15 23:40:18+00:00",
            "duration_minutes": 15,
            "description": "first meeting course 0",
        },
    ]

    # Edit meeting
    for meeting in meetings_to_be_edited:
        send(
            client,
            "/api/admin/edit-meeting",
            json={
                "token": admin_token,
                "meeting_id": meeting["meeting_id"],
                "start_utc": meeting["start_utc"],
                "duration_minutes": meeting["duration_minutes"],
                "description": meeting["description"],
            },
        )

    # Check meeting has been edited
    send(
        client,
        "/api/students/list-meetings",
        params={
            "token": admin_token,
            "course_id": course,
        },
    )["meetings"] == {
        "2": {
            "course_id": "SUBJ101",
            "start_utc": "2021-04-15 23:40:16+00:00",
            "duration_minutes": 14,
            "description": "Primary meeting",
        },
        "3": {
            "course_id": "SUBJ101",
            "start_utc": "2021-04-15 23:40:18+00:00",
            "duration_minutes": 18,
            "description": "Secondary meeting",
        },
    }
