import datetime

from backend import authentication
from backend import storage
from backend import channel as channel_utils
from backend import message as message_utils
from backend import errors


def standup_start(token, channel_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    i = 0
    while i < len(data["channels"]):
        if data["channels"][i]["channelID"] == channel_id:
            # check if currently running a stand_up
            if data["channels"][i]["standup_time"] >= datetime.datetime.now():
                raise ValueError("This channel already has a standup started")
            elif u_id not in data["channels"][i]["membersUID"]:
                raise errors.AccessError("This user isn't a member of the channel")
            else:
                # return time + 15 mins
                time = datetime.datetime.now() + datetime.timedelta(minutes=15)
                data["channels"][i]["standup_time"] = time
                storage.dump_data_store(data)
                return time
        i += 1

    raise ValueError("Channel ID is not a valid channel")


def standup_send(token, channel_id, message):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # check the message <= 1000 characters
    if len(message) > 1000:
        raise ValueError("Message is more than 1000 characters.")

    i = 0
    while i < len(data["channels"]):
        if data["channels"][i]["channelID"] == channel_id:
            # check if currently running a stand_up
            if data["channels"][i]["standup_time"] <= datetime.datetime.now():
                raise ValueError("This channel doesn't have a standup")
            elif u_id not in data["channels"][i]["membersUID"]:
                raise errors.AccessError("This user isn't a member of the channel")
            else:
                timesent = data["channels"][i]["standup_time"]
                message_utils.message_sendlater(token, channel_id, message, timesent)
                return
        i += 1

    raise ValueError("Channel ID is not a valid channel")
