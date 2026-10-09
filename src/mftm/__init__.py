"""Magnitude-First Temporal Model research utilities."""

from .distances import (
    coordinates_to_distances,
    classical_mds_gram,
    validate_distance_matrix,
)

__all__ = [
    "coordinates_to_distances",
    "classical_mds_gram",
    "validate_distance_matrix",
]
