from abc import ABC, abstractmethod


class PermissionChecker(ABC):
    """
    Interface for permissions checkers
    """

    @abstractmethod
    def check_permission(
        self,
        person_id,
        acting_as_role_id,
        permission_requested: str,
        resource_id,
    ) -> bool:
        pass

    @abstractmethod
    def get_resources_by_permission_name(self, name) -> list:
        pass

