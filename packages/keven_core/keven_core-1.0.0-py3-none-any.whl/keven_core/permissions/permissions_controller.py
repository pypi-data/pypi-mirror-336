from __future__ import annotations

import threading
import uuid
from dataclasses import dataclass
from typing import Optional, Dict

from keven_core.exceptions.database import AccessDenied
from keven_core.permissions.actas import ActAsSystem
from keven_core.permissions.user import UserPermissionInfo, UserRole


@dataclass
class AuditData:
    message: str
    permission_string: str
    resource_id: str
    result: bool


def disabled_checker_constructor():
    """
    Returns a PermissionChecker that disables permission checks.
    """
    from keven_core.permissions.abstracts.permission_checker import PermissionChecker

    class DisabledChecker(PermissionChecker):
        def check_permission(self, person_id, role_id, requested, resource_id):
            return True

        def get_resources_by_permission_name(self, name):
            pass

    return DisabledChecker()


class PermissionMetaClass(type):
    """
    Metaclass for implementing thread-safe sessions for the PermissionController.

    This metaclass provides the following key functionality:
      - Ensures that each thread has its own isolated PermissionController session.
      - Manages a stack of stored sessions, enabling temporary session swaps (e.g., via context managers like ActAsUser/ActAsSystem).
      - Provides thread-safe operations for creating, pushing, popping, and clearing sessions.

    Usage & Recommendations:
      - A session should typically represent a single unit of work, such as handling an API call or event.
      - When temporarily elevating or changing permissions (e.g., acting as another user), use push_session/pop_session
        to maintain a clear audit trail and avoid cross-thread contamination.
      - Always clear or properly end sessions after use to prevent stale session data.
      - Use the provided methods (register_permission_checker_constructor, disable_permission_checks, etc.) to configure
        the permission checking behavior system-wide.
    """

    # Magic methods
    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.sessions: Dict[int, PermissionController] = {}
        cls._lock = threading.Lock()
        cls.stored_sessions = {}
        cls.audit_trails = {}
        cls._permission_checker_constructor = None
        cls._permission_checker_args = None
        cls._permission_checker_kwargs = None
        cls.no_commit_mode = False
        cls.default_app_name = ""

    # @property methods
    @property
    def session(cls) -> PermissionController:
        """
        Returns the thread-safe session for checking permissions.
        Initializes a new session if one does not exist for the current thread.
        """
        ident = threading.current_thread().ident
        if ident not in cls.sessions:
            cls.setup_session(ident)
        return cls.sessions[ident]

    # Private methods (non-magic methods starting with double underscore)
    # (None in this class aside from __init__ already above)

    # Regular methods (alphabetical)
    def clear_session_stack(cls):
        """
        Clears the session stack for the current thread and sets up a new session.

        Recommendation:
          Use this to clean up any residual session data that might have been stored during complex permission operations.
        """
        ident = threading.current_thread().ident
        if ident in cls.stored_sessions:
            cls.stored_sessions[ident].clear()
        cls.setup_session(ident)

    def disable_permission_checks(cls):
        """
        Disables permission checks by registering a DisabledChecker.
        """
        cls.register_permission_checker_constructor(disabled_checker_constructor)

    def pop_session(cls):
        """
        Restores the previously saved session from the stack, removing the current session.

        Recommendation:
          Always ensure that every push_session is eventually paired with a pop_session.
        """
        ident = threading.current_thread().ident
        cls.sessions[ident] = cls.stored_sessions[ident].pop()

    def push_session(cls):
        """
        Saves the current session on a stack and creates a new session for the thread.

        Recommendation:
          Use this when temporarily changing the permission context (e.g., for elevated operations).
        """
        ident = threading.current_thread().ident
        session = cls.session
        cls.stored_sessions[ident].append(session)
        checker = cls._permission_checker_constructor(
            *cls._permission_checker_args, **cls._permission_checker_kwargs
        )
        cls.sessions[ident] = PermissionController(ident, checker)

    def register_permission_checker_constructor(cls, func, *args, **kwargs):
        """
        Registers the constructor for the PermissionChecker.

        Args:
            func: A callable that returns a new PermissionChecker instance.
            *args, **kwargs: Additional arguments to be passed to the checker constructor.
        """
        cls._permission_checker_constructor = func
        cls._permission_checker_args = args
        cls._permission_checker_kwargs = kwargs

    def setup_session(cls, ident):
        """
        Sets up a new session for the given thread identifier.
        Initializes stored sessions and audit trails if not already present.
        """
        with cls._lock:
            if ident not in cls.stored_sessions:
                cls.stored_sessions[ident] = []
            if ident not in cls.audit_trails:
                cls.audit_trails[ident] = []
            checker = cls._permission_checker_constructor(
                *cls._permission_checker_args, **cls._permission_checker_kwargs,
            )
            session = PermissionController(ident, checker)
            cls.sessions[ident] = session


class PermissionController(metaclass=PermissionMetaClass):
    """
    Controller for managing permission checks and access to resources.

    This class encapsulates the logic for permission verification using a pluggable PermissionChecker.
    It utilizes thread-local sessions (managed by PermissionMetaClass) to ensure that each thread
    operates in its own isolated permission context.

    Usage & Recommendations:
      - **Accessing the Controller:**
        Do not instantiate directly. Instead, always access the controller via the thread-local session:
            PermissionController.session.user_id = "x-y-z"
      - **Session Lifecycle:**
        A session should correspond to a single unit of work (e.g., an API call, command handler, etc.).
        It is recommended to push/pop or clear sessions appropriately to avoid stale state.
      - **User Setup:**
        Use the setup_user() method to configure the session's user and role. Note that if a role
        is provided as a string, it is automatically wrapped in a UserRole instance.
      - **Permission Checks:**
        Permission checks can be immediate or deferred. The controller records deferred checks (when delayed_checking is enabled)
        and performs a final check (via final_check) before completing the work.
      - **Audit Trail:**
        Every significant action (e.g., user changes, permission checks) is logged in the audit trail.
        This is crucial for maintaining a detailed record of access for sensitive data.

    Note:
      When temporarily elevating privileges (e.g., acting as another system user), consider using
      the provided context managers (e.g., ActAsUser, ActAsSystem) to ensure that sessions and audit trails are managed correctly.
    """

    # Magic methods
    def __init__(self, ident, checker):
        self.__strict = False
        self.__user_id = ""
        self.__user_info: Optional[UserPermissionInfo] = None
        self.__acting_as_role_id = ""
        self.__language_override = None
        self.__audit_trail = []
        self.session_id = str(uuid.uuid4())
        self.add_audit_event(f"Creating session: {self.session_id}")
        self.checker = checker
        self.account_recovery = False
        self.in_check = False
        self.resources_requested = {}
        self.__in_final_check = False
        self.containing_action = ""
        self.delayed_checking = True
        self.skip_final_checks = False
        self.cache = {}
        self.app_name = self.default_app_name
        self.allowed_calls = None

    # @property methods
    @property
    def acting_as_role_id(self):
        return self.__acting_as_role_id

    @acting_as_role_id.setter
    def acting_as_role_id(self, value):
        self.add_audit_event(f"Acting as user role: {value}")
        self.__acting_as_role_id = value

    @property
    def in_final_check(self):
        return self.__in_final_check

    @property
    def language_override(self):
        return self.__language_override

    @language_override.setter
    def language_override(self, value):
        self.add_audit_event(f"Language override: {value}")
        self.__language_override = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        self.add_audit_event(f"Acting as user: {value}")
        self.__user_id = value

    # Private methods
    def __does_user_have_permission(
            self, resource_id: any, permission_name: str, p_user_id: any = None
    ) -> bool:
        """
        Checks access for a specific resource.

        Args:
            resource_id: The ID of the resource.
            permission_name: The permission being requested.
            p_user_id: Optional user ID to check (useful with ActAsSystem).

        Returns:
            True if access is granted, False otherwise.

        Behavior:
            - If resource_id is false, if a final check is in progress, or if delayed
              checking is disabled, an immediate permission check is performed.
            - Otherwise, the permission request is recorded for deferred checking.
        """
        if not resource_id or self.__in_final_check or not self.delayed_checking:
            res = self.checker.check_permission(
                p_user_id or self.__user_id,
                self.__acting_as_role_id,
                permission_name,
                resource_id,
            )
            self.add_audit_event(
                f"Check Access '{permission_name}' for (user_id: {p_user_id or self.user_id}) to ({resource_id})",
                permission_string=permission_name,
                resource_id=resource_id,
                result=res,
            )
        else:
            if resource_id not in self.resources_requested:
                self.resources_requested[resource_id] = set()
            self.resources_requested[resource_id].add(permission_name)
            res = True

        return res

    # Regular methods (alphabetical)
    def add_audit_event(self, message, permission_string="", resource_id="", result=False):
        """
        Records an audit event with a message and additional permission details.
        """
        self.__audit_trail.append(
            AuditData(
                message=message,
                permission_string=permission_string,
                resource_id=resource_id,
                result=result,
            )
        )

    def does_user_have_permission(
            self, resource_id: any, permission_name: str, p_user_id: any = None
    ) -> bool:
        """
        Determines if the user has permission for a specific resource.
        If not in final check, performs an immediate permission check.
        """
        if not self.__in_final_check:
            return self.__does_user_have_permission(resource_id, permission_name, p_user_id)
        return False

    def final_check(self, session):
        """
        Performs deferred permission checks for all recorded resource requests.
        Uses an ActAsSystem context to ensure elevated permissions during final validation.
        Raises AccessDenied if any check fails.
        """
        with ActAsSystem("Check Permissions", session):
            self.__in_final_check = True
            if not self.skip_final_checks:
                for resource_id, permissions in self.resources_requested.items():
                    for permission in permissions:
                        if not self.__does_user_have_permission(resource_id, permission, p_user_id=None):
                            raise AccessDenied(f"Permission: {permission}, Resource: {resource_id}")
            self.log_audit_messages()
            self.__in_final_check = False

    def has_permission_name(self, permission_name: str):
        """
        Checks if the user's permission info includes a specific permission.
        """
        return permission_name in self.__user_info.permissions

    def log_audit_messages(self):
        """
        Logs all audit events using the system's event logging mechanism.
        """
        from keven_core.kafka.events.event import Event, EventNames

        event = Event.from_name(EventNames.SESSION_AUDIT_LOG)
        for audit in self.__audit_trail:
            log = event.details.add()
            log.session_id = self.session_id
            log.containing_action = self.containing_action
            log.message = audit.message
            log.user_id = self.user_id
            log.acting_as_role_id = self.acting_as_role_id
            log.resource_id = audit.resource_id
            log.permission_string = audit.permission_string
            log.result = audit.result

    def must_have_permission(self, permission: str, resource: any):
        """
        Ensures that the user has the required permission for a resource.
        Raises AccessDenied if the check fails.
        """
        if not self.does_user_have_permission(resource, permission):
            raise AccessDenied("You do not have the required permission for the resource")

    def print_audit_trail(self):
        """
        For debugging purposes: prints the current audit trail.
        """
        print("\n*****   RESPONSE AUDIT TRAIL   *****")
        for resource in self.__audit_trail:
            print(resource)
        print("***** END RESPONSE AUDIT TRAIL *****\n")

    def setup_user(self, user_id, act_as_role_id=None, user_permission_info: Optional[UserPermissionInfo] = None):
        """
        Sets up the current session's user details.

        Args:
            user_id: The ID of the current user.
            act_as_role_id: The role ID under which the user is acting.
                If provided as a string, it will be wrapped as a UserRole.
            user_permission_info: Optional detailed permission info for advanced checking.

        Note:
            If user_permission_info is not provided, a new UserPermissionInfo is created
            with the provided user_id and act_as_role_id.
        """
        self.user_id = user_id
        self.acting_as_role_id = act_as_role_id
        if user_permission_info is None:
            roles = []
            if act_as_role_id is not None:
                roles = [UserRole(id=str(act_as_role_id), name=str(act_as_role_id))]
            user_permission_info = UserPermissionInfo(
                user_id=user_id,
                roles=roles,
                permissions=set()
            )
        self.__user_info = user_permission_info

    def user_has_permission(self, permission_name: str, user_id=None) -> bool:
        """
        Checks if the current (or specified) user has the given permission.
        """
        return self.checker.check_permission(
            user_id or self.__user_id,
            self.__acting_as_role_id,
            permission_name,
            None,
        )
