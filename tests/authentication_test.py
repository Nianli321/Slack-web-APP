"""
Tests authentication functions
"""

import pytest

from backend import authentication, storage


def test_decode_token():
    """
    Tests decoding tokens
    """
    storage.clear_data_store()

    # test for valid token decode
    token = authentication.generate_token(100)
    res = authentication.decode_token(
        token, check_expiry=False)
    assert "u_id" in res and res["u_id"] == 100

    # test for tampered token signature decode
    token = authentication.generate_token(100)
    token = token[:-2] + "AA"
    assert authentication.decode_token(token, check_expiry=False) is None


def test_auth_login():
    """
    Tests login
    """
    storage.clear_data_store()

    # test for an email with no word before the @ symbol
    email = "@938.com"
    password = "1234F"

    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test for an email missing the @ symbol
    email = "myname938.com"
    password = "12345F"
    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test for an email that uses whitespaces as input:
    email = "    @    .com"
    password = "1234F"
    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test for an email missing the .com suffix
    email = "myname938"
    password = "1234F"
    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test an invalid password < len(5)
    email = "hi@938.com"
    password = "1234"

    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test for a password that uses only whitespaces
    email = "hi@938.com"
    password = "      "

    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test for a valid password
    email = "hi@938.com"
    password = "password1"

    with pytest.raises(ValueError):
        authentication.auth_login(email, password)

    # test logining in as a valid user

    # first create the user
    first_name = "Bob"
    last_name = "James"
    email = "valid@email.com"
    password = "password1"
    reg_res = authentication.auth_register(
        email, password, first_name, last_name)
    u_id = reg_res["u_id"]
    token = reg_res["token"]

    # then login as the user
    email = "valid@email.com"
    password = "password1"
    result = authentication.auth_login(email, password)
    # check u_id matches
    assert "u_id" in result and result["u_id"] == u_id
    # check token exists and is NOT the same as the registration token (should have expired)
    assert "token" in result and result["token"] != token

    # Check for wrong password
    with pytest.raises(ValueError):
        authentication.auth_login(email, "NotTheCorrectPassword")


def test_auth_register():
    """
    Tests registering users
    """

    storage.clear_data_store()

    # test an invalid first name and last name > 50 characters
    first_name = "a" * 100
    last_name = "B" * 100
    email = "hi1@938.com"
    password = "1234F"

    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test an invalid first name > 50 characters
    first_name = "a" * 100
    last_name = "B" * 5
    email = "hi1@938.com"
    password = "1234F"

    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test an invalid last name > 50 characters
    first_name = "a" * 5
    last_name = "B" * 100
    email = "hi1@938.com"
    password = "1234F"

    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test an invalid password < len(5)
    first_name = "hello"
    last_name = "hello"
    email = "hi2@938.com"
    password = "1234"
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test an invalid password no characters only numbers
    first_name = "hello"
    last_name = "hello"
    email = "hi3@938.com"
    password = "12345"
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test an invalid password only whitespace
    first_name = "hello"
    last_name = "hello"
    email = "hi4@938.com"
    password = "       "
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # test authenticating a valid user
    first_name = "Bob"
    last_name = "James"
    email = "valid1@email.com"
    password = "password1"
    u_id, token = authentication.auth_register(
        email, password, first_name, last_name)
    assert u_id is not None
    assert token is not None

    storage.clear_data_store()

    # test for invalid email and password, but valid first_name and last_name
    first_name = "Bob"
    last_name = "James"
    email = "        "
    password = "       "
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # create a user with 40 character first name and last name
    first_name = "papappapappapappapappapappapappapappapap"
    last_name = "papappapappapappapappapappapappapappapap"
    email = "valid2@email.com"
    password = "password1"
    u_id, token = authentication.auth_register(
        email, password, first_name, last_name)
    assert u_id is not None
    assert token is not None

    storage.clear_data_store()

    # create an invalid user with a first_name and last_name that contains numbers
    first_name = "pap23"
    last_name = "dragonSlayer55"
    email = "valid3@email.com"
    password = "password1"
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # create an invalid user with a first_name and last_name that symbols
    first_name = "pap@23"
    last_name = "dragonSlayer55!"
    email = "valid4@email.com"
    password = "password1"
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # Use an existing email
    first_name = "test"
    last_name = "test"
    email = "same@email.com"
    password = "password1"
    authentication.auth_register(email, password, first_name, last_name)

    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()

    # Use an invalid email
    first_name = "test"
    last_name = "test"
    email = "notaemail.com"
    password = "password1"
    with pytest.raises(ValueError):
        authentication.auth_register(email, password, first_name, last_name)

    storage.clear_data_store()


def test_auth_logout():
    """
    Tests logout
    """
    storage.clear_data_store()

    # test a simple logout
    email = "valid@email.com"
    first_name = "test"
    last_name = "test"
    password = "password1"
    user = authentication.auth_register(email, password, first_name, last_name)
    token = user["token"]

    assert authentication.auth_logout(token)
    # Should return None because token is expired
    assert authentication.decode_token(user["token"]) is None

    # test logout invalid token
    assert not authentication.auth_logout("invalid")


def test_auth_passwordreset_request():
    """
    Tests password reset request
    """
    storage.clear_data_store()

    # pass a valid email
    email = "valid@email.com"
    first_name = "test"
    last_name = "test"
    password = "password1"
    authentication.auth_register(email, password, first_name, last_name)

    assert authentication.auth_passwordreset_request(email)

    # pass an email with no @ symbol
    email = "validemail.com"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_request(email)

    # pass an email with no .com suffix
    email = "valid@email"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_request(email)

    # Pass an email purely whitespaces
    email = "    @    .com"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_request(email)


def test_auth_passwordreset_reset():
    """
    Tests reset password
    """
    storage.clear_data_store()

    # Test valid code
    email = "valid@email.com"
    first_name = "test"
    last_name = "test"
    password = "password1"
    authentication.auth_register(email, password, first_name, last_name)
    valid_code = authentication.auth_passwordreset_request(email)

    assert authentication.auth_passwordreset_reset(
        valid_code, "new_password") == "new_password"

    storage.clear_data_store()

    # Test invalid code
    email = "valid@email.com"
    first_name = "test"
    last_name = "test"
    password = "password1"
    authentication.auth_register(email, password, first_name, last_name)
    invalid_code = "as980123"

    with pytest.raises(ValueError):
        authentication.auth_passwordreset_reset(invalid_code, "new_password")

    storage.clear_data_store()
    # test invalid password < len(password)
    reset_code = "1234"
    new_password = "1234"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_reset(reset_code, new_password)

    # test invalid password only numebrs no characters
    reset_code = "1234"
    new_password = "12345"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_reset(reset_code, new_password)

    # test password with just whitespace - 6 whitespaces
    reset_code = "1234"
    new_password = "      "
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_reset(reset_code, new_password)

    # test invalid password with just characters
    reset_code = "1234"
    new_password = "abcdefgh"
    with pytest.raises(ValueError):
        authentication.auth_passwordreset_reset(reset_code, new_password)
