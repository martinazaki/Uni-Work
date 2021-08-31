import pytest

from test_helpers import (
    client,
    create_test_user,
    create_test_course,
    create_test_team,
    create_test_meeting,
    send,
)


def test_admin_remove_meetings(client):
    admin_token = create_test_user(client, "admin@gmail.com", "adminpass")

    course_ids = []
    meeting_ids = []

    course = create_test_course(
        client, admin_token, "SUBJ101", "Introduction To Subjects"
    )

    meet = create_test_meeting(
        client, admin_token, course, "2021-04-16 5:00:18+00:00", 27, "test meeting"
    )

    course_ids.append(course)
    meeting_ids.append(meet)

    meetings_to_be_removed = [
        {
            "course_id": course_ids[0],
            "meeting_id": meeting_ids[0],
        },
    ]

    # Removing the meeting
    for meeting in meetings_to_be_removed:
        send(
            client,
            "/api/admin/remove-meeting",
            json={
                "token": admin_token,
                "course_id": meeting["course_id"],
                "meeting_id": meeting["meeting_id"],
            },
        )

    # Check meeting is removed
    send(
        client,
        "/api/students/list-meetings",
        params={
            "token": admin_token,
            "course_id": course,
        },
    )["meetings"] == {
        "course_id": "SUBJ101",
    }
