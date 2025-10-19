from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class DocumentMetadata:
    """Fixed schema for document metadata"""

    title: str
    author: str | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(
        init=False, default_factory=lambda: datetime.now(timezone.utc)
    )

    def updated(
        self,
        *,
        title: str | None = None,
        author: str | None = None,
        custom_fields: Dict[str, Any] | None = None,
    ) -> "DocumentMetadata":
        """Return a new DocumentMetadata with selective updates, preserving created_at."""
        new_title = title if title is not None else self.title
        new_author = author if author is not None else self.author
        new_custom = dict(self.custom_fields)
        if custom_fields:
            new_custom.update(custom_fields)
        return DocumentMetadata(
            title=new_title,
            author=new_author,
            created_at=self.created_at,
            custom_fields=new_custom,
        )
