import pytest
from test_helpers import client, send, create_test_user, create_test_course


def test_admin_create_and_list_meetings(client):
    admin_token = create_test_user(client, "foqwero", "bar")

    course_ids = []
    course_ids.append(
        create_test_course(client, admin_token, "test-course", "Test course")
    )
    course_ids.append(
        create_test_course(
            client, admin_token, "test-course-second", "Test course second!"
        )
    )

    sent_meetings = [
        {
            "course_id": course_ids[0],
            "start_utc": "2021-04-15 23:40:18+00:00",
            "duration_minutes": 20,
            "description": "first meeting course 0",
        },
        {
            "course_id": course_ids[0],
            "start_utc": "2021-04-15 00:00:18+00:00",
            "duration_minutes": 20,
            "description": "second meeting course 0",
        },
        {
            "course_id": course_ids[1],
            "start_utc": "2021-04-16 5:00:18+00:00",
            "duration_minutes": 20,
            "description": "first meeting course 1",
        },
        {
            "course_id": course_ids[1],
            "start_utc": "2021-04-16 5:20:18+00:00",
            "duration_minutes": 20,
            "description": "second meeting course 1",
        },
    ]

    for meeting in sent_meetings:
        meeting_id = send(
            client,
            "/api/admin/create-meeting",
            json={
                "token": admin_token,
                "course_id": meeting["course_id"],
                "start_utc": meeting["start_utc"],
                "duration_minutes": meeting["duration_minutes"],
                "description": meeting["description"],
            },
        )["meeting_id"]

    # I doubt this is great style, but it works
    def recieve_meetings_from(course_id):
        recieved_meetings = send(
            client,
            "/api/students/list-meetings",
            params={
                "course_id": course_id,
                "token": admin_token,
            },
        )["meetings"]

        for meeting in recieved_meetings:
            # massage so that the recieved meetings look the same
            del meeting["id"]
            meeting["course_id"] = course_id

            assert meeting in sent_meetings, "got back a meeting that was never created"
            sent_meetings.remove(meeting)

    recieve_meetings_from(course_ids[0])
    recieve_meetings_from(course_ids[1])

    assert len(sent_meetings) == 0, "some courses that were created weren't listed"
