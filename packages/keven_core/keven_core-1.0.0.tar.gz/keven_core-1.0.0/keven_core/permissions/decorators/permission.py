import functools

from keven_core.exceptions import AccessDenied
from keven_core.permissions.permissions_controller import PermissionController


def permission(permission_name: str, account_recovery=False):
    """
    Use this decorator to protect functions.  This ensures that the correct
    permission has been granted to the current user.
    """

    def permission_decorator(func):
        @functools.wraps(func)
        def permission_wrapper(*args, **kwargs):
            if (
                PermissionController.session.account_recovery
                and not account_recovery
            ):
                raise AccessDenied(permission_name)

            if not PermissionController.session.user_has_permission(
                permission_name
            ):
                raise AccessDenied(permission_name)
            return func(*args, **kwargs)

        setattr(permission_decorator, "__permission_name", permission_name)
        return permission_wrapper

    return permission_decorator
