import logging
from keven_core.permissions.abstracts.permission_checker import PermissionChecker


class SystemProcessChecker(PermissionChecker):
    def __init__(self, process_name):
        self.process_name = process_name
        logging.info(
            f"Process: {process_name} is using the permissions "
            f"checker: SystemProcessChecker"
        )

    def check_permission(
        self,
        person_id,
        acting_as_role_id,
        permission_requested: str,
        resource_id,
    ) -> bool:
        return True

    def get_resources_by_permission_name(self, name) -> list:
        pass
