from backend import authentication
from backend import channel as channel_utils


def search(token, query_str):

    data = channel_utils.get_data()
    # Check valid token
    if authentication.decode_token(token) == None:
        raise ValueError("Invalid token provided.")
    u_id = authentication.decode_token(token)["u_id"]

    if len(query_str) > 1000:
        raise ValueError("Messages cannot be more than 1000 characters")

    messages = []

    # find the channels the user is apart of.
    i = 0
    #print(channels['channels'][i]['channel_id'])
    while i < len(data["channels"]):
        j = 0
        if u_id in data["channels"][i]["membersUID"]:
            while j < len(data["channels"][i]["messages"]):
                if query_str in data["channels"][i]["messages"][j]["message"]:
                    messages.append(data["channels"][i]["messages"][j])
                j += 1
        i += 1

    return messages
