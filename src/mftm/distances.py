"""Utilities for finite one-dimensional magnitude-first temporal data.

The package concerns representations and distance geometry. It does not infer
that time is ontologically a distance, and it does not make physical predictions.
"""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

FloatMatrix = NDArray[np.float64]


def coordinates_to_distances(coordinates: ArrayLike) -> FloatMatrix:
    """Return D[i,j] = abs(x[i]-x[j]) from a finite one-dimensional vector."""
    x = np.asarray(coordinates, dtype=np.float64)
    if x.ndim != 1:
        raise ValueError("coordinates must be a one-dimensional array")
    if not np.all(np.isfinite(x)):
        raise ValueError("coordinates must contain only finite values")
    with np.errstate(over="ignore", invalid="ignore"):
        d = np.abs(x[:, None] - x[None, :])
    if not np.all(np.isfinite(d)):
        raise ValueError("pairwise differences overflowed floating-point range")
    return d


def validate_distance_matrix(
    distances: ArrayLike, *, atol: float = 1e-10
) -> FloatMatrix:
    """Validate matrix shape, finiteness, symmetry, non-negativity and zero diagonal.

    This basic validator intentionally does not establish triangle inequality or
    Euclidean embeddability. Tiny negative round-off in [-atol, 0) is clamped.
    """
    if not np.isfinite(atol) or atol < 0:
        raise ValueError("atol must be finite and non-negative")
    d = np.asarray(distances, dtype=np.float64)
    if d.ndim == 1 and d.size == 0:
        d = np.empty((0, 0), dtype=np.float64)
    if d.ndim != 2 or d.shape[0] != d.shape[1]:
        raise ValueError("distances must be a square two-dimensional matrix")
    if not np.all(np.isfinite(d)):
        raise ValueError("distances must contain only finite values")
    if np.any(d < -atol):
        raise ValueError("distances must be non-negative")
    if not np.allclose(d, d.T, atol=atol, rtol=0.0):
        raise ValueError("distances must be symmetric")
    if not np.allclose(np.diag(d), 0.0, atol=atol, rtol=0.0):
        raise ValueError("distance matrix diagonal must be zero")
    out = np.maximum(d, 0.0).copy()
    np.fill_diagonal(out, 0.0)
    return out


def validate_pseudometric(distances: ArrayLike, *, atol: float = 1e-10) -> FloatMatrix:
    """Validate the pseudometric axioms for a finite distance matrix."""
    d = validate_distance_matrix(distances, atol=atol)
    if d.size:
        slack = d[:, None, :] + d[None, :, :] - d[:, :, None]
        if np.any(slack < -atol):
            raise ValueError("distance matrix violates triangle inequality")
    return d


def classical_mds_gram(distances: ArrayLike, *, atol: float = 1e-10) -> FloatMatrix:
    """Compute B = -1/2 J D^2 J from a validated distance matrix."""
    d = validate_distance_matrix(distances, atol=atol)
    n = d.shape[0]
    if n == 0:
        return np.empty((0, 0), dtype=np.float64)
    j = np.eye(n, dtype=np.float64) - np.ones((n, n), dtype=np.float64) / n
    b = -0.5 * j @ np.square(d) @ j
    return (b + b.T) / 2.0


def distance_metrics(reference: ArrayLike, candidate: ArrayLike) -> dict[str, float]:
    """Return max-absolute error, RMSE, and mean absolute error for matrices."""
    a = np.asarray(reference, dtype=np.float64)
    b = np.asarray(candidate, dtype=np.float64)
    if a.shape != b.shape or a.size == 0:
        raise ValueError("reference and candidate must have the same non-empty shape")
    if not np.all(np.isfinite(a)) or not np.all(np.isfinite(b)):
        raise ValueError("inputs must be finite")
    delta = a - b
    return {
        "max_abs_error": float(np.max(np.abs(delta))),
        "rmse": float(np.sqrt(np.mean(np.square(delta)))),
        "mae": float(np.mean(np.abs(delta))),
    }
