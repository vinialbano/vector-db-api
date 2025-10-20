from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4

from app.errors import InvalidEntityError


@dataclass(frozen=True)
class ChunkId:
    value: UUID

    @classmethod
    def generate(cls) -> "ChunkId":
        return cls(uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> "ChunkId":
        try:
            return cls(UUID(id_str))
        except (ValueError, TypeError) as exc:
            raise InvalidEntityError(f"Invalid chunk id: {id_str}") from exc

    def __str__(self) -> str:
        return str(self.value)
