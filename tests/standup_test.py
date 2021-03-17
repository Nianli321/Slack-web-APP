import pytest
import datetime

from backend import storage
from backend import standup
from backend import channel as channel_utils
from backend import authentication
from backend import errors


def test_standup_start():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid1@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # set up 2nd user
    dic2 = authentication.auth_register(
        'valid2@email.com', 'password11', 'Bobby', 'Jamesy')
    token2 = dic2['token']

    # Valid token, valid channel_id, but no access:
    usertoken = token2
    channel_id = channel_id_valid
    with pytest.raises(errors.AccessError):
        standup.standup_start(usertoken, channel_id)

    # Valid token, valid channel_id:
    usertoken = token1
    channel_id = channel_id_valid
    time = standup.standup_start(usertoken, channel_id)
    data = channel_utils.get_data()
    assert time < datetime.datetime.now() + datetime.timedelta(minutes=16)
    assert time > datetime.datetime.now() + datetime.timedelta(minutes=14)
    assert time == data["channels"][0]["standup_time"]

    # invalid token, valid channel_id:
    usertoken = "invalidToken"
    channel_id = channel_id_valid
    with pytest.raises(ValueError):
        standup.standup_start(usertoken, channel_id)

    # valid token, invalid channel_id:
    usertoken = token1
    channel_id = 9191
    with pytest.raises(ValueError):
        standup.standup_start(usertoken, channel_id)



def test_standup_send():
    storage.clear_data_store()
    # set up user
    dic1 = authentication.auth_register(
        'valid1@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # creat a valid channel in the name of user1
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # No active standup
    usertoken = token1
    channel_id = channel_id_valid
    message = "No start up"
    with pytest.raises(ValueError):
        standup.standup_send(usertoken, channel_id, message)

    # Start the standup
    standup.standup_start(usertoken, channel_id)

    # Valid token, valid channel_id:
    usertoken = token1
    channel_id = channel_id_valid
    message = "Stand up active"
    standup.standup_send(usertoken, channel_id, message)

    data = channel_utils.get_data()
    assert data["channels"][0]["standup_time"] == data["channels"][0]["messages"][0]["time_created"]

    # Error when Channel does not exist
    message = "Hello There"
    usertoken = "mytoken1234"
    channel_id = 12123  # this is an invalid channel
    with pytest.raises(ValueError):
        standup.standup_send(usertoken, channel_id, message)

    # Error when message > 1000 chars
    message = "H" * 1001
    usertoken = "mytoken1234"
    channel_id = 1
    with pytest.raises(ValueError):
        standup.standup_send(usertoken, channel_id, message)

    # set up 2nd user, which isn't a member of the channel
    dic2 = authentication.auth_register(
        'valid2@email.com', 'password12', 'Boby', 'Jamesy')
    token2 = dic2['token']

    # AccessError if the user is authorised, but not a member of the channel
    message = "Hello There"
    usertoken = token2
    channel_id = channel_id_valid
    with pytest.raises(errors.AccessError):
        standup.standup_send(usertoken, channel_id, message)

    # Error if user doesn't exist
    message = "Hello There"
    usertoken = "mytoken1234"
    channel_id = channel_id_valid
    with pytest.raises(ValueError):
        standup.standup_send(usertoken, channel_id, message)
