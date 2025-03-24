# keven_core v1.0.0
Python package containing common utilities, functions, and helpers across all microservices

keven_core offers the following subpackages:
- configuration
- database
- exceptions
- grpc
- kafka
- logging
- models
- security
- utils

## Configuration
Classes and utilities for Configuration
### BaseConfig: Dynamic Environment Configuration Management
`BaseConfig` is the foundational configuration class in **keven_core**, designed to **dynamically load and inherit environment variables** across multiple microservice submodules.

#### How It Works:
- **Multi-Level Inheritance** → Each subclass (`DomainConfig`, `DatabaseConfig`, etc.) retains and extends the environment variables of its parent, ensuring configuration consistency across modules.
- **Priority-Based Loading** → Variables are loaded in the following order:
  1. **Explicitly declared class attributes**
  2. **System environment variables (`os.environ`)**
  3. **`.env` file specific to the subclass (if present)**
- **Automatic Variable Merging** → New environment variables from `.env` files or subclass definitions **merge with inherited values** instead of overwriting them.
- **Case-Insensitive Access** → Variables are normalized and accessible via both **uppercase and lowercase names**.

This approach ensures that each microservice submodule can define its own configurations **while preserving inherited values from parent modules**. This way, the `domain` submodule can be the first to subclass `BaseConfig`, then the `database` submodule can subclass the config class from `domain`, and the resulting instance would contain **all of the env variables** from both `domain` and `database`.🚀
