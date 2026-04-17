from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import UUID, uuid4


@dataclass
class Room:
    name: str
    capacity: int
    id: UUID = field(default_factory=uuid4)
    location: str = ""
    description: str | None = None
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=timezone.utc))
