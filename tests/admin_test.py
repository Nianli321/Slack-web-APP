import pytest

from backend import admin, authentication, errors, storage


def test_admin_userpermission_change():
    storage.clear_data_store()

    result = authentication.auth_register(
        'test_admin_userpermission_change_primary@example.com', 'password', 'Randy', 'Random')

    valid_primary_uid = result["u_id"]
    valid_primary_token = result["token"]

    result = authentication.auth_register(
        'test_admin_userpermission_change_user@example.com', 'password', 'Randy', 'Random')

    valid_test_uid = result["u_id"]
    valid_test_token = result["token"]

    # Try update a user's permission levels
    # Set to user level (3)
    with pytest.raises(errors.AccessError):
        admin.admin_userpermission_change(
            "invalid_token", valid_test_uid, 3)

    # Try update a user's permission levels
    # Set to user level (3)
    assert admin.admin_userpermission_change(
        valid_primary_token, valid_test_uid, 3)

    # Set to admin level (2)
    assert admin.admin_userpermission_change(
        valid_primary_token, valid_test_uid, 2)

    # set to owner level (1)
    assert admin.admin_userpermission_change(
        valid_primary_token, valid_test_uid, 1)

    # Test with invalid user id
    with pytest.raises(ValueError):
        admin.admin_userpermission_change(valid_primary_token, -1, 1)

    # Test with an invalid permission id
    with pytest.raises(ValueError):
        admin.admin_userpermission_change(
            valid_primary_token, valid_test_uid, -1)

    # Test access permissions (not at least an admin)
    # Demote the test user to member first
    assert admin.admin_userpermission_change(
        valid_primary_token, valid_test_uid, 3)

    # Should raise AccessError
    with pytest.raises(errors.AccessError):
        assert admin.admin_userpermission_change(
            valid_test_token, valid_primary_uid, 2)

    # Should be unable to modify self permissions (to prevent having no one with admin powers left)
    with pytest.raises(ValueError):
        assert admin.admin_userpermission_change(
            valid_primary_token, valid_primary_uid, 3)

    # Test admin modifying an owner (should raise AccessError)
    assert admin.admin_userpermission_change(
        valid_primary_token, valid_test_uid, 2)

    with pytest.raises(errors.AccessError):
        assert admin.admin_userpermission_change(
            valid_test_token, valid_primary_uid, 3)

    storage.clear_data_store()
