from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass(frozen=True)
class Embedding:
    """Immutable vector representation"""

    values: Tuple[float, ...]

    def __post_init__(self):
        if len(self.values) == 0:
            raise ValueError("Embedding cannot be empty")
        if not all(isinstance(v, (int, float)) for v in self.values):
            raise ValueError("All embedding values must be numeric")

    @property
    def dimension(self) -> int:
        return len(self.values)

    @classmethod
    def from_list(cls, values: List[float]) -> Embedding:
        return cls(tuple(values))

    def cosine_similarity(self, other: Embedding) -> float:
        if self.dimension != other.dimension:
            raise ValueError("Embeddings must have same dimension")

        a = np.asarray(self.values, dtype=float)
        b = np.asarray(other.values, dtype=float)

        dot = float(np.dot(a, b))
        norm_a = float(np.linalg.norm(a))
        norm_b = float(np.linalg.norm(b))

        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def euclidean_distance(self, other: Embedding) -> float:
        if self.dimension != other.dimension:
            raise ValueError("Embeddings must have same dimension")

        a = np.asarray(self.values, dtype=float)
        b = np.asarray(other.values, dtype=float)

        return float(np.linalg.norm(a - b))
