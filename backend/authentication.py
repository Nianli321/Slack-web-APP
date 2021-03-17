"""
Authentication functions for slackr
"""

import hashlib
import re
import secrets
from random import randint
from enum import Enum

import jwt

from backend import storage, utils

JWT_SECRET = "lUw6cdFG#89RV"
MAX_HANDLE_LEN = 20


class SlackrPermissions(Enum):
    """
    Global permission levels for Slackr
    """
    OWNER = 1
    ADMIN = 2
    MEMBER = 3


def decode_token(token, check_expiry=True):
    """
    Tries decoding the token using the JWT secret
    On failure/decoding an expired token it returns None
    """
    data = get_auth_store()
    valid_tokens = data["tokens"].values()

    try:
        decoded_res = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.InvalidTokenError:
        return None

    if not check_expiry or token in valid_tokens:
        return decoded_res

    return None


def is_duplicate_handle(handle, users):
    """
    Checks if the handle given is a duplicate
    """
    for user in users:
        if user["handle_str"] == handle:
            return True

    return False


def is_valid_first_name(first_name):
    """
    Validity checks for first names
    """
    # Inclusive - uses chained comparision operators
    valid_len = 1 <= len(first_name) <= 50
    return valid_len and first_name.isalpha()


def is_valid_last_name(last_name):
    """
    Validity checks for last names
    Kept distinct from is_valid_first_name to reduce refactor if spec changes
    """
    # Inclusive - uses chained comparision operators
    valid_len = 1 <= len(last_name) <= 50
    return valid_len and last_name.isalpha()


def is_valid_password(password):
    """
    Validity checks for passwords
    """
    return len(password) >= 6 and not password.isspace()


def is_valid_email(email):
    """
    Checks if email is valid
    From https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/
    """
    result = re.match(r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$", email)
    return result is not None


def is_registered_email(email, users):
    """
    Checks if the email is registered
    """
    for user in users:
        if user["email"] == email:
            return True
    return False


def hash_password(password):
    """
    Hashes a password and returns the hex digest
    """
    return hashlib.sha256(password.encode()).hexdigest()


def get_auth_store():
    """
    Returns the data store, specifically creating the users list if it doesn't exist
    """
    data_store = storage.load_data_store()
    if "users" not in data_store:
        data_store["users"] = []

    if "tokens" not in data_store:
        data_store["tokens"] = {}

    if "reset_codes" not in data_store:
        data_store["reset_codes"] = {}

    return data_store


def generate_token(u_id):
    """
    Generates a UTF-8 string representation of a JWT token
    """
    return jwt.encode(
        {
            "u_id": u_id,
            "nonce": secrets.token_urlsafe(64)
        },
        JWT_SECRET,
        algorithm="HS256"
    ).decode("utf-8")


def generate_reset_code():
    """
    Generates a random reset code
    """
    return secrets.token_urlsafe(16)


def _generate_uid():
    """
    Generates a new unique user ID (> 32 bit integer sufficient for avoiding collisions)
    """
    return utils.generate_luid()


def _generate_random_tag(handle, factor):
    """
    Generates a random tag to append to the handle
    E.g.
    gordonzho#123
    """
    tag = '#' + " ".join(str(randint(0, 9)) for i in range(factor))

    # It is safe to slice the string in this way - in the extreme case of the tag length being
    # longer than the handle itself, the handle slice will return an empty string
    randomised_handle = handle[:-len(tag)] + tag

    return randomised_handle[:MAX_HANDLE_LEN]


def _generate_handle(first_name, last_name, users):
    """
    Generates a new handle and generates a random tag if it already exists
    """

    handle = (first_name.lower() + last_name.lower())[:MAX_HANDLE_LEN]
    uniqueness_factor = 1

    while is_duplicate_handle(handle, users):
        handle = _generate_random_tag(handle, uniqueness_factor)
        uniqueness_factor += 1

    return handle


def auth_login(email, password):
    """
    Given a registered users' email and password and generates a valid token for the user to remain authenticated
    """

    if not is_valid_email(email):
        raise ValueError("Invalid email given")

    data = get_auth_store()
    users = data["users"]
    valid_tokens = data["tokens"]
    new_token = None
    u_id = None

    for user in users:
        if user["email"] == email:
            if user["hashed_password"] == hash_password(password):
                u_id = user["u_id"]
                new_token = generate_token(u_id)
                valid_tokens[user["email"]] = new_token

            else:
                raise ValueError("Gave incorrect password for given email")

    # Couldn't find user
    if new_token is None:
        raise ValueError("Couldn't find a user with that email")

    storage.dump_data_store(data)

    return {
        "u_id": u_id,
        "token": new_token
    }


def auth_logout(token):
    """
    Given an active token, invalidates the taken to log the user out.
    If a valid token is given, and the user is successfully logged out, it returns true, otherwise false.
    """
    data = get_auth_store()
    email_to_logout = None

    for email, valid_token in data["tokens"].items():
        if token == valid_token:
            email_to_logout = email

    if email_to_logout is not None:
        data["tokens"].pop(email_to_logout, None)
        storage.dump_data_store(data)
        return True

    return False


def auth_register(email, password, name_first, name_last):
    """
    Given a user's first and last name, email address, and password,
    create a new account for them and return a new token for authentication in their session.
    A handle is generated that is the concatentation of a lowercase-only first name and last name.
    If the concatenation is longer than 20 characters, it is cutoff at 20 characters.
    If the handle is already taken, you may modify the handle in any way you see fit to make it
    unique.
    """
    data = get_auth_store()
    users = data["users"]
    valid_tokens = data["tokens"]

    if not is_valid_first_name(name_first):
        raise ValueError("Gave an invalid first name")

    if not is_valid_last_name(name_last):
        raise ValueError("Gave an invalid last name")

    if not is_valid_password(password):
        raise ValueError("Gave an invalid password")

    if not is_valid_email(email):
        raise ValueError("Gave an invalid email")

    if is_registered_email(email, users):
        raise ValueError("Gave an already taken email")

    u_id = _generate_uid()
    permission_id = SlackrPermissions.MEMBER.value
    if not users:
        permission_id = SlackrPermissions.OWNER.value

    token = generate_token(u_id)
    handle_str = _generate_handle(name_first, name_last, users)

    data["users"].append({
        "u_id": u_id,
        "handle_str": handle_str,
        "first_name": name_first,
        "last_name": name_last,
        "permission_id": permission_id,
        "email": email,
        "hashed_password": hash_password(password)
    })

    valid_tokens[email] = token

    storage.dump_data_store(data)

    return {
        "u_id": u_id,
        "token": token
    }


def auth_passwordreset_request(email):
    """
    Given an email address, if the user is a registered user, send's them a an email containing a specific secret code,
    that when entered in auth_passwordreset_reset, shows that the user trying to reset the password is the one who got
    sent this email.

    The Flask app must actually send the email - this function does the rest of the work of generating the reset code
    """

    if not is_valid_email(email):
        raise ValueError("Gave an invalid email to send a password reset to")

    data = get_auth_store()
    reset_code = None
    for user in data["users"]:
        if user["email"] == email:
            reset_code = generate_reset_code()
            data["reset_codes"][reset_code] = email

    storage.dump_data_store(data)

    return reset_code


def auth_passwordreset_reset(reset_code, new_password):
    """
    Given a reset code for a user, set that user's new password to the password provided
    """
    if not is_valid_password(new_password):
        raise ValueError("Invalid password given")

    data = get_auth_store()

    email_to_reset = None

    if reset_code in data["reset_codes"]:
        email_to_reset = data["reset_codes"][reset_code]

    if email_to_reset is None:
        raise ValueError("No such reset code")

    for user in data["users"]:
        if user["email"] == email_to_reset:
            data["reset_codes"].pop(reset_code, None)
            user["hashed_password"] = hash_password(new_password)

    storage.dump_data_store(data)
    return new_password
