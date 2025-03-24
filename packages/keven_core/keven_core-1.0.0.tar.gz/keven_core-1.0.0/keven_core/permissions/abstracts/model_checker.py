from abc import ABC, abstractmethod

from keven_core.exceptions.code import ClassConfiguration
import logging


class ModelChecker(ABC):
    """
    Base your model checker on this and pass it into the @restricted_model
    decorator
    """

    def __init__(
        self, person_id, acting_as_role_id, resource_id, data_model_class_name
    ):
        self.person_id = person_id
        self.role_id = acting_as_role_id
        self.resource_id = resource_id
        self.data_model_class_name = data_model_class_name

    @abstractmethod
    def create(self) -> bool:
        pass

    @abstractmethod
    def read(self) -> bool:
        pass

    @abstractmethod
    def update(self) -> bool:
        pass

    @abstractmethod
    def delete(self) -> bool:
        pass

    def access_event(self, event_name):
        logging.verbose(
            "ACCESS EVENT: "
            f"{self.data_model_class_name} {event_name} {self.resource_id}"
        )

    @abstractmethod
    def get_resource(self) -> object:
        pass

    @property
    def resource(self):
        return self.get_resource()


class ModelCheckerRegistry:
    """
    This is the internal registry for model checker classes.
    """

    _registry = dict()

    @classmethod
    def _session(cls):
        return None

    @classmethod
    def register_checker(
        cls, checker_class, data_model_class, role_class=None
    ):
        if role_class is None:
            key = data_model_class.__name__
        else:
            key = f"{data_model_class.__name__}-{role_class.__name__}"
        if not cls._registry.get(key):
            cls._registry[key] = [checker_class]
        else:
            cls._registry[key].append(checker_class)

    @classmethod
    def register_checker_for_class_list(
        cls, checker_class, role_class, class_list
    ):
        for model_class in class_list:
            cls.register_checker(
                checker_class, model_class, role_class=role_class
            )

    @classmethod
    def check_permission(
        cls,
        person_id,
        acting_as_role_id,
        permission_requested: str,
        resource_id,
    ) -> bool:
        checkers = list()
        fields = permission_requested.split(".")
        data_model_class_name = fields[0]
        operation = fields[-1]

        # Generic class first
        checker_class = cls._registry.get(data_model_class_name)
        if checker_class:
            checkers.extend(checker_class)

        role_names = []
        if rn := cls.get_role_name(acting_as_role_id):
            role_names.append(rn)

        if hasattr(cls, "get_role_names"):
            role_names.extend(cls.get_role_names(person_id))

        for role_name in role_names:
            role_key = f"{data_model_class_name}-{role_name}"
            checker_class = cls._registry.get(role_key)
            if checker_class:
                checkers.extend(checker_class)

        if len(checkers) == 0:
            raise ClassConfiguration(
                f"Data model permission checker class:"
                f" {data_model_class_name} not found"
            )

        granted = False

        for checker_class in checkers:
            checker: ModelChecker = checker_class(
                person_id,
                acting_as_role_id,
                resource_id,
                data_model_class_name,
            )

            if operation == "create" and checker.create():
                granted = True

            if operation == "read" and checker.read():
                granted = True

            if operation == "update" and checker.update():
                granted = True

            if operation == "delete" and checker.delete():
                granted = True

            if granted:
                checker.access_event(operation)
                return True

        return granted

    @classmethod
    def get_role_name(cls, acting_as_role_id):
        return None
