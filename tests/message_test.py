from datetime import datetime

import pytest

from backend import authentication
from backend import channel as channel_utils
from backend import errors
from backend import message as message_utils
from backend import storage

# If the test produces a vlue error, beneath the test explanation there will be a # VALUE ERROR


def test_message_sendlater():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid1@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Everything valid.
    token = token1
    channel_id = channel_id_valid
    message = "Valid message."
    time_sent = datetime(2019, 10, 31, 10, 10)
    message_id = message_utils.message_sendlater(token, channel_id, message, time_sent)

    # Prove it worked
    u_id = authentication.decode_token(token)["u_id"]
    channel = channel_utils.get_channel(channel_id)
    assert channel['messages'][0]['message_id'] == message_id

    # Token invaid
    token = "NotValid"
    channel_id = channel_id_valid
    message = "Valid message."
    time_sent = datetime(2019, 10, 31, 10, 10)
    with pytest.raises(ValueError):
        message_utils.message_sendlater(token, channel_id, message, time_sent)

    # The channel which the message is getting posted too doesn't exist
    # VALUE ERROR
    token = token1
    channel_id = -12
    message = "Valid message."
    time_sent = datetime(2019, 10, 31, 10, 10)
    # use channel_list
    with pytest.raises(ValueError):
        message_utils.message_sendlater(token, channel_id, message, time_sent)

    # set up another channel, which the original user doesn't have access too
    dic2 = authentication.auth_register(
        'valid3@email.com', 'password2', 'Bobby', 'Jamesy')
    token2 = dic2['token']

    # creat a valid channel in the name of user1
    dic_a = channel_utils.channels_create(token2, 'name', False)
    channel_id_valid1 = dic_a['channel_id']

    # User lacks access to current channel trying to post in.
    token = token1
    channel_id = channel_id_valid1
    message = "Valid message"
    time_sent = datetime(2019, 10, 31, 10, 10)
    with pytest.raises(errors.AccessError):
        message_utils.message_sendlater(token, channel_id, message, time_sent)

    # Message is too long (over 1000 characters).
    # VALUE ERROR
    token = token1
    channel_id = channel_id_valid
    message = "0123456789" * 101
    time_sent = datetime(2019, 10, 31, 10, 10)
    with pytest.raises(ValueError):
        message_utils.message_sendlater(token, channel_id, message, time_sent)

    # Time sent is in the past
    # VALUE ERROR
    token = token1
    channel_id = channel_id_valid
    message = "Valid message."
    time_sent = datetime(2019, 8, 31, 10, 10)
    with pytest.raises(ValueError):
        message_utils.message_sendlater(token, channel_id, message, time_sent)

    pass


def test_message_send():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid2@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Value error when message too long
    # VALUE ERROR
    token = token1
    channel_id = channel_id_valid
    message = "0123456789" * 101
    with pytest.raises(ValueError):
        message_utils.message_send(token, channel_id, message)

    # Invalid token.
    token = "InvalidToken"
    channel_id = channel_id_valid
    message = "Valid message"
    with pytest.raises(ValueError):
        message_utils.message_send(token, channel_id, message)

    # Channel_id doesn't exist.
    token = token1
    channel_id = -1
    message = "Valid message"
    with pytest.raises(ValueError):
        message_utils.message_send(token, channel_id, message)


    # set up another channel, which the original user doesn't have access too
    dic2 = authentication.auth_register(
        'valid3@email.com', 'password2', 'Bobby', 'Jamesy')
    token2 = dic2['token']

    # creat a valid channel in the name of user1
    dic_a = channel_utils.channels_create(token2, 'matth', False)
    channel_id_valid1 = dic_a['channel_id']

    # User lacks access to current channel trying to post in.
    token = token1
    channel_id = channel_id_valid1
    message = "Valid message"
    with pytest.raises(errors.AccessError):
        message_utils.message_send(token, channel_id, message)

    # Everything Valid
    token = token1
    channel_id = channel_id_valid
    message = "Valid message"
    message_id = message_utils.message_send(token, channel_id, message)

    u_id = authentication.decode_token(token)["u_id"]
    channel = channel_utils.get_channel(channel_id)
    assert channel['messages'][0]['message_id'] == message_id
    assert channel['messages'][0]['u_id'] == u_id
    assert channel['messages'][0]['message'] == "Valid message"
    assert channel['messages'][0]['reacts'] == [{'react_id': 1, 'u_ids': [], 'is_this_user_reacted': False}]
    assert channel['messages'][0]['is_pinned'] == False

    # send a second message
    message = "Second message"
    token = token1
    message_id2 = message_utils.message_send(token, channel_id, message)
    channel = channel_utils.get_channel(channel_id)
    assert channel['messages'][0]['message_id'] == message_id2
    assert channel['messages'][1]['message_id'] == message_id


def test_message_remove():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid3@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # Channel to post message which will be deleated
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Message to be deleated
    message_id = message_utils.message_send(token1, channel_id_valid, "Hello")

    # ValueError when message doesn't exist
    # VALUE ERROR
    token = token1
    message_id1 = -99
    with pytest.raises(errors.AccessError):
        message_utils.message_remove(token, message_id1)

    # When all of the following isn't true:
    # Meassage with message_id wasn't sent by the authorised user making the request
    # Meassage with message_id was not sent by an owner of this channel
    # Meassage with message_id was not sent by an admin or owner of the slack
    # ACCESS ERROR
    # second user without access
    dic2 = authentication.auth_register(
        'valid33@email.com', 'password2', 'Bobby', 'Jamesy')
    token2 = dic2['token']
    token = token2
    with pytest.raises(errors.AccessError):
        message_utils.message_remove(token, message_id)

    # Everything valid
    token = token1
    message_utils.message_remove(token, message_id)

    # Check
    channel = channel_utils.get_channel(channel_id_valid)
    assert channel['messages'] == []

    pass


def test_message_edit():
    # set up user
    storage.clear_data_store()
    dic1 = authentication.auth_register(
        'valid4@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Message to be edited
    message = "Unedited message"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    # When all of the following isn't true:
    # Meassage with message_id wasn't sent by the authorised user making the request
    # Meassage with message_id was not sent by an owner of this channel
    # Meassage with message_id was not sent by an admin or owner of the slack
    # VALUE ERROR
    dic2 = authentication.auth_register(
        'valid33@email.com', 'password2', 'Bobby', 'Jamesy')
    token2 = dic2['token']
    token = token2
    message = "Editted message."
    with pytest.raises(errors.AccessError):
        message_utils.message_edit(token, message_id, message)

    # Message is too long (over 1000 characters).
    token = token1
    message = "0123456789" * 101
    with pytest.raises(ValueError):
        message_utils.message_edit(token, message_id, message)

    # Message_id is invalid.
    token = token1
    bad_message_id = -99
    message = "Editted message."
    with pytest.raises(errors.AccessError):
        message_utils.message_edit(token, bad_message_id, message)

    # Everything valid.
    token = token1
    message = "Editted message."
    message_utils.message_edit(token, message_id, message)

    # Prove that it worked
    data = channel_utils.get_data()
    assert data["channels"][0]['messages'][0] == "Editted message."

    pass


def test_message_react():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid5@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Message to be reacted
    message = "React to me :)"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    # Invalid token
    token = "Invalidtoken"
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_react(token, message_id, react_id)

    # Everything valid
    token = token1
    react_id = 1
    message_utils.message_react(token, message_id, react_id)

    # Prove that it worked.
    u_id = authentication.decode_token(token)["u_id"]
    channel = channel_utils.get_channel(channel_id_valid)
    assert channel['messages'][0]['message'] == message
    assert channel['messages'][0]['reacts'] == [{'is_this_user_reacted': True, \
                                                'react_id': 1, 'u_ids': [u_id]}]

    # message_id isn't a valid message within a channel that the user has joined
    # VALUE ERROR
    token = token1
    bad_message_id = -99
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_react(token, bad_message_id, react_id)

    # react id isn't valid
    # VALUE ERROR
    token = token1
    react_id = -99
    with pytest.raises(ValueError):
        message_utils.message_react(token, message_id, react_id)

    # message with id message_id already contains an active react with given id
    # VALUE ERROR
    token = token1
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_react(token, message_id, react_id)
    pass


def test_message_unreact():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid6@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # message to be unreacted
    message = "unReact to me :)"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    # Setting the message to have been reacted to by token1 with a react_id 1
    react_id = 1
    message_utils.message_react(token1, message_id, react_id)

    # Everything valid.
    token = token1
    react_id = 1
    message_utils.message_unreact(token, message_id, react_id)

    # Prove that it worked
    channel = channel_utils.get_channel(channel_id_valid)
    u_id = authentication.decode_token(token)["u_id"]
    assert channel['messages'][0]['reacts'] == [{'is_this_user_reacted': False, \
                                                'react_id': 1, 'u_ids': []}]

    # message_id isn't a valid message within a channel that the user has joined
    # VALUE ERROR
    token = token1
    message_id = -99
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_unreact(token, message_id, react_id)

    # react id isn't valid
    # VALUE ERROR
    token = token1
    react_id = -99
    with pytest.raises(ValueError):
        message_utils.message_unreact(token, message_id, react_id)

    # message with id message_id does not contain an active react with given id
    # VALUE ERROR
    token = token1
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_unreact(token, message_id, react_id)

    # Invalid token
    token = "Invalidtoken"
    react_id = 1
    with pytest.raises(ValueError):
        message_utils.message_unreact(token, message_id, react_id)


def test_message_pin():
    storage.clear_data_store()
    # set up user (assuming user has admin privlages)
    dic1 = authentication.auth_register(
        'valid7@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', True)
    channel_id_valid = dic['channel_id']

    # message to pin
    message = "Pin me :)"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    # second user
    dic2 = authentication.auth_register(
        'valid20@email.com', 'password2', 'Bobb', 'Jamesss')
    token2 = dic2['token']

    # The authorised user isn't a member of the channel that contains the message.
    # ACCESS ERROR
    token = token2
    with pytest.raises(errors.AccessError):
        message_utils.message_pin(token, message_id)
    pass

    # make the user a member of the channel, but not an admin
    channel_utils.channel_join(token2, channel_id_valid)

    # The authoriserd user isn't an admin.
    # VALUE ERROR
    token = token2
    with pytest.raises(ValueError):
        message_utils.message_pin(token, message_id)

    # Everything valid.
    token = token1
    message_utils.message_pin(token, message_id)

    # Prove that it worked
    channel = channel_utils.get_channel(channel_id_valid)
    assert channel['messages'][0]['is_pinned'] == True

    # Message_id isn't a valid message.
    # VALUE ERROR
    token = token1
    bad_message_id = -99
    with pytest.raises(ValueError):
        message_utils.message_pin(token, bad_message_id)

    # Message id is already pinned.
    # VALUE ERROR
    token = token1
    with pytest.raises(ValueError):
        message_utils.message_pin(token, message_id)


def test_message_unpin():
    storage.clear_data_store()
    # set up user (assuming user has admin privlages)
    dic1 = authentication.auth_register(
        'valid8@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', True)
    channel_id_valid = dic['channel_id']

    # message to pin/unpin
    message = "unPin me :)"
    token = token1
    message_id = message_utils.message_send(token, channel_id_valid, message)

    message_utils.message_pin(token, message_id)

    # second user
    dic2 = authentication.auth_register(
        'valid20@email.com', 'password2', 'Bobb', 'Jamesss')
    token2 = dic2['token']

    # The authorised user isn't a member of the channel that contains the message
    # ACCESS ERROR
    token = token2
    with pytest.raises(errors.AccessError):
        message_utils.message_unpin(token, message_id)

    # make the user a member of the channel, but not an admin
    channel_utils.channel_join(token2, channel_id_valid)

    # The authoriserd user isn't an admin
    # VALUE ERROR
    token = token2
    with pytest.raises(ValueError):
        message_utils.message_unpin(token, message_id)

    # Everything valid
    token = token1
    message_utils.message_unpin(token, message_id)

    # Prove that it worked
    channel = channel_utils.get_channel(channel_id_valid)
    assert channel['messages'][0]['is_pinned'] == False

    # Message_id isn't a valid message
    # VALUE ERROR
    token = token1
    bad_message_id = -99
    with pytest.raises(ValueError):
        message_utils.message_unpin(token, bad_message_id)

    # Message id is already unpinned
    # VALUE ERROR
    token = token1
    with pytest.raises(ValueError):
        message_utils.message_unpin(token, message_id)

    pass
