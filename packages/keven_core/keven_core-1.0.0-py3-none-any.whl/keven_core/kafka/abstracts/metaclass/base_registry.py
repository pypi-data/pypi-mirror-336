import logging
from typing import Any, Dict, Set, Type


class BaseRegistryMeta(type):
    """
    Base metaclass for automatically registering handler subclasses.

    Derived metaclasses must implement the following class methods:
      - get_registry(): Return the dictionary used for registration.
      - get_registration_attr(): Return the name of the class attribute to use as a key.
      - get_excluded_names(): Return a set of class names to exclude from auto-registration.

    The __init__ method of this metaclass automatically registers any concrete subclass
    (i.e. one that does not have abstract methods) that has a non-None value for the
    attribute specified by get_registration_attr(), and whose name is not in get_excluded_names().
    """

    def __init__(cls, name, bases, namespace) -> None:
        super().__init__(name, bases, namespace)
        # Only auto-register if:
        #  - auto_register is True (default)
        #  - The class name is not in the set of excluded names (e.g., for long-running handlers)
        #  - The registration key (e.g., event_name or command_name) is not None.
        if getattr(cls, "auto_register", True) and name not in cls.get_excluded_names():
            key = getattr(cls, cls.get_registration_attr(), None)
            if key is not None:
                registry = cls.get_registry()
                if key not in registry:
                    registry[key] = set()
                registry[key].add(cls)
                logging.info(f"Registered {name} for {cls.get_registration_attr()} = {key}")

    @classmethod
    def get_registry(mcs) -> Dict[Any, Set[Type]]:
        """
        Should be implemented in derived metaclasses to return the specific registry.
        """
        raise NotImplementedError("Derived metaclasses must implement get_registry.")

    @classmethod
    def get_registration_attr(mcs) -> str:
        """
        Should be implemented in derived metaclasses to specify the attribute name used as key.
        """
        raise NotImplementedError("Derived metaclasses must implement get_registration_attr.")

    @classmethod
    def get_excluded_names(mcs) -> Set[str]:
        """
        Returns a set of class names to exclude from auto-registration.
        Derived metaclasses can override this if needed.
        """
        return set()


