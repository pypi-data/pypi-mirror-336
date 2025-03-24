import inspect
import uuid

from keven_core.kafka.events.event import Event, EventNames


class ActAsUser:
    """
    When entering and exiting the block the current session is scrubbed.
    Any objects accessed inside the block should be disregarded and not
    accessed outside of it.
    """

    def __init__(self, reason: str, db_session, user_id, role_id):
        self.initial_user_id = ""
        self.parent_locals = set()
        self.reason = reason
        self.id = uuid.uuid4().__str__()
        self.db_session = db_session
        self.user_id = user_id
        self.role_id = role_id

    def __enter__(self):
        """
        Saves the current session and creates a new one.  It expires all
        SQLAlchemy objects in the current session.  It returns the previous
        sessions user id.
        """
        from keven_core.kafka.events.logger import keven_log_event
        from keven_core.permissions.permissions_controller import PermissionController

        parent = inspect.stack()[1]
        for local in parent[0].f_locals:
            self.parent_locals.add(local)

        self.initial_user_id = PermissionController.session.user_id
        PermissionController.push_session()
        PermissionController.session.user_id = self.user_id
        PermissionController.session.acting_as_role_id = self.role_id
        self.db_session.expire_all()

        if self.reason != "Load user for session":
            event = Event.from_name(EventNames.ACT_AS_USER)
            event.details.reason = self.reason
            event.details.user_id = self.initial_user_id
            event.details.acting_as_user_id = self.user_id
            event.details.acting_as_role_id = self.role_id
            keven_log_event(event)
        return self.initial_user_id

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Restores the previous Permission session and expires all SQLAlchemy
        objects to ensure permissions are rechecked.
        """
        from keven_core.permissions.permissions_controller import PermissionController

        PermissionController.session.add_audit_event(
            f"ActingAsUser({self.id}): Exiting"
        )
        PermissionController.pop_session()
        self.db_session.expire_all()


class ActAsSystem(ActAsUser):
    """
    When entering and exiting the block the current session is scrubbed.
    Any objects accessed inside the block should be disregarded and not
    accessed outside of it.
    """

    def __init__(self, reason: str, db_session):
        super().__init__(reason, db_session, "System", "SystemRole")
