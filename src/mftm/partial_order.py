"""Finite strict partial-order helpers for exploratory order-structure controls.

These routines describe an input directed relation; they do not infer chronology,
causality, or a physical interpretation from magnitude-only data.
"""
from __future__ import annotations
from collections.abc import Iterable
import numpy as np
from numpy.typing import NDArray


def transitive_closure(size: int, relations: Iterable[tuple[int, int]]) -> NDArray[np.bool_]:
    """Return the strict transitive closure of a finite directed relation.

    Each pair (i, j) means i precedes j. The relation must be acyclic.
    Cycles, self-relations, malformed pairs, and out-of-range endpoints raise
    ValueError. Incomparable pairs remain false in both directions.
    """
    if isinstance(size, bool) or not isinstance(size, int) or size < 0:
        raise ValueError("size must be a non-negative integer")
    reach = np.zeros((size, size), dtype=bool)
    for relation in relations:
        if not isinstance(relation, (tuple, list)) or len(relation) != 2:
            raise ValueError("each relation must be a pair of event indices")
        i, j = relation
        if (isinstance(i, bool) or isinstance(j, bool)
                or not isinstance(i, (int, np.integer))
                or not isinstance(j, (int, np.integer))):
            raise ValueError("event indices must be integers")
        i, j = int(i), int(j)
        if not (0 <= i < size and 0 <= j < size):
            raise ValueError("event index out of range")
        if i == j:
            raise ValueError("strict partial order cannot contain a self-relation")
        reach[i, j] = True
    for k in range(size):
        reach |= reach[:, k, None] & reach[None, k, :]
    if np.any(np.diag(reach)):
        raise ValueError("directed relations contain a cycle; no strict partial order exists")
    return reach


def incomparable_pairs(size: int, relations: Iterable[tuple[int, int]]) -> list[tuple[int, int]]:
    """Return unordered event-index pairs incomparable in either direction."""
    reach = transitive_closure(size, relations)
    return [(i, j) for i in range(size) for j in range(i + 1, size)
            if not reach[i, j] and not reach[j, i]]
