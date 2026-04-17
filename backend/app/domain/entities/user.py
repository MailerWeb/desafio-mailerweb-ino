import enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


class UserRole(enum.Enum):
    OWNER = "OWNER"
    MEMBER = "MEMBER"


@dataclass
class User:
    email: str
    name: str
    password_hash: str
    id: UUID = field(default_factory=uuid4)
    role: UserRole = UserRole.MEMBER
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
