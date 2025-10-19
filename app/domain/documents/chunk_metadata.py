from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict


@dataclass
class ChunkMetadata:
    """Fixed schema for chunk metadata"""

    source: str
    page_number: int | None = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    custom_fields: Dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(
        init=False, default_factory=lambda: datetime.now(timezone.utc)
    )

    def updated(
        self,
        *,
        source: str | None = None,
        page_number: int | None = None,
        custom_fields: Dict[str, Any] | None = None,
    ) -> "ChunkMetadata":
        """Return a new ChunkMetadata based on this one with the provided updates.

        - `source` and `page_number` override the existing values when provided.
        - `custom_fields` are shallow-merged onto existing custom_fields when provided.
        The returned instance preserves the original `created_at` timestamp.
        """
        new_source = source if source is not None else self.source
        new_page = page_number if page_number is not None else self.page_number
        new_custom = dict(self.custom_fields)
        if custom_fields:
            new_custom.update(custom_fields)

        return ChunkMetadata(
            source=new_source,
            page_number=new_page,
            created_at=self.created_at,
            custom_fields=new_custom,
        )

    def matches_filter(self, filters: Dict[str, Any]) -> bool:
        """Check whether this metadata matches the provided filters.

        Supported filters: 'source', 'page_number', 'created_after', 'created_before'.
        """
        for key, value in filters.items():
            if key == "source" and self.source != value:
                return False
            if key == "page_number" and self.page_number != value:
                return False
            if key == "created_after":
                if self.created_at <= value:
                    return False
            if key == "created_before":
                if self.created_at >= value:
                    return False
        return True
