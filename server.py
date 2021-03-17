"""Flask server"""
import sys
from json import dumps
from smtplib import SMTPException

from flask import Flask, request
from flask_cors import CORS
from flask_mail import Mail, Message

from backend import admin as admin_utils
from backend import authentication as auth_utils
from backend import channel as channel_utils
from backend import message as message_utils
from backend import search as search_utils
from backend import user as user_utils
from backend import standup as standup_utils

MAIL_USERNAME = "cs1531namegenerator@gmail.com"

APP = Flask(__name__)
APP.config.update(
    MAIL_SERVER="smtp.gmail.com",
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME="cs1531namegenerator@gmail.com",
    MAIL_PASSWORD="Y0XJYH@suk309"
)

CORS(APP)

#### ECHO ####
@APP.route("/echo/get", methods=["GET"])
def echo1():
    """ echo what it recieves """
    return dumps({
        "echo": request.args.get("echo"),
    })


@APP.route("/echo/post", methods=["POST"])
def echo2():
    """ echos what it recieves """
    return dumps({
        "echo": request.form.get("echo"),
    })


#### AUTHENTICATION ####
@APP.route("/auth/register", methods=["POST"])
def auth_register():
    email = request.form.get("email")
    password = request.form.get("password")
    first_name = request.form.get("name_first")
    last_name = request.form.get("name_last")

    res = auth_utils.auth_register(email,
                                   password,
                                   first_name,
                                   last_name)

    return dumps(res)


@APP.route("/auth/login", methods=["POST"])
def auth_login():
    email = request.form.get("email")
    password = request.form.get("password")

    result = auth_utils.auth_login(email, password)

    return dumps({
        "u_id": result["u_id"],
        "token": result["token"]
    })


@APP.route("/auth/passwordreset/request", methods=["POST"])
def auth_passwordreset_request():
    email = request.form.get("email")

    try:
        reset_code = auth_utils.auth_passwordreset_request(email)
    except ValueError:
        # Just ignore invalid attempts
        return dumps({})

    mail = Mail(APP)
    try:
        msg = Message(subject="Your password reset code for Slackr",
                      body=f"Your password reset code is {reset_code}",
                      sender=MAIL_USERNAME,
                      recipients=[email])
        mail.send(msg)
        return dumps({})
    except SMTPException:
        return dumps({})


@APP.route("/admin/userpermission/change", methods=["POST"])
def admin_userpermission_change():
    token = request.form.get("token")
    u_id = request.form.get("u_id")
    permission_id = request.form.get("permission_id")

    try:
        u_id = int(u_id)
        permission_id = int(permission_id)
    except TypeError:
        raise ValueError("Gave an invalid u_id or permission_id")

    admin_utils.admin_userpermission_change(token, u_id, permission_id)

    return dumps({})


@APP.route("/auth/logout", methods=["POST"])
def auth_logout():
    token = request.form.get("token")

    result = auth_utils.auth_logout(token)

    return dumps({"is_success": result})


@APP.route("/auth/passwordreset/reset", methods=["POST"])
def auth_passwordreset_reset():
    reset_code = request.form.get("reset_code")
    new_password = request.form.get("new_password")

    auth_utils.auth_passwordreset_reset(reset_code, new_password)

    return dumps({})

##### CHANNEL/CHANNELS #####
@APP.route("/channel/invite", methods=["POST"])
def channel_invite():

    token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    u_id = int(request.form.get("u_id"))

    channel_utils.channel_invite(token, channel_id, u_id)

    return dumps({
    })


@APP.route("/channel/details", methods=["GET"])
def channel_details():

    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))

    details = channel_utils.channel_details(token, channel_id)

    return dumps({
        "name": details["name"],
        "all_members": details["members"],
        "owner_members": details["ownersUID"]
    })


@APP.route("/channel/messages", methods=["GET"])
def channel_messages():

    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    start = request.args.get("start")

    messages = channel_utils.channel_messages(token, channel_id, start)

    return dumps({
        "messages": messages["messages"],
        "start": messages["start"],
        "end": messages["end"]
    })


@APP.route("/channel/leave", methods=["POST"])
def channel_leave():

    token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))

    channel_utils.channel_leave(token, channel_id)

    return dumps({
    })


@APP.route("/channel/join", methods=["POST"])
def channel_join():

    token = request.form.get("token")
    channel_id = request.form.get("channel_id")

    channel_utils.channel_join(token, channel_id)

    return dumps({
    })


@APP.route("/channel/addowner", methods=["POST"])
def channel_addowner():

    token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    u_id = int(request.form.get("u_id"))

    channel_utils.channel_addowner(token, channel_id, u_id)

    return dumps({
    })


@APP.route("/channel/removeowner", methods=["POST"])
def channel_removeowner():

    token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    u_id = int(request.form.get("u_id"))

    channel_utils.channel_removeowner(token, channel_id, u_id)

    return dumps({
    })


@APP.route("/channels/list", methods=["GET"])
def channels_list():

    token = request.args.get("token")

    c_list = channel_utils.channels_list(token)

    return dumps({
        "channels": c_list["channels"]
    })


@APP.route("/channels/listall", methods=["GET"])
def channels_listall():

    token = request.args.get("token")

    c_list = channel_utils.channels_listall(token)

    return dumps({
        "channels": c_list["channels"]
    })


@APP.route("/channels/create", methods=["POST"])
def channels_create():

    token = request.form.get("token")
    name = request.form.get("name")
    is_public = request.form.get("is_public")

    channel_id = channel_utils.channels_create(token, name, is_public)

    return dumps({
        "channel_id": channel_id
    })


##### MESSAGES #####
@APP.route("/message/sendlater", methods=["POST"])
def message_send_later():

    my_token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    message = request.form.get("message")
    time = request.form.get("time_sent")

    message_id = message_utils.message_sendlater(
        my_token, channel_id, message, time)

    return dumps({
        "message_id": message_id
    })


@APP.route("/message/send", methods=["POST"])
def message_send():

    my_token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    message = request.form.get("message")

    message_id = message_utils.message_send(my_token, channel_id, message)

    return dumps({
        "message_id": message_id
    })


@APP.route("/message/remove", methods=["DELETE"])
def message_remove():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))

    message_utils.message_remove(my_token, message_id)

    return dumps({
    })


@APP.route("/messgae/edit", methods=["PUT"])
def message_edit():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))
    message = request.form.get("message")

    message_utils.message_edit(my_token, message_id, message)

    return dumps({
    })


@APP.route("/message/react", methods=["POST"])
def message_react():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))
    react_id = int(request.form.get("react_id"))

    message_utils.message_react(my_token, message_id, react_id)

    return dumps({
    })


@APP.route("/message/unreact", methods=["POST"])
def message_unreact():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))
    react_id = int(request.form.get("react_id"))

    message_utils.message_unreact(my_token, message_id, react_id)

    return dumps({
    })


@APP.route("/message/pin", methods=["POST"])
def message_pin():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))

    message_utils.message_pin(my_token, message_id)

    return dumps({
    })


@APP.route("/message/unpin", methods=["POST"])
def message_unpin():

    my_token = request.form.get("token")
    message_id = int(request.form.get("message_id"))

    message_utils.message_unpin(my_token, message_id)

    return dumps({
    })


##### SEARCH #####
@APP.route("/search", methods=["GET"])
def search():

    my_token = request.args.get("token")
    query = request.args.get("query_str")

    msgs = search_utils.search(my_token, query)

    return dumps({
        "messages": msgs
    })

#######PROFILE#######
@APP.route("/user/profile", methods=["GET"])
def user_profile():

    my_token = request.args.get("token")
    my_uid = int(request.args.get("u_id"))

    response = user_utils.user_profile(my_token, my_uid)

    return dumps({
        "email": response["email"],
        "name_first": response["name_first"],
        "name_last": response["name_last"],
        "handle_str": response["handle_str"]
    })


@APP.route("/user/profile/setname", methods=["PUT"])
def user_profile_setname():

    my_token = request.form.get("token")
    my_first_name = request.form.get("name_first")
    my_last_name = request.form.get("name_last")

    user_utils.user_profile_setname(my_token, my_first_name, my_last_name)

    return dumps({
    })

# PUT user/profile/setemail
@APP.route("/user/profile/setemail", methods=["PUT"])
def user_profile_setemail():

    my_token = request.form.get("token")
    my_email = request.form.get("email")

    user_utils.user_profile_setemail(my_token, my_email)
    return dumps({
    })


@APP.route("/user/profile/sethandle", methods=["PUT"])
def user_profile_sethandle():

    my_token = request.form.get("token")
    my_handle = request.form.get("handle_str")

    user_utils.user_profile_sethandle(my_token, my_handle)
    return dumps({
    })


##### Standup #####
@APP.route("/standup/start", methods=["POST"])
def standup_start():

    my_token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))

    time_finish = standup_utils.standup_start(my_token, channel_id)

    return dumps({
        'time_finish': time_finish
    })


@APP.route("/standup/send", methods=["POST"])
def standup_send():

    my_token = request.form.get("token")
    channel_id = int(request.form.get("channel_id"))
    message = request.form.get("message")

    standup_utils.standup_send(my_token, channel_id, message)

    return dumps({
    })


if __name__ == "__main__":
    APP.run(port=(sys.argv[1] if len(sys.argv) > 1 else 5000))
