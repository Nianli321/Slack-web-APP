import pytest

from backend import search
from backend import authentication
from backend import channel as channel_utils
from backend import message as message_utils
from backend import storage

def test_search():
    storage.clear_data_store()
    # User to search
    dic1 = authentication.auth_register(
        'valid8@email.com', 'password1', 'Bob', 'James')
    token1 = dic1['token']

    # Second user
    dic2 = authentication.auth_register(
        'valid9@email.com', 'password3', 'Bb', 'Js')
    token2 = dic2['token']

    # channel to search through
    dic = channel_utils.channels_create(token1, 'name', False)
    channel_id_valid = dic['channel_id']

    # Submit messages
    message = "Valid message"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    message = "second message"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    message = "third message"
    message_id = message_utils.message_send(token1, channel_id_valid, message)

    # Messages in the channel
    # Search using a valid token for a query which doesn't exist
    token = token1
    queryString = "hello"
    assert search.search(token, queryString) == []

    token = token1
    queryString = "Va"
    assert search.search(token, queryString)[0]['message'] == "Valid message"

    token = token1
    queryString = " mess"
    assert search.search(token, queryString)[1]['message'] == "second message"

    # Serch using a valid token, without access to the channel where the messages are
    token = token2
    queryString = " mess"
    assert search.search(token, queryString) == []

    # search using an invalid token for a valid string.
    token = "invalid"
    queryString = "wassup"
    with pytest.raises(ValueError):
        search.search(token, queryString)

    # handle whitespace as a query string.
    token = token1
    queryString = "      "
    assert search.search(token, queryString) == []

    # handle 1000 characters - Different words.
    token = token1
    queryString = "Hello There Lorem ipsum dolor sit amet, consectetuer \
    adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. \
    Cum sociis natoque penatibus et magnis dis parturient montes, nascetur \
    ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium \
    quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, \
    aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, \
    venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer \
    tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate \
    eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend \
    ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. \
    Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. \
    Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. \
    Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper\
     libero, sit amet adipiscing sem neque sed ipsum. N"
    with pytest.raises(ValueError):
        search.search(token, queryString)

    # handle 1001 characters - Same letter.
    token = token1
    queryString = "H" * 1001
    with pytest.raises(ValueError):
        search.search(token, queryString)
