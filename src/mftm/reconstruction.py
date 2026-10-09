"""Reconstruction and orientation operations for complete line-distance data."""
from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

from .distances import classical_mds_gram, coordinates_to_distances, validate_distance_matrix

FloatArray = NDArray[np.float64]


def reconstruct_coordinates_1d(
    distances: ArrayLike, *, tol: float = 1e-8, strict: bool = True
) -> FloatArray:
    """Reconstruct centered 1-D coordinates by classical MDS.

    The returned orientation is arbitrary. Translation is fixed by centering.
    With strict=True, non-PSD or rank>1 inputs are rejected within relative tolerance.
    With strict=False, the leading eigenpair gives a rank-one spectral approximation.
    """
    if not np.isfinite(tol) or tol < 0:
        raise ValueError("tol must be finite and non-negative")
    d = validate_distance_matrix(distances)
    n = d.shape[0]
    if n == 0:
        return np.empty((0,), dtype=np.float64)
    if n == 1:
        return np.zeros((1,), dtype=np.float64)
    b = classical_mds_gram(d)
    vals, vecs = np.linalg.eigh(b)
    spectral_scale = float(np.max(np.abs(vals)))
    threshold = tol * spectral_scale if spectral_scale > 0.0 else tol
    if strict and float(vals[0]) < -threshold:
        raise ValueError("distance matrix is not Euclidean within tolerance (negative Gram eigenvalue)")
    positive = np.flatnonzero(vals > threshold)
    if strict and len(positive) > 1:
        raise ValueError("distance matrix is not one-dimensional within tolerance (rank exceeds one)")
    idx = int(np.argmax(vals))
    if vals[idx] <= threshold:
        coords = np.zeros(n, dtype=np.float64)
    else:
        coords = vecs[:, idx] * np.sqrt(max(0.0, float(vals[idx])))
    coords -= np.mean(coords)
    return coords


def align_coordinates(reference: ArrayLike, candidate: ArrayLike) -> FloatArray:
    """Align candidate to reference using translation and the better reflection."""
    ref = np.asarray(reference, dtype=np.float64)
    cand = np.asarray(candidate, dtype=np.float64)
    if ref.ndim != 1 or cand.ndim != 1 or ref.shape != cand.shape:
        raise ValueError("coordinate arrays must be one-dimensional and have equal shape")
    if not np.all(np.isfinite(ref)) or not np.all(np.isfinite(cand)):
        raise ValueError("coordinate arrays must be finite")
    if ref.size == 0:
        return cand.copy()
    ref_centered = ref - ref.mean()
    cand_centered = cand - cand.mean()
    direct = np.sqrt(np.mean((ref_centered - cand_centered) ** 2))
    reflected = np.sqrt(np.mean((ref_centered + cand_centered) ** 2))
    aligned = cand_centered if direct <= reflected else -cand_centered
    return aligned + ref.mean()


def orient_from_directed_relation(
    coordinates: ArrayLike, first: int, second: int, *, relation: str = "before"
) -> FloatArray:
    """Choose the reflection consistent with one known directed relation.

    relation='before' means coordinates[first] < coordinates[second]; 'after'
    reverses that constraint. The input is assumed reconstructed up to reflection.
    """
    x = np.asarray(coordinates, dtype=np.float64)
    if x.ndim != 1 or not np.all(np.isfinite(x)):
        raise ValueError("coordinates must be a finite one-dimensional array")
    if relation not in {"before", "after"}:
        raise ValueError("relation must be 'before' or 'after'")
    n = x.size
    if not (0 <= first < n and 0 <= second < n):
        raise IndexError("event index out of range")
    if first == second or np.isclose(x[first], x[second]):
        raise ValueError("directed relation requires distinct temporal positions")
    want_increasing = relation == "before"
    currently_increasing = x[first] < x[second]
    return x.copy() if want_increasing == currently_increasing else -x.copy()


def coordinate_origin(coordinates: ArrayLike, reference_index: int) -> FloatArray:
    """Set a reference event to zero without changing pairwise distances."""
    x = np.asarray(coordinates, dtype=np.float64)
    if x.ndim != 1 or not np.all(np.isfinite(x)):
        raise ValueError("coordinates must be a finite one-dimensional array")
    if not 0 <= reference_index < x.size:
        raise IndexError("reference event index out of range")
    return x - x[reference_index]


def inertial_proper_time(delta_coordinate_time: float, speed: float, *, c: float = 1.0) -> float:
    """Compute inertial flat-spacetime proper time Δτ=Δt sqrt(1-v²/c²).

    This illustrative special-relativistic calculation is not an MFTM prediction.
    """
    dt, v, light_speed = float(delta_coordinate_time), float(speed), float(c)
    if not all(np.isfinite(z) for z in (dt, v, light_speed)):
        raise ValueError("arguments must be finite")
    if dt < 0:
        raise ValueError("coordinate-time interval must be non-negative")
    if light_speed <= 0:
        raise ValueError("c must be positive")
    if abs(v) >= light_speed:
        raise ValueError("inertial speed must satisfy |v| < c")
    return dt * float(np.sqrt(1.0 - (v / light_speed) ** 2))


def reconstruction_residuals(original: ArrayLike, reconstructed: ArrayLike) -> dict[str, float]:
    """Compare pairwise distances generated by reconstructed coordinates."""
    from .distances import distance_metrics
    observed = validate_distance_matrix(original)
    predicted = coordinates_to_distances(reconstructed)
    return distance_metrics(observed, predicted)
