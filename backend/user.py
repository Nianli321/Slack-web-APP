''' These functions are repsonsible for the user changing his firstname, lastname,
handle, profile picture and email'''

import re

from backend import authentication, storage, errors

# Load the User Data
# get the path of the file so that we can open it
def get_user_data():
    user_data = storage.load_data_store()

    if "users" in user_data:
        return user_data["users"]

    return None


def user_profile(token, u_id):

    user_data = get_user_data()
    for user in user_data:
        if u_id == user['u_id']:
            return {
                "email": user['email'],
                "name_first": user['first_name'],
                "name_last": user['last_name'],
                "handle_str": user['handle_str']
            }

    raise ValueError("u_id is not a valid user")


# PUT user/profile/setname
# This function sets the first name and the last name of the user
def user_profile_setname(token, name_first, name_last):

    user_index = 0
    index = 0
    new_info = {}
    user_data = get_user_data()

    decoded_token = authentication.decode_token(token)

    if decoded_token is None:
        raise errors.AccessError

    u_id = decoded_token["u_id"]

    # check the length of the firstname and lastname
    # change the name for the profile with the specified token
    if not (authentication.is_valid_first_name(name_first) and authentication.is_valid_last_name(name_last)):
        raise ValueError

    for user in user_data:
        if u_id == user['u_id']:
            index = user_index
            new_info['u_id'] = user['u_id']
            new_info['handle_str'] = user['handle_str']
            new_info['first_name'] = name_first
            new_info['last_name'] = name_last
            new_info['email'] = user['email']
            new_info['hashed_password'] = user['hashed_password']
        user_index = user_index + 1

    update_pickle(index, new_info)

    return {}

# PUT user/profile/setemail
# this function sets the email of the user


def user_profile_setemail(token, email):

    regex = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    user_index = 0
    index = 0
    new_info = {}
    user_data = get_user_data()
    decoded_token = authentication.decode_token(token)

    if decoded_token is None:
        raise errors.AccessError

    u_id = decoded_token["u_id"]

    # remove trailing and leading whitespace
    email = email.strip()
    # check the email is not in use:
    for user in user_data:
        if user['email'] == email:
            raise ValueError("Email address taken")

            # pass the regualar expression
            # and the string in search() method
        if u_id == user['u_id']:
            if re.search(regex, email):
                index = user_index
                new_info['u_id'] = user['u_id']
                new_info['handle_str'] = user['handle_str']
                new_info['first_name'] = user['first_name']
                new_info['last_name'] = user['last_name']
                new_info['email'] = email
                new_info['hashed_password'] = user['hashed_password']
            else:
                raise ValueError("Not a valid Email")
        user_index = user_index + 1

    update_pickle(index, new_info)

    return {}

# PUT user/profile/sethandle
# Throw a ValueError if the handle is already in use
# Throw a ValueError if the handle is < 3 or > 20


def user_profile_sethandle(token, handle_str):
    user_index = 0
    index = 0
    new_info = {}
    user_data = get_user_data()
    decoded_token = authentication.decode_token(token)

    if decoded_token is None:
        raise errors.AccessError

    u_id = decoded_token["u_id"]

    # remove leading and trailing whitespace
    handle_str = handle_str.strip()
    # check the handle is not in use:
    for user in user_data:
        if user['handle_str'] == handle_str:
            raise ValueError("This handle already exists")
        if u_id == user['u_id']:
            if len(handle_str) >= 3 and len(handle_str) <= 20 and not handle_str.isspace():
                index = user_index
                new_info['u_id'] = user['u_id']
                new_info['handle_str'] = handle_str
                new_info['first_name'] = user['first_name']
                new_info['last_name'] = user['last_name']
                new_info['email'] = user['email']
                new_info['hashed_password'] = user['hashed_password']
            else:
                raise ValueError("Invalid handle")
        user_index = user_index + 1

    update_pickle(index, new_info)
    return {}

# This function is completed in Iteration 3

''' Completed in Iteration 3'''
'''def user_profiles_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

    return {}'''


''' This function updates the pickle file to include the modified user info'''


def update_pickle(index, new_info):

    #user_data = get_user_data()
    user_data = storage.load_data_store()
    # delete the input given the index
    del user_data['users'][index]
    # add the new information for that user
    user_data['users'].append(new_info)
    # write to file
    storage.dump_data_store(user_data)
