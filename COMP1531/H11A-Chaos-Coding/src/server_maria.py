# Written by Maria Cuyutupa Garcia z5223865 in March 2020

# Python libraries
from flask import Flask, request
from json import dumps

# Project Files
import standup as st
import channel_owner as ch  ###
import channels as chs

APP = Flask(__name__)

# Channel addowner
@APP.route("/channel/addowner", methods=["POST"])
def channel_addowner_flask():
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    u_id = request.form.get("u_id")
    save()

    return dumps(ch.channel_addowner(token, channel_id, u_id))

# Channel removeowner
@APP.route("/channel/removeowner", methods=["POST"])
def channel_removeowner_flask():
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    u_id = request.form.get("u_id")
    save()

    return dumps(ch.channel_removeowner(token, channel_id, u_id))

# Channels list
@APP.route("/channels/list", methods=["GET"])
def channels_list_flask():
    return dumps(chs.channels_list(request.form.get("token")))

# Channels listall
@APP.route("/channels/listall", methods=["GET"])
def channels_listall_flask():
    return dumps(chs.channels_listall(request.form.get("token")))

# Channels create
@APP.route("/channels/create", methods=["POST"])
def channels_create_flask():
    token = request.form.get("token")
    name = request.form.get("name")
    is_public = request.form.get("is_public")
    save()

    return dumps(chs.channels_create(token, name, is_public))

# Stand-up start
@APP.route("/standup/start", methods=["POST"])
def standup_start_flask():
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")
    length = request.form.get("length")
    save()

    return dumps(st.standup_start(token, channel_id, length))

# Stand-up active
@APP.route("/standup/active", methods=["GET"])
def standup_active_flask():
    token = request.form.get("token")
    channel_id = request.form.get("channel_id")

    return dumps(st.standup_active(token, channel_id))

# Stand-up send
@APP.route("/standup/send", methods=["POST"])
def standup_send_flask():
    token = request.form.get("token")
    channel_id = request.form.get("channel_id") 
    message = request.form.get("message")

    return dumps(st.standup_send(token, channel_id, message))

if __name__ == "__main__":
    APP.run(port=8080)