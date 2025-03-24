from dataclasses import dataclass, field
from typing import List

@dataclass
class UserRole:
    id: str
    name: str


@dataclass
class UserPermissionInfo:
    user_id: str
    roles: List[UserRole] = field(default_factory=list)
    permissions: set = field(default_factory=set)
