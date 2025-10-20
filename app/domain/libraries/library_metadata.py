from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict

from app.errors import InvalidEntityError


@dataclass
class LibraryMetadata:
    """Fixed schema for library metadata"""

    name: str
    description: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(
        init=False, default_factory=lambda: datetime.now(timezone.utc)
    )
    custom_fields: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if not self.name.strip():
            raise InvalidEntityError("Library name cannot be empty")

    def updated(
        self,
        *,
        name: str | None = None,
        description: str | None = None,
        custom_fields: Dict[str, Any] | None = None,
    ) -> "LibraryMetadata":
        """Return a new LibraryMetadata with selective updates and refreshed updated_at."""
        new_name = name if name is not None else self.name
        new_description = description if description is not None else self.description
        new_custom = dict(self.custom_fields)
        if custom_fields:
            new_custom.update(custom_fields)
        return LibraryMetadata(
            name=new_name,
            description=new_description,
            created_at=self.created_at,
            custom_fields=new_custom,
        )
