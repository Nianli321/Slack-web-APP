from datetime import datetime
from secrets import token_bytes
from sys import byteorder

from backend import authentication
from backend import storage
from backend import channel as channel_utils
from backend import errors, utils

'''
message = {
    'message_id' = 0
    'u_id' = 0
    'message' = ''
    'time_created' = datetime
    'reacts' = [{ react_id, u_ids[], is_this_user_reacted[] }]
    'is_pinned' = False
}
'''
# Send a message from authorised_user to the channel specified by channel_id
# automatically at a specified time in the future


def message_sendlater(token, channel_id, message, time_sent):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # check the message <= 1000 characters
    if len(message) > 1000:
        raise ValueError("Message is more than 1000 characters.")

    # check if user is an admin, owner or a member of the channel
    channel_deats = channel_utils.channel_details(token, channel_id)
    if u_id not in channel_deats['all_members']:
        raise errors.AccessError(
            "The user isn't authorised to post in this channel.")

    # time in the future
    if time_sent < datetime.now():
        raise ValueError("Time sent is in the past.")

    # generate a message_id, and set to post at correct time
    message = message_create(u_id, message, time_sent)

    # put the message into the channel
    for channel in data['channels']:
        if channel['channelID'] == channel_id:
            break
    channel['messages'].insert(0, message)
    # HOW TO DO TIME?

    storage.dump_data_store(data)
    return message['message_id']

# Send a message from authorised_user to the channel specified by channel_id


def message_send(token, channel_id, text):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # check the message <= 1000 characters
    if len(text) > 1000:
        raise ValueError("Message is more than 1000 characters")

    # check if user is an admin, owner or a member of the channel
    channel_deats = channel_utils.channel_details(token, channel_id)
    if u_id not in channel_deats['all_members']:
        raise errors.AccessError(
            "The user isn't authorised to post in this channel")

    # generate a message_id, and post it
    message = message_create(u_id, text, datetime.now())

    # put the message onto a channel
    for channel in data['channels']:
        if channel['channelID'] == channel_id:
            break
    channel['messages'].insert(0, message)

    storage.dump_data_store(data)

    return message['message_id']

# Given a message_id for a message, this message is removed from the channel


def message_remove(token, message_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # find message through channel/list, then channel messages to find the correct message
    i = 0
    while i < len(data["channels"]):
        j = 0
        if u_id in data["channels"][i]["membersUID"]:
            while j < len(data["channels"][i]["messages"]):
                if message_id == data["channels"][i]["messages"][j]["message_id"]:
                    if (u_id not in data["channels"][i]['ownersUID']) and \
                        (u_id not in data["channels"][i]["messages"][j]['u_id']):
                        raise ValueError(
                            "Neither the original poster of this message or an owner")
                    del data["channels"][i]["messages"][j]
                    storage.dump_data_store(data)
                    return
                j += 1
        i += 1

    raise errors.AccessError("Message_id isn't in any channel you have access too")
    pass

# Given a message, update it's text with new text


def message_edit(token, message_id, message):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # check the message <= 1000 characters
    if len(message) > 1000:
        raise ValueError("Message is more than 1000 characters")

    # find message through channel/list, then channel messages to find the correct message
    i = 0
    #print(channels['channels'][i]['channel_id'])
    while i < len(data["channels"]):
        j = 0
        if u_id in data["channels"][i]["membersUID"]:
            while j < len(data["channels"][i]["messages"]):
                if message_id == data["channels"][i]["messages"][j]["message_id"]:
                    if (u_id not in data["channels"][i]['ownersUID']) and \
                        (u_id not in data["channels"][i]["messages"][j]['u_id']):
                        raise ValueError(
                            "Neither the original poster of this message or an owner")
                    data["channels"][i]["messages"][j] = message
                    storage.dump_data_store(data)
                    return
                j += 1
        i += 1

    raise errors.AccessError("Message_id isn't in any channel you have access too")
    pass


# Given a message within a channel the authorised user is part of, add a "react" to that message


def message_react(token, message_id, react_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # Valid react_id (Only 1 is currently valid)
    if react_id != 1:
        raise ValueError("not a valid react_id")

    # search through channel/list, then channel messages to find the correct message
    i = 0
    #print(channels['channels'][i]['channel_id'])
    while i < len(data["channels"]):
        j = 0
        if u_id in data["channels"][i]["membersUID"]:
            while j < len(data["channels"][i]["messages"]):
                if message_id == data["channels"][i]["messages"][j]["message_id"]:
                    if data["channels"][i]["messages"][j]["reacts"][0]['is_this_user_reacted'] == True:
                        raise ValueError(
                            "You have already reacted to this message with this reaction")
                    data["channels"][i]["messages"][j]["reacts"][0]['is_this_user_reacted'] = True
                    data["channels"][i]["messages"][j]["reacts"][0]['u_ids'].append(u_id)
                    storage.dump_data_store(data)
                    return
                j += 1
        i += 1

    # check react id's
    raise ValueError(
        "Not a valid message in a channel that the user is apart of")

# Given a message within a channel the authorised user is part of,
# remove a "react" to that particular message


def message_unreact(token, message_id, react_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # Valid react_id (Only 1 is currently valid)
    if react_id != 1:
        raise ValueError("not a valid react_id")

    # search through channel/list, then channel messages to find the correct message
    i = 0
    #print(channels['channels'][i]['channel_id'])
    while i < len(data["channels"]):
        j = 0
        if u_id in data["channels"][i]["membersUID"]:
            while j < len(data["channels"][i]["messages"]):
                if message_id == data["channels"][i]["messages"][j]["message_id"]:
                    if data["channels"][i]["messages"][j]["reacts"][0]['is_this_user_reacted'] == False:
                        raise ValueError(
                            "You haven't reacted to this message with this reaction")
                    data["channels"][i]["messages"][j]["reacts"][0]['is_this_user_reacted'] = False
                    data["channels"][i]["messages"][j]["reacts"][0]['u_ids'].remove(u_id)
                    storage.dump_data_store(data)
                    return
                j += 1
        i += 1

    # check react id's
    raise ValueError("Not a valid message in a channel that the user is apart of")

# Given a message within a channel, mark it as "pinned" to be given special
# display treatment by the frontend


def message_pin(token, message_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # if the token owner is an owner or an admin (p_id 1 and 2) (search through all
    # users for permission level)
    # look through all channels the user is apart of
    i = 0
    while i < len(data["channels"]):
        j = 0
        while j < len(data["channels"][i]["messages"]):
            if message_id == data["channels"][i]["messages"][j]["message_id"]:
                if u_id in data["channels"][i]["ownersUID"]:
                    if data["channels"][i]["messages"][j]["is_pinned"] == True:
                        raise ValueError(
                            "This message is already pinned")
                    data["channels"][i]["messages"][j]["is_pinned"] = True
                    storage.dump_data_store(data)
                    return
                if u_id in data["channels"][i]["membersUID"]:
                    raise ValueError ("User isn't an admin")
                raise errors.AccessError("User isn't a member of the channel the message is in")
            j += 1
        i += 1

    raise ValueError("message_id isn't a valid message")
    pass

# Given a message within a channel, remove it's mark as unpinned


def message_unpin(token, message_id):
    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    # if the token owner is an owner or an admin (p_id 1 and 2)
    # (search through all users for permission level)
    # look through all channels the user is apart of
    #print(channels['channels'][i]['channel_id'])
    i = 0
    while i < len(data["channels"]):
        j = 0
        while j < len(data["channels"][i]["messages"]):
            if message_id == data["channels"][i]["messages"][j]["message_id"]:
                if u_id in data["channels"][i]["ownersUID"]:
                    if data["channels"][i]["messages"][j]["is_pinned"] == False:
                        raise ValueError(
                            "This message is already pinned")
                    data["channels"][i]["messages"][j]["is_pinned"] = False
                    storage.dump_data_store(data)
                    return
                if u_id in data["channels"][i]["membersUID"]:
                    raise ValueError("User isn't an admin")
                raise errors.AccessError("User isn't a member of the channel the message is in")
            j += 1
        i += 1

    raise ValueError("message_id isn't a valid message")
    pass


def message_create(u_id, message, time_sent):

    message = {
        'message_id': utils.generate_luid(),
        'u_id': u_id,
        'message': message,
        'time_created': time_sent,
        # Currently only 1 react_id
        'reacts': [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}],
        'is_pinned': False
    }

    return message
