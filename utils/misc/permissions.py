from copy import copy

from aiogram import types

default_permissions = {
    "can_send_messages": True,
    "can_send_media_messages": True,
    "can_send_polls": True,
    "can_send_other_messages": True,
    "can_add_web_page_previews": True,
    "can_invite_users": True,
    "can_change_info": False,
    "can_pin_messages": False,
}


async def get_new_user_permissions():
    new_permissions = copy(default_permissions)
    new_permissions.update(
        can_send_messages=True,
        can_send_media_messages=False,
        can_send_polls=False,
        can_send_other_messages=True,
        can_add_web_page_previews=False,
        can_invite_users=False,
        can_change_info=False,
        can_pin_messages=False
    )

    return types.ChatPermissions(**new_permissions)


async def get_user_permissions():
    return types.ChatPermissions(**default_permissions)