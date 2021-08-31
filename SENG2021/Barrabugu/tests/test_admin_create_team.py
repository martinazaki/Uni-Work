from test_helpers import (
    create_test_course,
    create_test_user,
    register_test_users,
    send,
    client,
)


def test_admin_create_team(client):
    admin_token = create_test_user(client, "admin", "admin")

    course_a_id = create_test_course(client, admin_token, "test", "test!")
    course_b_id = create_test_course(client, admin_token, "test b", "test b!!")

    student_id_a1, student_id_a2 = register_test_users(
        client, admin_token, ("foo", "bar"), course_a_id
    )
    student_id_b1, student_id_b2 = register_test_users(
        client, admin_token, ("baz", "yo"), course_b_id
    )

    # student a1 isn't in course b
    send(
        client,
        "/api/admin/create-team",
        json={
            "token": admin_token,
            "name": "3",
            "course_id": course_b_id,
            "leader_id": student_id_a1,
        },
        expected_status_code=403,
        expected_response_type="access error",
    )

    team_a_id = send(
        client,
        "/api/admin/create-team",
        json={
            "token": admin_token,
            "name": "2",
            "course_id": course_a_id,
            "leader_id": student_id_a1,
        },
    )["team_id"]

    team_b_id = send(
        client,
        "/api/admin/create-team",
        json={
            "token": admin_token,
            "name": "1",
            "course_id": course_b_id,
            "leader_id": student_id_b1,
        },
    )["team_id"]
    assert team_a_id != team_b_id
