''' Chaos Coding Server, April 2020'''

# Python libraries
import os
import json
import threading
from flask import Flask, request
from flask_cors import CORS

# Files from project
import auth
import user
import database
import channel as ch
import channels as chs
import message as msg
import standup as st
from workspace_admin import workspace_reset, admin_userpermissions_change
from search import search
from server_helpers import save

def defaultHandler(err):
    """Defult handler function."""

    response = err.get_response()
    print('response', err, err.get_response())
    response.data = json.dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Check if server has been opened before by checking if server_data.json has been created
if os.path.exists('server_data.json'):
    DATA = json.load(open('server_data.json', 'r'))
    database.update_database(DATA)

# Interval duration in seconds.
INTERVAL = 10


def interval_persistence():
    """Intveral persistence function."""

    threading.Timer(INTERVAL, interval_persistence).start()
    save()


@APP.route('/data/getall', methods=['GET'])
def get_all():
    """Flask for data get all function."""

    # Dev showing all data
    return json.dumps({
        'data': json.load(open('server_data.json', 'r'))
    })

#............................. AUTH .............................#
# auth_register
@APP.route("/auth/register", methods=["POST"])
def auth_register_flask():
    """Flask for auth register function; registers a user."""

    data = request.get_json()

    email = data["email"]
    password = data["password"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    result = auth.auth_register(email, password, name_first, name_last)
    save()
    interval_persistence()
    return json.dumps(result)

# auth_login
@APP.route("/auth/login", methods=['POST'])
def auth_login_flask():
    """Flask for auth login function; allows a user to login in."""

    data = request.get_json()
    email = data["email"]
    password = data["password"]

    result = auth.auth_login(email, password)
    save()
    interval_persistence()
    return json.dumps(result)

# auth_logout
@APP.route("/auth/logout", methods=['POST'])
def auth_logout_flask():
    """Flask for auth logout function; allows a user to logout in."""

    data = request.get_json()
    token = data["token"]

    result = auth.auth_logout(token)
    save()
    interval_persistence()
    return json.dumps(result)

# auth_passwordreset_request
@APP.route("/auth/passwordreset/request", methods=['POST'])
def auth_passwordreset_request_flask():
    """Flask for auth password reset request function; sends email to user about password."""

    data = request.get_json()
    email = data["email"]

    result = auth.auth_passwordreset_request(email)
    save()
    interval_persistence()
    return json.dumps(result)

# auth_passwordreset_reset
@APP.route("/auth/passwordreset/reset", methods=['POST'])
def auth_passwordreset_reset_flask():
    """Flask for auth password reset function; user is able to reset password."""

    data = request.get_json()

    reset_code = data["reset_code"]
    new_password = data["new_password"]

    result = auth.auth_passwordreset_reset(reset_code, new_password)
    save()
    interval_persistence()
    return json.dumps(result)

#............................. CHANNEL .............................#
# channel_invite
@APP.route("/channel/invite", methods=['POST'])
def channel_invite_flask():
    """Flask for channel invite function; invites user to channel."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    u_id = int(data["u_id"])

    result = ch.channel_invite(token, channel_id, u_id)
    save()
    interval_persistence()
    return json.dumps(result)

# channel_details
@APP.route("/channel/details", methods=['GET'])
def channel_details_flask():
    """Flask for channel details function; gives basic details of channel."""

    token = request.args["token"]
    channel_id = int(request.args["channel_id"])
    result = ch.channel_details(token, channel_id)

    return json.dumps(result)

# channel_messages
@APP.route("/channel/messages", methods=['GET'])
def channel_messages_flask():
    """Flask for channel messages function; shows channel messages."""

    token = request.args["token"]
    channel_id = int(request.args["channel_id"])
    start = int(request.args["start"])

    result = ch.channel_messages(token, channel_id, start)
    save()
    interval_persistence()
    return json.dumps(result)

# channel_leave
@APP.route("/channel/leave", methods=['POST'])
def channel_leave_flask():
    """Flask for channel leave function; user leaves channel."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])

    result = ch.channel_leave(token, channel_id)
    save()
    interval_persistence()
    return json.dumps(result)

# channel_join
@APP.route("/channel/join", methods=['POST'])
def channel_join_flask():
    """Flask for channel join function; user joins channel."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])

    result = ch.channel_join(token, channel_id)
    save()
    interval_persistence()
    return json.dumps(result)

# channel addowner
@APP.route("/channel/addowner", methods=["POST"])
def channel_addowner_flask():
    """Flask for channel addowner function; user making channel is owner."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    u_id = int(data["u_id"])

    result = ch.channel_addowner(token, channel_id, u_id)
    save()
    interval_persistence()
    return json.dumps(result)

# channel removeowner
@APP.route("/channel/removeowner", methods=["POST"])
def channel_removeowner_flask():
    """Flask for chanel removeowner function; removes owner of channel."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    u_id = int(data["u_id"])

    result = ch.channel_removeowner(token, channel_id, u_id)
    save()
    interval_persistence()
    return json.dumps(result)

#............................. CHANNELS .............................#
# channels list
@APP.route("/channels/list", methods=["GET"])
def channels_list_flask():
    """Flask for channels list function; lists all channels of user."""

    token = request.args["token"]

    result = chs.channels_list(token)
    return json.dumps(result)

# channels listall
@APP.route("/channels/listall", methods=["GET"])
def channels_listall_flask():
    """Flask for channels listall function; lists all channels."""

    token = request.args["token"]

    result = chs.channels_listall(token)
    return json.dumps(result)

# channels create
@APP.route("/channels/create", methods=["POST"])
def channels_create_flask():
    """Flask for channels create function; creates new channel."""

    data = request.get_json()
    token = data["token"]
    name = data["name"]
    is_public = data["is_public"]

    result = chs.channels_create(token, name, is_public)
    save()
    interval_persistence()
    return json.dumps(result)

#............................. MESSAGE .............................#
# message_send
@APP.route("/message/send", methods=['POST'])
def message_send_flask():
    """Flask for message send function; sends message from user."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    message = data["message"]

    result = msg.message_send(token, channel_id, message)
    save()
    interval_persistence()
    return json.dumps(result)

# message_sendlater
@APP.route("/message/sendlater", methods=['POST'])
def message_send_later_flask():
    """Flask for message send later function; user sends message at desired time."""

    data = request.get_json()
    token = data["token"]
    channel_id = int(data["channel_id"])
    message = data["message"]
    time_sent = float(data["time_sent"])

    result = msg.message_send_later(token, channel_id, message, time_sent)
    save()
    interval_persistence()
    return json.dumps(result)

# message_react
@APP.route("/message/react", methods=['POST'])
def message_react_flask():
    """Flask for message react function; user uses react in message."""

    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])
    react_id = int(data['react_id'])

    result = msg.message_react(token, message_id, react_id)
    save()
    interval_persistence()
    return json.dumps(result)

# message_unreact
@APP.route("/message/unreact", methods=['POST'])
def message_unreact_flask():
    """Flask for message unreact function; user removes react in message."""

    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    react_id = int(data['react_id'])

    result = msg.message_unreact(token, message_id, react_id)

    save()
    interval_persistence()
    return json.dumps(result)

# message_pin
@APP.route("/message/pin", methods=['POST'])
def message_pin_flask():
    """Flask for message pin function; user pins message."""

    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])

    result = msg.message_pin(token, message_id)
    save()
    interval_persistence()
    return json.dumps(result)

# message_unpin
@APP.route("/message/unpin", methods=['POST'])
def message_unpin_flask():
    """Flask for message unpin function; user unpins pinned message."""

    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])

    result = msg.message_unpin(token, message_id)
    save()
    interval_persistence()
    return json.dumps(result)

# message_remove
@APP.route("/message/remove", methods=['DELETE'])
def message_remove_flask():
    """Flask for message remove function; user removes message."""

    data = request.get_json()
    token = data['token']
    message_id = int(data['message_id'])

    result = msg.message_remove(token, message_id)
    save()
    interval_persistence()
    return json.dumps(result)

# message_edit
@APP.route("/message/edit", methods=['PUT'])
def message_edit_flask():
    """Flask for message edit function; user updates message text."""

    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']

    result = msg.message_edit(token, message_id, message)
    save()
    interval_persistence()
    return json.dumps(result)

#............................. USER .............................#
# user_profile
@APP.route("/user/profile", methods=['GET'])
def user_profile_flask():
    """Flask for user profile function; returns user information."""

    token = request.args["token"]
    u_id = int(request.args["u_id"])
    result = user.user_profile(token, u_id)
    save()
    interval_persistence()
    return json.dumps(result)  #### Check this return

# user_profile_setname
@APP.route("/user/profile/setname", methods=['PUT'])
def user_profile_setname_flask():
    """Flask for user profile setname function; updates user's first/last names."""

    data = request.get_json()
    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    result = user.user_profile_setname(token, name_first, name_last)

    save()
    interval_persistence()
    return json.dumps(result)

# user_profile_setemail
@APP.route("/user/profile/setemail", methods=['PUT'])
def user_profile_setemail_flask():
    """Flask for user profile setemail function; updates user's email."""

    data = request.get_json()
    token = data["token"]
    email = data["email"]

    result = user.user_profile_setemail(token, email)

    save()
    interval_persistence()
    return json.dumps(result)

# user_profile_sethandle
@APP.route("/user/profile/sethandle", methods=['PUT'])
def user_profile_sethandle_flask():
    """Flask for user profile sethandle function; updates user's handle."""

    data = request.get_json()
    token = data["token"]
    handle_str = data["handle_str"]

    result = user.user_profile_sethandle(token, handle_str)

    save()
    interval_persistence()
    return json.dumps(result)

# user_profile_uploadphoto
@APP.route("/user/profile/uploadphoto", methods=['POST'])
def user_profile_uploadphoto_flask():
    """Flask for user profile upload photo function; uploads user's photo."""

    data = request.get_json()

    token = data["token"]
    img_url = data["img_url"]
    x_start = int(data["x_start"])
    y_start = int(data["y_start"])
    x_end = int(data["x_end"])
    y_end = int(data["y_end"])

    result = user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)

    save()
    interval_persistence()
    return json.dumps(result)

# user_all
@APP.route("/users/all", methods=['GET'])
def users_all_flask():
    """Flask for users all function; returns details about all users."""

    token = request.args["token"]
    result = user.users_all(token)
    return json.dumps(result)

#............................. STAND-UP .............................#
# stand-up start
@APP.route("/standup/start", methods=["POST"])
def standup_start_flask():
    """Flask for standup start function; returns standup time finish."""

    token = request.args["token"]
    data = request.get_json
    channel_id = int(data["channel_id"])
    length = data["length"]

    result = st.standup_start(token, channel_id, length)

    save()
    interval_persistence()
    return json.dumps(result)

# stand-up active
@APP.route("/standup/active", methods=["GET"])
def standup_active_flask():
    """Flask for standup active function; returns standup time finish and active status."""

    token = request.args["token"]
    channel_id = int(request.args["channel_id"])
    result = st.standup_active(token, channel_id)

    return json.dumps(result)

# stand-up send
@APP.route("/standup/send", methods=["POST"])
def standup_send_flask():
    """Flask for standup send function; sends message to get buffered."""

    token = request.args["token"]
    channel_id = int(request.args["channel_id"])
    data = request.get_json()
    message = data["message"]

    result = st.standup_send(token, channel_id, message)

    save()
    interval_persistence()
    return json.dumps(result)

#............................. MISCELLANEOUS .............................#
# search
@APP.route("/search", methods=['GET'])
def search_flask():
    """Flask for search function; returns messages relating to query."""

    token = request.args["token"]
    query_str = request.args["query_str"]

    result = search(token, query_str)

    save()
    interval_persistence()
    return json.dumps(result)

# admin_userpermission_change
@APP.route("/admin/userpermission/change", methods=['POST'])
def admin_userpermissions_change_flask():
    """Flask for admin userpermissions change function; sets user permissions to new permissions."""

    data = request.get_json()
    token = data["token"]
    u_id = int(data["u_id"])
    permission_id = int(data["permission_id"])

    result = admin_userpermissions_change(token, u_id, permission_id)
    save()
    interval_persistence()
    return json.dumps(result)

# admin_user_remove
@APP.route("/admin/user/remove", methods=['DELETE'])
def admin_user_remove_flask():
    """Flask for admin user remove function; removes user from Slackr."""

    token = request.args["token"]
    u_id = int(request.args["u_id"])

    result = admin_user_remove(token, u_id)
    save()
    return json.dumps(result)

# workspace_reset
@APP.route("/workspace/reset", methods=['POST'])
def workspace_reset_flask():
    """Flask for workspace rest function; resets the workspace state."""

    result = workspace_reset()

    save()
    interval_persistence()
    return json.dumps(result)

if __name__ == "__main__":
    APP.run(debug=True, port=8956)
