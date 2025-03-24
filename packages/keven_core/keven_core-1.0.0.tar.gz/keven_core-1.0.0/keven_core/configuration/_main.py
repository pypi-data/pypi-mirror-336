from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
import os
from pydantic import Field
from types import MappingProxyType


class BaseConfig(BaseSettings):
    """
    Base configuration class that microservices inherit.

    Configuration is loaded from environment variables first,
    then falls back to a .env file located in the microservice.
    Supports dynamic environment selection (dev, prod, staging).
    """

    ENV: str = Field(default_factory=lambda: os.getenv("ENV", "dev"))  # Default to development if not set

    model_config = {"extra": "allow", "validate_assignment": True, "arbitrary_types_allowed": True}

    @classmethod
    def load_env(cls, env_file: str = None):
        """Loads environment variables from the selected .env file if they are not set."""
        subclass_path = Path(__file__).resolve()
        if cls != BaseConfig:
            subclass_path = Path(cls.__module__.replace(".", "/")).parent

        env_file_path = Path(env_file) if env_file else subclass_path / ".env"
        if env_file_path.exists():
            load_dotenv(dotenv_path=env_file_path, override=True)
            return dotenv_values(env_file_path)  # Returns only key-value pairs from .env
        elif env_file:
            raise FileNotFoundError(f"No such file: {env_file}")
        return {}

    def __init_subclass__(cls, **kwargs):
        """Ensure that new environment variables from all sources are inherited and recognized before subclass instantiation."""
        super().__init_subclass__(**kwargs)

        # Ensure _env_vars exists in subclasses and inherits parent values
        cls._env_vars = getattr(cls, "_env_vars", {}).copy()  # Copy parent vars

        # Include explicitly declared fields (inherited + new)
        for field in cls.model_fields.keys():
            field_value = getattr(cls, field, None)
            if field_value is not None:
                cls._env_vars.setdefault(field.upper(), field_value)

        # Include environment variables from .env and os.environ
        env_vars = {key.upper(): value for key, value in {**os.environ, **cls.load_env()}.items() if value is not None}

        # Merge new environment variables without overwriting existing ones
        cls._env_vars.update(env_vars)

        for key, value in env_vars.items():
            if not hasattr(cls, key):  # Only add if not explicitly declared
                setattr(cls, key, value)

    def __init__(self, **values):
        """Ensure Pydantic initializes with inherited environment variables."""
        super().__init__(**values)

        # Preserve parent values while ensuring instance isolation
        inherited_vars = getattr(self, "_env_vars", {}).copy()
        self._env_vars = MappingProxyType(inherited_vars)

    def __getattr__(self, name):
        """Allow access to uppercase environment variables using lowercase names and cache results."""
        uppercase_name = name.upper()

        if uppercase_name in self.__dict__:
            return self.__dict__[uppercase_name]

        if uppercase_name in self._env_vars:
            value = self._env_vars[uppercase_name]
            self.__dict__[uppercase_name] = value  # Cache the result in __dict__
            self.__dict__[name] = value  # Cache lowercase alias too
            return value

        raise AttributeError(f"{self.__class__.__name__} has no attribute '{name}'")
