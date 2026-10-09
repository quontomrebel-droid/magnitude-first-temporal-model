"""Targeted error-path tests to improve branch coverage and input contracts."""
import numpy as np
import pytest
from mftm import (
    align_coordinates,
    classical_mds_gram,
    coordinate_origin,
    orient_from_directed_relation,
    reconstruct_coordinates_1d,
)


@pytest.mark.parametrize("tol", [-1.0, np.nan, np.inf])
def test_reconstruction_rejects_invalid_tolerance(tol):
    with pytest.raises(ValueError, match="tol"):
        reconstruct_coordinates_1d([[0.0]], tol=tol)


def test_alignment_accepts_empty_coordinate_arrays():
    result = align_coordinates([], [])
    assert result.shape == (0,)


def test_alignment_rejects_shape_mismatch():
    with pytest.raises(ValueError, match="equal shape"):
        align_coordinates([0, 1], [0])


def test_alignment_rejects_nonfinite_coordinates():
    with pytest.raises(ValueError, match="finite"):
        align_coordinates([0, np.nan], [0, 1])


@pytest.mark.parametrize("coords", [[[0, 1]], [0, np.inf]])
def test_orientation_rejects_invalid_coordinate_vector(coords):
    with pytest.raises(ValueError, match="finite one-dimensional"):
        orient_from_directed_relation(coords, 0, 1)


@pytest.mark.parametrize("coords,reference", [([[0, 1]], 0), ([0, np.nan], 0)])
def test_coordinate_origin_rejects_invalid_coordinates(coords, reference):
    with pytest.raises(ValueError, match="finite one-dimensional"):
        coordinate_origin(coords, reference)


def test_coordinate_origin_rejects_out_of_range_reference():
    with pytest.raises(IndexError, match="reference event index"):
        coordinate_origin([0, 1], 2)


def test_empty_mds_gram_matrix():
    assert classical_mds_gram([]).shape == (0, 0)


def test_empty_matrix_is_a_valid_pseudometric_on_the_empty_set():
    from mftm import validate_pseudometric
    assert validate_pseudometric([]).shape == (0, 0)
