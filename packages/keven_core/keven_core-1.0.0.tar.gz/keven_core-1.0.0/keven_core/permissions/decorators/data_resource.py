import inspect

from sqlalchemy import event
from sqlalchemy.ext.hybrid import hybrid_property

from keven_core.exceptions.database import (
    ReadAccessDenied,
    CreateAccessDenied,
    UpdateAccessDenied,
    DeleteAccessDenied
)
from keven_core.permissions.actas import ActAsSystem
from keven_core.permissions.permissions_controller import PermissionController



class RestrictedList(object):
    def __init__(self, list_name, data_object):
        self.list_name = list_name
        self.data_object = data_object

    def restricted_list(self, data_object=None):
        return self.data_object.restricted_list(self.list_name)


def restricted_resource(_cls=None, resource_id_field=None, resource_name=None):
    """
    A Class decorator which restricts access to a SQLAlchemy Data object
    :param _cls: internal
    :param resource_id_field: The name of the field containing the resources
    unique id.  Defaults to 'id'
    :param resource_name: The name of the resource.  Defaults to the Class name

    Your model will receive the following additional methods:

    Class methods (to be used before attempting to load a resource)
    -------------
    All of the functions below return a bool response.

    has_read_access(resource_id)
    has_update_access(resource_id)
    has_delete_access(resource_id)
    has_create_access

    Instance Methods
    ----------------
    All of the functions return a bool response. The user_id
    parameter is optional.

    can_read(user_id=None)
    can_update(user_id=None)
    can_delete(user_id=None)

    Other Instance Methods
    -----------------------
    restricted_list(collection_name) - Returns a list of objects in a
    collection that the user has read access to.  collection_name is a string
    which is the name of the collection attribute on the class.


    """

    """
    The following functions are attached to the SQLAlchemy class to allow for
    resource access checking on each instance. 
    """

    def can_create(self):
        return PermissionController.session.user_has_permission(
            f"{self.__resource_name}.create", None
        )

    def can_read(self, user_id=None, resource_id=None):
        _id = resource_id if inspect.isclass(self) else self.get_resource_id()
        return PermissionController.session.does_user_have_permission(
            _id, f"{self.__resource_name}.read", user_id
        )

    def can_read_field(
        self,
        field_name,
        user_id=None,
        resource_id=None,
        raise_exception_on_false=False,
    ):
        _id = resource_id if inspect.isclass(self) else self.get_resource_id()
        res = PermissionController.session.does_user_have_permission(
            _id, f"{self.__resource_name}.{field_name}.read", user_id
        )

        if not raise_exception_on_false or res:
            return res
        else:
            raise ReadAccessDenied(
                f"{self.__resource_name}.{field_name}:" f"{_id}"
            )

    def can_update(self, user_id=None, resource_id=None):
        _id = resource_id if inspect.isclass(self) else self.get_resource_id()

        return PermissionController.session.does_user_have_permission(
            _id, f"{self.__resource_name}.update", user_id
        )

    def can_update_field(self, field_name, user_id=None):
        if field_name[0] == "_":
            field_name = field_name[1:]
        return PermissionController.session.does_user_have_permission(
            self.get_resource_id(),
            f"{self.__resource_name}.{field_name}.update",
            user_id,
        )

    def can_delete(self, user_id=None):
        return PermissionController.session.does_user_have_permission(
            self.get_resource_id(), f"{self.__resource_name}.delete", user_id
        )

    def get_resource_id(self):
        return getattr(self, self.__resource_id)

    def has_read_access(cls, resource_id, user_id=None):
        return PermissionController.session.does_user_have_permission(
            resource_id, f"{cls.__resource_name}.read", user_id
        )

    def has_update_access(cls, resource_id, user_id=None):
        return PermissionController.session.does_user_have_permission(
            resource_id, f"{cls.__resource_name}.read", user_id
        )

    def has_delete_access(cls, resource_id, user_id=None):
        return PermissionController.session.does_user_have_permission(
            resource_id, f"{cls.__resource_name}.read", user_id
        )

    def has_create_access(cls, user_id=None):
        return PermissionController.session.user_has_permission(
            f"{cls.__resource_name}.create", user_id
        )

    def restricted_list(self, collection_name=""):
        with ActAsSystem(
            f"restricted_list {collection_name}",
            self._sa_instance_state.session,
        ) as user_id:
            result = [
                itm
                for itm in getattr(self, collection_name)
                if itm.can_read(user_id)
            ]
        return result

    """
    These functions are the event handlers which are registered with SQLAlchemy
    """

    def on_load(target, context):
        if PermissionController.session.in_check:
            return

        PermissionController.session.in_check = True
        try:
            for attr in target._sa_class_manager.local_attrs:
                attribute = target._sa_class_manager[attr]
                if (
                    hasattr(attribute.prop, "uselist")
                    and attribute.prop.uselist
                ):
                    setattr(
                        target,
                        f"masked_{attr}",
                        RestrictedList(attr, target).restricted_list,
                    )

            if not target.can_read():
                raise ReadAccessDenied(
                    f"{target.__class__.__name__}:"
                    f"{target.get_resource_id()}"
                )
        finally:
            PermissionController.session.in_check = False

    def on_refresh(target, context, attrs):
        on_load(target, context)

    def on_modify(target, value, oldvalue, initiator):
        if PermissionController.session.in_check:
            return

        PermissionController.session.in_check = True
        try:
            if not target._sa_instance_state.has_identity:
                if not PermissionController.session.user_has_permission(
                    f"{target.__resource_name}.create"
                ):
                    raise CreateAccessDenied(target.__resource_name)

            elif not target.can_update() and not target.can_update_field(
                initiator.key
            ):
                raise UpdateAccessDenied(
                    f"{target.__class__.__name__}:"
                    f"{target.get_resource_id()}"
                )
        finally:
            PermissionController.session.in_check = False

    def on_before_delete(mapper, connection, target):
        if PermissionController.session.in_check:
            return

        PermissionController.session.in_check = True
        try:
            if not target._can_delete():
                raise DeleteAccessDenied(
                    f"{target.__class__.__name__}:"
                    f"{target.get_resource_id()}"
                )
        finally:
            PermissionController.session.in_check = False

    def resource_decorator(cls):
        """
        Enhance the SQLAlchemy class with our permissions checking methods
        """
        for attr in cls._sa_class_manager.local_attrs:
            attribute = getattr(cls, attr)
            event.listen(attribute, "set", on_modify)

        setattr(cls, "__resource_id", resource_id_field or "id")
        setattr(cls, "__resource_name", resource_name or cls.__name__)
        cls.get_resource_id = get_resource_id
        setattr(cls, "has_read_access", classmethod(has_read_access))
        setattr(cls, "has_update_access", classmethod(has_update_access))
        setattr(cls, "has_delete_access", classmethod(has_delete_access))
        setattr(cls, "has_create_access", classmethod(has_create_access))

        setattr(cls, "can_read", can_read)
        setattr(cls, "can_read_field", can_read_field)
        setattr(cls, "can_update", can_update)
        setattr(cls, "can_update_field", can_update_field)
        setattr(cls, "can_create", can_create)
        setattr(cls, "_can_delete", can_delete)
        setattr(cls, "restricted_list", restricted_list)

        event.listen(cls, "load", on_load)
        event.listen(cls, "refresh", on_refresh)
        event.listen(cls, "before_delete", on_before_delete)

        return cls

    if _cls is None:
        return resource_decorator
    else:
        return resource_decorator(_cls)


class restricted_property(hybrid_property):
    def __get__(self, instance, owner):
        if not instance:
            return super().__get__(instance, owner)
        else:
            if instance.can_read_field(
                self.fget.__name__, raise_exception_on_false=True
            ):
                return super().__get__(instance, owner)


class masked_property(hybrid_property):
    def __get__(self, instance, owner):
        if not instance:
            return super().__get__(instance, owner)
        else:
            if instance.can_read_field(self.fget.__name__):
                return super().__get__(instance, owner)
        return None
