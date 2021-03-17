import pytest

from backend import authentication
from backend import user as user_utils
from backend import storage, errors


def test_user_profile():

    storage.clear_data_store()

    # Get valid user's profile
    user = authentication.auth_register(
        'test_user_profile@example.com', 'password', 'Randy', 'Random')

    valid_uid = user["u_id"]
    valid_token = user["token"]

    valid_profile = user_utils.user_profile(valid_token, valid_uid)
    assert "email" in valid_profile and valid_profile["email"]
    assert "name_first" in valid_profile and valid_profile["name_first"]
    assert "name_last" in valid_profile and valid_profile["name_last"]
    assert "handle_str" in valid_profile and valid_profile["handle_str"]

    # Get user profile with an invalid u_id
    invalid_uid = '-1'

    with pytest.raises(ValueError):
        user_utils.user_profile(valid_token, invalid_uid)


def test_user_profile_setname():
    storage.clear_data_store()

    user = authentication.auth_register(
        'test_user_profile@example.com', 'password', 'Randy', 'Random')

    valid_token = user["token"]
    error_token = None

    # Try update a user's name correctly
    assert user_utils.user_profile_setname(valid_token, 'Short', 'Name') == {}
    
    # try with invalid token
    with pytest.raises(errors.AccessError):
         user_utils.user_profile_setname(error_token, 'Short', 'Name')
    # Try update a user's FIRST name to be too long
    with pytest.raises(ValueError):
        user_utils.user_profile_setname(valid_token, 'a' * 51, 'Name')

    # Try update a user's LAST name to be too long
    with pytest.raises(ValueError):
        user_utils.user_profile_setname(valid_token, 'Randy', 'a' * 51)

    # Try update a user's BOTH first and last name to be too long
    with pytest.raises(ValueError):
        user_utils.user_profile_setname(valid_token, 'a' * 51, 'a' * 51)

    # Test with an empty string
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(valid_token, '')


def test_user_profile_setemail():
    storage.clear_data_store()

    user = authentication.auth_register(
        'test_user_profile_setemail@example.com', 'password', 'Randy', 'Random')
    valid_token = user["token"]
    error_token = None

    # Try update a user's email correctly
    assert user_utils.user_profile_setemail(
        valid_token, 'valid@example.com') == {}

    # Try setting an email that already exists
    user = authentication.auth_register(
        'test_user_profile_setemail_duplicate@example.com', 'password', 'Randy', 'Random')
    valid_token = user["token"]
    
    with pytest.raises(errors.AccessError):
        user_utils.user_profile_setemail(
            error_token, 'validemail@example.com')

    with pytest.raises(ValueError):
        user_utils.user_profile_setemail(
            valid_token, 'test_user_profile_setemail_duplicate@example.com')
    
    # Set an email that already exists with leading and trailing whitespace
    with pytest.raises(ValueError):
        user_utils.user_profile_setemail(
            valid_token, ' test_user_profile_setemail_duplicate@example.com   ')

    # Try setting an invalid email (missing @)
    with pytest.raises(ValueError):
        user_utils.user_profile_setemail(valid_token, 'wrong')

    # Try setting an invalid email (empty string)
    with pytest.raises(ValueError):
        user_utils.user_profile_setemail(valid_token, '')
        
        # Try setting an invalid email
    with pytest.raises(ValueError):
        user_utils.user_profile_setemail(valid_token, '     @.com')


def test_user_profile_sethandle():
    storage.clear_data_store()

    user = authentication.auth_register(
        'test_user_profile_sethandle@example.com', 'password', 'Randy', 'Random')
    valid_token = user["token"]
    error_token = None

    # Try update a user's handle correctly
    assert user_utils.user_profile_sethandle(
        valid_token, 'valid@example.com') == {}

    # Test with a handle that is too long (>20 chars)
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(
            valid_token, 'a' * 21)

    # Test with a handle that is already used
    with pytest.raises(errors.AccessError):
        user_utils.user_profile_sethandle(
            error_token, 'validhanlde')
            
     # Test with a handle that is already used
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(
            valid_token, 'valid@example.com')

    # Test with an empty string
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(valid_token, '')
        
        # Test with an Blank
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(valid_token, '     ')
        
         # Test with a handle that already exists but with a space on the end
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(valid_token, 'valid@example.com ')
   
        # Test with a handle that already exists but with more than one space on the end
    with pytest.raises(ValueError):
        user_utils.user_profile_sethandle(valid_token, 'valid@example.com    ')

    storage.clear_data_store()


'''def test_user_profiles_uploadphoto():
    storage.clear_data_store()

    user = authentication.auth_register(
        'test_user_profiles_uploadphoto@example.com', 'password', 'Randy', 'Random')
    valid_token = user["token"]

    # Try upload a photo correctly
    assert user_utils.user_profiles_uploadphoto(
        valid_token, 'https://picsum.photos/id/248/400/400', 0, 0, 300, 300) == {}

    # Try upload a photo with an invalid URI
    with pytest.raises(ValueError):
        user_utils.user_profiles_uploadphoto(
            valid_token, 'wrong', 0, 0, 300, 300) == {}

    # Try upload a photo with crop dimensions bigger than the image dimensions
    with pytest.raises(ValueError):
        user_utils.user_profiles_uploadphoto(
            valid_token, 'https://picsum.photos/id/248/400/400', 0, 0, 100000, 100000) == {}

    # Try upload a photo with negative crop dimensions
    with pytest.raises(ValueError):
        user_utils.user_profiles_uploadphoto(
            valid_token, 'https://picsum.photos/id/248/400/400', -10, 0, 10, 10) == {}'''
