import numpy as np
import pytest

from mftm.distances import (
    classical_mds_gram,
    coordinates_to_distances,
    validate_distance_matrix,
)


def test_known_distances():
    d = coordinates_to_distances([0, 2, 5])
    np.testing.assert_allclose(d, [[0, 2, 5], [2, 0, 3], [5, 3, 0]])


def test_translation_invariance():
    x = np.array([-3.0, 0.5, 8.0, 8.0])
    np.testing.assert_allclose(
        coordinates_to_distances(x),
        coordinates_to_distances(x + 17.25),
    )


def test_reflection_invariance():
    x = np.array([-3.0, 0.5, 8.0, 8.0])
    np.testing.assert_allclose(
        coordinates_to_distances(x),
        coordinates_to_distances(-x + 4.0),
    )


def test_empty_and_singleton_inputs():
    assert coordinates_to_distances([]).shape == (0, 0)
    np.testing.assert_array_equal(coordinates_to_distances([4]), [[0]])


def test_randomized_line_distances_have_rank_one_gram():
    rng = np.random.default_rng(20261009)
    for n in range(2, 12):
        x = rng.normal(size=n)
        gram = classical_mds_gram(coordinates_to_distances(x))
        eigenvalues = np.linalg.eigvalsh(gram)
        assert eigenvalues.min() >= -1e-9
        assert np.count_nonzero(eigenvalues > 1e-8) <= 1


@pytest.mark.parametrize(
    "bad",
    [
        [[0, 1], [2, 0]],       # asymmetric
        [[0, -1], [-1, 0]],     # negative
        [[1, 1], [1, 0]],        # nonzero diagonal
        [[0, np.nan], [np.nan, 0]],
        [[0, 1, 2], [1, 0, 1]],  # nonsquare
    ],
)
def test_invalid_matrices_are_rejected(bad):
    with pytest.raises(ValueError):
        validate_distance_matrix(bad)


def test_triangle_violating_matrix_passes_basic_validation_but_is_not_euclidean():
    # Basic validation intentionally does not claim Euclidean embeddability.
    d = validate_distance_matrix([[0, 1, 3], [1, 0, 1], [3, 1, 0]])
    gram = classical_mds_gram(d)
    assert np.linalg.eigvalsh(gram).min() < -1e-8
