"""Basic mathematical utilities for one-dimensional distance matrices."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def coordinates_to_distances(coordinates: ArrayLike) -> NDArray[np.float64]:
    """Return D[i, j] = abs(x[i] - x[j]) for a finite 1-D coordinate array."""
    x = np.asarray(coordinates, dtype=float)
    if x.ndim != 1:
        raise ValueError("coordinates must be a one-dimensional array")
    if not np.all(np.isfinite(x)):
        raise ValueError("coordinates must contain only finite values")
    return np.abs(x[:, None] - x[None, :])


def validate_distance_matrix(
    distances: ArrayLike,
    *,
    atol: float = 1e-10,
) -> NDArray[np.float64]:
    """Validate basic distance-matrix properties and return a float array.

    This checks symmetry, non-negativity, finiteness, and a zero diagonal.
    It does not prove that the matrix is a Euclidean distance matrix.
    """
    d = np.asarray(distances, dtype=float)
    if d.ndim != 2 or d.shape[0] != d.shape[1]:
        raise ValueError("distances must be a square 2-D matrix")
    if not np.all(np.isfinite(d)):
        raise ValueError("distances must contain only finite values")
    if np.any(d < -atol):
        raise ValueError("distances must be non-negative")
    if not np.allclose(d, d.T, atol=atol, rtol=0.0):
        raise ValueError("distances must be symmetric")
    if not np.allclose(np.diag(d), 0.0, atol=atol, rtol=0.0):
        raise ValueError("distance matrix diagonal must be zero")
    # Clamp tiny negative roundoff values to zero after validation.
    return np.maximum(d, 0.0)


def classical_mds_gram(distances: ArrayLike) -> NDArray[np.float64]:
    """Return the double-centered Gram matrix B = -1/2 J D^2 J.

    Input entries are distances, not squared distances. This function validates
    basic matrix properties but does not guarantee Euclidean embeddability.
    """
    d = validate_distance_matrix(distances)
    n = d.shape[0]
    if n == 0:
        return np.empty((0, 0), dtype=float)
    centering = np.eye(n) - np.ones((n, n), dtype=float) / n
    return -0.5 * centering @ (d**2) @ centering
