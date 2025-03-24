from sqlalchemy import event
from keven_core.permissions.permissions_controller import PermissionController

from keven_core.exceptions import (
    ReadAccessDenied,
    CreateAccessDenied,
    UpdateAccessDenied,
    DeleteAccessDenied,
)


def restricted_model(_cls=None, resource_name=None):
    """
    A Class decorator which restricts access to a SQLAlchemy Data Model.  This
    does not restrict access to individual objects / records
    :param _cls: internal
    :param resource_name: The name of the resource.  Defaults to the Class name

    Your model will receive the following additional methods:

    Class methods (to be used before attempting to load a resource)
    -------------
    All of the functions below return a bool response.

    has_read_access()
    has_update_access()
    has_delete_access()
    has_create_access()

    Instance Methods
    ----------------
    All of the functions return a bool response. The user_id
    parameter is optional.

    can_read(user_id=None)
    can_update(user_id=None)
    can_delete(user_id=None)

    """

    """
    The following functions are attached to the SQLAlchemy class to allow for
    model access checking on each instance. 
    """

    def can_create(self, user_id=None):
        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.create", user_id
        )

    def can_read(self, user_id=None):
        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.read", user_id
        )

    def can_read_field(
            self,
            field_name,
            user_id=None,
            raise_exception_on_false=False,
    ):
        res = PermissionController.session.user_has_permission(
            f"{self.__resource_name}.{field_name}.read", user_id
        )

        if not raise_exception_on_false or res:
            return res
        else:
            raise ReadAccessDenied(f"{self.__resource_name}.{field_name}")

    def can_update(self, user_id=None):

        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.update", user_id
        )

    def can_update_field(self, field_name, user_id=None):
        if field_name[0] == "_":
            field_name = field_name[1:]
        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.{field_name}.update",
            user_id,
        )

    def can_delete(self, user_id=None):
        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.delete", user_id
        )

    """
    These functions are the event handlers which are registered with SQLAlchemy
    """

    def on_load(target, context):
        if not target.can_read():
            raise ReadAccessDenied(f"{target.__class__.__name__}")

    def on_refresh(target, context, attrs):
        on_load(target, context)

    def on_modify(target, value, oldvalue, initiator):
        if not target._sa_instance_state.has_identity:
            if not target.can_create():
                raise CreateAccessDenied(target.__resource_name)

        elif not target.can_update() and not target.can_update_field(
                initiator.key
        ):
            raise UpdateAccessDenied(f"{target.__class__.__name__}")

    def on_before_delete(mapper, connection, target):
        if not target.can_delete():
            raise DeleteAccessDenied(f"{target.__class__.__name__}")

    def model_decorator(cls):
        """
        Enhance the SQLAlchemy class with our permissions checking methods
        """
        setattr(cls, "__resource_name", resource_name or cls.__name__)
        setattr(cls, "has_read_access", classmethod(can_read))
        setattr(cls, "has_update_access", classmethod(can_update))
        setattr(cls, "has_delete_access", classmethod(can_delete))
        setattr(cls, "has_create_access", classmethod(can_create))

        setattr(cls, "can_read", can_read)
        setattr(cls, "can_read_field", can_read_field)
        setattr(cls, "can_update", can_update)
        setattr(cls, "can_update_field", can_update_field)
        setattr(cls, "can_create", can_create)
        setattr(cls, "can_delete", can_delete)

        event.listen(cls, "load", on_load)
        event.listen(cls, "refresh", on_refresh)
        event.listen(cls, "before_delete", on_before_delete)
        for attr in cls._sa_class_manager.local_attrs:
            attribute = getattr(cls, attr)
            event.listen(attribute, "set", on_modify)

        return cls

    if _cls is None:
        return model_decorator
    else:
        return model_decorator(_cls)


def unrestricted_model(cls):
    """
    A class decorator for auditing which models are unrestricted
    """

    """
    The following functions are attached to the SQLAlchemy class to allow for
    model access checking on each instance. 

    print(unrestricted_model.models) to see the list of models
    """
    if not hasattr(unrestricted_model, "models"):
        unrestricted_model.models = list()
    unrestricted_model.models.append(cls.__name__)
    return cls
