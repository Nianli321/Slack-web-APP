"""
Admin related functions
"""

from backend import authentication, errors, storage
from backend.authentication import SlackrPermissions

VALID_ADMIN_LEVELS = (SlackrPermissions.OWNER.value,
                      SlackrPermissions.ADMIN.value)


def admin_userpermission_change(token, u_id, permission_id):
    """
    Changes the permission level for a user
    """

    # check for valid users
    decoded_token = authentication.decode_token(token)
    if decoded_token is None:
        raise errors.AccessError("Not a valid user")

    # check for valid permission_id
    if not permission_id in set(perm.value for perm in SlackrPermissions):
        raise ValueError("Not a valid permission_id")

    admin_id = decoded_token["u_id"]
    data = authentication.get_auth_store()

    user_to_change = None

    # Get user and admin levels
    for user_index, user in enumerate(data["users"]):
        if user["u_id"] == admin_id:
            admin = user

        if user["u_id"] == u_id:
            user_to_change = user_index

    # check if user exists
    if user_to_change is None:
        raise ValueError("Unknown user to modify")

    # check if modifying their own permissions (to avoid getting stuck with no one with permissions)
    if admin["u_id"] == data["users"][user_to_change]["u_id"]:
        raise ValueError("Can't modify own permissions")

    # check if level is either admin or owner
    if admin["permission_id"] not in VALID_ADMIN_LEVELS:
        raise errors.AccessError("Not a valid owner or admin")

    # check if is another owner if modifying an owner
    if (admin["permission_id"] != SlackrPermissions.OWNER.value
            and data["users"][user_to_change]["permission_id"] == SlackrPermissions.OWNER.value):
        raise errors.AccessError("Admins cannot change a owner's permission")

    data["users"][user_to_change]["permission_id"] = permission_id

    storage.dump_data_store(data)

    return True
