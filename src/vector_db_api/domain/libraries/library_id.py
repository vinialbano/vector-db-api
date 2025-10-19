from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class LibraryId:
    value: UUID

    @classmethod
    def generate(cls) -> "LibraryId":
        return cls(uuid4())

    @classmethod
    def from_string(cls, id_str: str) -> "LibraryId":
        return cls(UUID(id_str))

    def __str__(self) -> str:
        return str(self.value)
