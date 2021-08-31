import os.path
import flask
from errors import *
import db

import admin
import auth
import students
import sysadmin

app = flask.Flask(__name__)
app.config.from_mapping(DATABASE="database.db")


########################################################################
##                            Auth Routing                            ##
########################################################################


@app.route("/api/auth/register", methods=["POST"])
def auth_register_handler():
    email, password, name = get_fields_from_body(email=str, password=str, name=str)
    token = auth.register(email, password, name)
    return {
        "type": "success",
        "token": token,
        "redirect_to": "student.html",
    }


@app.route("/api/auth/login", methods=["POST"])
def auth_login_handler():
    email, password = get_fields_from_body(email=str, password=str)
    token = auth.login(email, password)
    return {
        "type": "success",
        "token": token,
        "redirect_to": "student.html",
    }


########################################################################
##                           Admin Routing                            ##
########################################################################


####################  Student Interaction Functions  ###################


@app.route("/api/admin/move", methods=["POST"])
def admin_move():
    token, course_id, source_team_id, dest_team_id, student_id = get_fields_from_body(
        token=str,
        course_id=int,
        source_team_id=int,
        dest_team_id=int,
        student_id=int,
    )

    info = admin.move(token, course_id, source_team_id, dest_team_id, student_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/admin/create-team", methods=["POST"])
def admin_create_team_handler():
    token, name, course_id, leader_id = get_fields_from_body(
        token=str, name=str, course_id=int, leader_id=int
    )
    team_id = admin.create_team(token, name, course_id, leader_id)
    return {
        "type": "success",
        "team_id": team_id,
    }


@app.route("/api/admin/edit-student", methods=["POST"])
def admin_edit_student():
    token, student_id, description, course_id = get_fields_from_body(
        token=str,
        student_id=int,
        description=str,
        course_id=int,
    )

    admin.edit_student(token, student_id, description, course_id)

    return {"type": "success"}


@app.route("/api/admin/set-freeze", methods=["POST"])
def admin_set_freeze():
    token, frozen, course_id = get_fields_from_body(
        token=str,
        frozen=bool,
        course_id=int,
    )

    admin.set_freeze(token, frozen, course_id)
    return {
        "type": "success",
    }


###################  Course Administration Functions  ##################


@app.route("/api/admin/import", methods=["POST"])
def admin_import():
    token, course_id, overwrite, student_info = get_fields_from_body(
        token=str,
        course_id=int,
        overwrite=bool,
        student_info=list,
    )

    user_ids = admin.import_students(token, course_id, overwrite, student_info)

    return {
        "type": "success",
        "user_ids": user_ids,
    }


@app.route("/api/admin/organise-teamless", methods=["POST"])
def admin_organise_teamless():
    token, course_id = get_fields_from_body(
        token=str,
        course_id=int,
    )

    info = admin.oragnise_teamless(token, course_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/admin/remove-student-from-course", methods=["POST"])
def admin_remove_student_from_course():
    token, student_id, course_id = get_fields_from_body(
        token=str,
        student_id=int,
        course_id=int,
    )

    info = admin.remove_student_from_course(token, student_id, course_id)

    return {
        "type": "success",
        "info": info,
    }


#########################  Meeting Functions  ##########################


@app.route("/api/admin/create-meeting", methods=["POST"])
def admin_create_meeting_handler():
    token, course_id, start_utc, duration_minutes, description = get_fields_from_body(
        token=str,
        course_id=int,
        start_utc=str,
        duration_minutes=int,
        description=str,
    )

    meeting_id = admin.create_meeting(
        token,
        course_id,
        start_utc,
        duration_minutes,
        description,
    )
    return {
        "type": "success",
        "meeting_id": meeting_id,
    }


@app.route("/api/admin/edit-meeting", methods=["POST"])
def admin_edit_meeting():
    token, meeting_id, start_utc, duration_minutes, description = get_fields_from_body(
        token=str,
        meeting_id=int,
        start_utc=str,
        duration_minutes=int,
        description=str,
    )

    info = admin.edit_meeting(
        token, meeting_id, start_utc, duration_minutes, description
    )

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/admin/remove-meeting", methods=["POST"])
def admin_remove_meeting():
    token, course_id, meeting_id = get_fields_from_body(
        token=str,
        course_id=int,
        meeting_id=int,
    )

    info = admin.remove_meeting(token, course_id, meeting_id)

    return {
        "type": "success",
        "info": info,
    }


###########################  Misc Functions  ###########################


@app.route("/api/admin/create-course", methods=["POST"])
def admin_create_course():
    token, name, slug = get_fields_from_body(
        token=str,
        name=str,
        slug=str,
    )

    course_id = admin.create_course(token, name, slug)

    return {
        "type": "success",
        "course_id": course_id,
    }


########################################################################
##                          Student Routing                           ##
########################################################################


#######################  Team Movement Functions  ######################


@app.route("/api/students/create-team", methods=["POST"])
def students_create_team():
    token, team_name, course_id = get_fields_from_body(
        token=str,
        team_name=str,
        course_id=int,
    )

    team_id = students.create_team(token, team_name, course_id)

    return {
        "type": "success",
        "team_id": team_id,
    }


@app.route("/api/students/apply", methods=["POST"])
def students_apply():
    token, team_id, course_id = get_fields_from_body(
        token=str,
        team_id=int,
        course_id=int,
    )

    info = students.apply(token, team_id, course_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/retract-application", methods=["POST"])
def students_retract_application():
    token, team_id, course_id = get_fields_from_body(
        token=str,
        team_id=int,
        course_id=int,
    )

    info = students.retract_application(token, team_id, course_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/accept", methods=["POST"])
def students_accept():
    token, student_id, course_id = get_fields_from_body(
        token=str,
        student_id=int,
        course_id=int,
    )

    info = students.accept(token, student_id, course_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/invite", methods=["POST"])
def students_invite():
    token, student_email, course_id = get_fields_from_body(
        token=str,
        student_email=str,
        course_id=int,
    )
    info = students.invite(token, student_email, course_id)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/leave", methods=["POST"])
def students_leave():
    token, team_id, course_id = get_fields_from_body(
        token=str,
        team_id=int,
        course_id=int,
    )
    info = students.leave(token, team_id, course_id)
    return {
        "type": "success",
        "info": info,
    }


#####################  Team Organisation Functions  ####################


@app.route("/api/students/teamless", methods=["GET"])
def students_teamless():
    token, course_id, page, count = get_fields_from_body(
        token=str,
        course_id=int,
        page=int,
        count=int,
    )
    teamless = students.teamless(token, course_id, page, count)

    return {
        "type": "success",
        "teamless": teamless,
    }


@app.route("/api/students/teams", methods=["GET"])
def students_teams():
    token, course_id, page, count = get_fields_from_body(
        token=str,
        course_id=int,
        page=int,
        count=int,
    )

    teams = students.teams(token, course_id, page, count)

    return {
        "type": "success",
        "teams": teams,
    }


@app.route("/api/students/filter-teams", methods=["GET"])
def students_filter_teams():
    token, team_name, pattern = get_fields_from_body(
        token=str,
        team_name=str,
        pattern=str,
    )

    info = students.filter_teams(token, team_name, pattern)

    return {
        "type": "success",
        "info": info,
    }


#########################  Meeting Functions  ##########################


@app.route("/api/students/edit-description", methods=["POST"])
def students_edit_description():
    token, student_id, description = get_fields_from_body(
        token=str,
        student_id=int,
        description=str,
    )

    info = students.edit_description(token, student_id, description)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/rank-meetings", methods=["POST"])
def students_rank_meetings():
    token, student_id, meeting_ranks = get_fields_from_body(
        token=str,
        student_id=int,
        meeting_ranks=dict,
    )

    info = students.rank_meetings(token, student_id, meeting_ranks)

    return {
        "type": "success",
        "info": info,
    }


@app.route("/api/students/list-meetings", methods=["GET"])
def students_list_meetings():
    token, course_id = get_fields_from_body(
        token=str,
        course_id=int,
    )

    meetings = students.list_meetings(token, course_id)

    return {
        "type": "success",
        "meetings": meetings,
    }


########################################################################
##                          Sysadmin Routing                          ##
########################################################################


@app.route("/api/sysadmin/delete-student", methods=["POST"])
def admin_delete_student():
    token, student_id = get_fields_from_body(
        token=str,
        student_id=int,
    )

    admin.delete_student(token, student_id)

    return {
        "type": "success",
    }


@app.route("/api/sysadmin/student-to-course-admin", methods=["POST"])
def sys_admin_student_convert():
    token, student_id, course_id = get_fields_from_body(
        token=str,
        student_id=int,
        course_id=int,
    )
    # TODO check token

    status = sysadmin.convert_student_to_course_admin(token, student_id, course_id)

    return status


########################################################################
##                            Misc Routing                            ##
########################################################################


@app.errorhandler(InputError)
def error_handler_input(e):
    return (
        flask.jsonify(type="input error", error=InputError.code, text=e.description),
        InputError.code,
    )


@app.errorhandler(AccessError)
def error_handler_access(e):
    return (
        flask.jsonify(type="access error", error=AccessError.code, text=e.description),
        AccessError.code,
    )


@app.errorhandler(500)
def error_handler_internal(e):
    return flask.jsonify(type="internal error", error=500, text=str(e)), 500


def get_fields_from_body(**fields_type):
    """
    foo, bar = get_fields_from_body(foo=str, bar=list)

    foo # guaranted to be a string
    bar # guaranted to be a list

    The order of the argument must match the order of the variables on LHS.
    """

    if flask.request.method == "GET":
        body = dict(flask.request.args)
    elif flask.request.method == "POST":
        if not flask.request.is_json:
            raise InputError("expect JSON response")
        body = flask.request.get_json()
    else:
        raise InputError(f"invalid method {flask.request.method}")

    if type(body) != dict:
        raise InputError(f"any JSON body should be an object (dict), got {type(body)}")

    for field_name, field_type in fields_type.items():
        if field_name not in body:
            raise InputError(f"field name {field_name!r} missing from body")

        if type(field_type) != type:
            raise ValueError(
                f"You, the developer, made a mistake. {field_type} isn't a type. "
                f"A type is something like str or int for example."
                f"Feel free to message Mathieu if you want some help"
            )

        if flask.request.method == "GET":
            if field_type == bool:
                if body[field_name] in ("true", "True", "TRUE"):
                    body[field_name] = True
                elif body[field_name] in ("false", "False", "FALSE"):
                    body[field_name] = False
                else:
                    raise InputError(
                        f"Field {field_name!r} should be a boolean, got {body[field_name]!r}"
                    )
            elif field_type == int:
                try:
                    body[field_name] = int(body[field_name])
                except ValueError as e:
                    raise InputError(
                        f"Field {field_name!r} should be an int, got {body[field_name]!r}"
                    )
            elif field_type != str:
                raise ValueError(
                    f"You, the developer, made a mistake. On a GET request, the only accepted"
                    f"field types are (bool, int, str)"
                )
        else:
            if type(body[field_name]) != field_type:
                raise InputError(
                    f"field {field_name!r} is of wrong type, expected {field_type}, got {type(body[field_name])}"
                )

        yield body[field_name]

    # if you find a parameter that isn't required, raise an error
    for key in body:
        if key not in fields_type:
            raise InputError(f"invalid parameter: {key} is unused")


@app.route("/<path:path>")
def static_serve(path):
    # works for any bloddy damn folder name BUT static. wtf flask
    return flask.send_from_directory("client", path)


@app.route("/")
def index():
    return flask.redirect("login.html")


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(flask.g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    if not os.path.exists(app.config["DATABASE"]):
        with app.app_context():
            db.initialize()

    app.run("0.0.0.0", 3001)
