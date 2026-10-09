"""Expanded tests tied to the formal MFTM specification.

These are mathematical/property-style and synthetic algorithm tests. Passing them
is not empirical evidence about physical time, quantum theory, or ontology.
"""
from fractions import Fraction

import numpy as np
import pytest

from mftm import (
    align_coordinates,
    classical_mds_gram,
    coordinate_origin,
    coordinates_to_distances,
    distance_metrics,
    inertial_proper_time,
    orient_from_directed_relation,
    reconstruct_coordinates_1d,
    reconstruction_residuals,
    validate_distance_matrix,
    validate_pseudometric,
)


# A — exact definition and pseudo(metric) axioms.
@pytest.mark.parametrize("coordinates", [
    [], [0], [4, 4], [0, 1], [-10, 0, 10], [0, 1, 1, 4],
    [Fraction(1, 3), Fraction(5, 7), Fraction(-2, 5)],
])
def test_A_definition_matches_absolute_difference_exactly(coordinates):
    d = coordinates_to_distances(coordinates)
    expected = (np.empty((0, 0)) if not coordinates else
                np.asarray([[abs(float(a) - float(b)) for b in coordinates] for a in coordinates]))
    np.testing.assert_allclose(d, expected, rtol=0, atol=0)


@pytest.mark.parametrize("seed", range(25))
def test_A_nonnegativity_symmetry_diagonal_and_triangle(seed):
    rng = np.random.default_rng(5000 + seed)
    x = rng.integers(-100, 101, size=1 + seed % 16).astype(float)
    d = coordinates_to_distances(x)
    assert np.all(d >= 0)
    np.testing.assert_array_equal(d, d.T)
    np.testing.assert_array_equal(np.diag(d), np.zeros(len(x)))
    for i in range(len(x)):
        for j in range(len(x)):
            assert d[i, j] <= d[i, :].max() + d[:, j].max()
            for k in range(len(x)):
                assert d[i, j] <= d[i, k] + d[k, j]
    validate_pseudometric(d)


@pytest.mark.parametrize("coordinates", [[0, 0, 1], [4, 4], [1, 2, 2, 8]])
def test_A_distinct_event_labels_can_have_zero_separation(coordinates):
    d = coordinates_to_distances(coordinates)
    for i, x in enumerate(coordinates):
        for j, y in enumerate(coordinates):
            assert (d[i, j] == 0) == (x == y)


@pytest.mark.parametrize("coordinates", [[0, 1], [-4, 0, 9], [Fraction(0), Fraction(1, 3), Fraction(2, 3)]])
def test_A_unique_timestamps_give_identity_of_indiscernibles(coordinates):
    assert len(set(coordinates)) == len(coordinates)
    d = coordinates_to_distances(coordinates)
    for i in range(len(coordinates)):
        for j in range(len(coordinates)):
            assert (d[i, j] == 0) == (i == j)


def test_A_pseudometric_is_not_necessarily_a_metric():
    d = coordinates_to_distances([2, 2, 5])
    assert d[0, 1] == 0
    with pytest.raises(ValueError, match="identity"):
        _assert_metric_identity(d)


def _assert_metric_identity(d):
    if np.any((d == 0) & (~np.eye(d.shape[0], dtype=bool))):
        raise ValueError("identity of indiscernibles fails: pseudometric only")


@pytest.mark.parametrize("bad", [
    [[0, 1, 3], [1, 0, 1], [3, 1, 0]],
    [[0, 2, 2], [2, 0, 5], [2, 5, 0]],
])
def test_A_triangle_inequality_is_a_separate_validation_step(bad):
    validate_distance_matrix(bad)
    with pytest.raises(ValueError, match="triangle"):
        validate_pseudometric(bad)


# B — translation, units and rescaling invariance.
@pytest.mark.parametrize("shift", [-1e8, -1000, -1, -0.125, 0, 0.25, 4, 1000, 1e8])
def test_B_translation_does_not_change_D(shift):
    x = np.array([-3.25, -1, 0, 4.5, 4.5])
    np.testing.assert_allclose(coordinates_to_distances(x + shift), coordinates_to_distances(x), rtol=1e-8, atol=1e-8)


@pytest.mark.parametrize("scale", [-100, -2, -0.1, 0, 0.1, 1, 2, 100])
def test_B_scale_changes_magnitudes_by_absolute_scale(scale):
    x = np.array([-2.0, -0.25, 1.5, 8.0])
    np.testing.assert_allclose(coordinates_to_distances(scale * x), abs(scale) * coordinates_to_distances(x), rtol=1e-12, atol=1e-12)


def test_B_seconds_to_milliseconds_changes_units_not_structure():
    seconds = np.array([0.0, 0.25, 1.5, 2.0])
    ms = 1000 * seconds
    d_seconds, d_ms = coordinates_to_distances(seconds), coordinates_to_distances(ms)
    np.testing.assert_allclose(d_ms, 1000 * d_seconds)
    np.testing.assert_array_equal(d_ms > 0, d_seconds > 0)


# C — reflection invariance and direction blindness controls.
@pytest.mark.parametrize("seed", range(30))
def test_C_global_reflection_with_arbitrary_shift_preserves_matrix(seed):
    rng = np.random.default_rng(8100 + seed)
    x = rng.normal(size=1 + seed % 20)
    shift = float(rng.normal() * 100)
    np.testing.assert_allclose(coordinates_to_distances(x), coordinates_to_distances(shift - x), rtol=1e-12, atol=1e-12)


def test_C_direction_blindness_control_is_exactly_chance_in_paired_reflections():
    """A deterministic estimator sees identical D for each paired opposite truth.

    The test is an identifiability control, not a probabilistic estimate from a
    single random sample: every matrix is presented with both global orientations.
    """
    correct = total = 0
    for seed in range(100):
        rng = np.random.default_rng(9100 + seed)
        x = np.cumsum(rng.uniform(0.1, 3.0, size=8))
        x -= x.mean()
        for true_x in (x, -x):
            d = coordinates_to_distances(true_x)
            estimate = reconstruct_coordinates_1d(d)
            predicted_before = estimate[0] < estimate[-1]
            actually_before = true_x[0] < true_x[-1]
            correct += int(predicted_before == actually_before)
            total += 1
    assert total == 200
    assert correct == total // 2


def test_C_same_D_cannot_change_deterministic_orientation_estimate():
    x = np.array([-5.0, -1.0, 0.5, 2.0, 8.0])
    d1 = coordinates_to_distances(x)
    d2 = coordinates_to_distances(-x)
    np.testing.assert_array_equal(d1, d2)
    np.testing.assert_array_equal(reconstruct_coordinates_1d(d1), reconstruct_coordinates_1d(d2))


# D — distance sufficiency, MDS eigenspectrum, reconstruction diagnostics.
@pytest.mark.parametrize("seed", range(40))
def test_D_reconstruction_recovers_full_pairwise_matrix(seed):
    rng = np.random.default_rng(10100 + seed)
    x = rng.normal(loc=20, scale=7, size=2 + seed % 50)
    d = coordinates_to_distances(x)
    recovered = reconstruct_coordinates_1d(d)
    np.testing.assert_allclose(coordinates_to_distances(recovered), d, rtol=1e-8, atol=1e-8)
    aligned = align_coordinates(x, recovered)
    assert np.sqrt(np.mean((x - aligned) ** 2)) < 1e-7


@pytest.mark.parametrize("n", [2, 3, 4, 5, 10, 25, 50, 100, 150])
def test_D_exact_line_embedding_gram_is_psd_and_rank_at_most_one(n):
    rng = np.random.default_rng(11100 + n)
    x = rng.uniform(-100, 100, size=n)
    eigenvalues = np.linalg.eigvalsh(classical_mds_gram(coordinates_to_distances(x)))
    assert eigenvalues.min() > -1e-7
    assert np.count_nonzero(eigenvalues > 1e-7) <= 1


@pytest.mark.parametrize("coordinates", [[0, 0], [7], [0, 1], [-10, -2, 0, 0, 17]])
def test_D_degenerate_and_duplicate_timestamp_cases_reconstruct(coordinates):
    d = coordinates_to_distances(coordinates)
    reconstructed = reconstruct_coordinates_1d(d)
    np.testing.assert_allclose(coordinates_to_distances(reconstructed), d, atol=1e-8)


def test_D_equidistant_three_point_matrix_is_not_a_line_embedding():
    d = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 0]], dtype=float)
    assert np.linalg.matrix_rank(classical_mds_gram(d), tol=1e-8) == 2
    with pytest.raises(ValueError, match="rank exceeds one"):
        reconstruct_coordinates_1d(d)


def test_D_non_euclidean_matrix_rejected_by_negative_gram_eigenvalue():
    d = np.array([[0, 1, 3], [1, 0, 1], [3, 1, 0]], dtype=float)
    with pytest.raises(ValueError, match="negative Gram eigenvalue"):
        reconstruct_coordinates_1d(d)


def test_D_permuting_event_labels_permutes_D_and_keeps_reconstruction_equivalent():
    x = np.array([-3.0, 0.0, 1.0, 9.0, 12.0])
    order = np.array([3, 0, 4, 1, 2])
    d = coordinates_to_distances(x)
    permuted = d[np.ix_(order, order)]
    recovered = reconstruct_coordinates_1d(permuted)
    np.testing.assert_allclose(coordinates_to_distances(recovered), permuted, atol=1e-8)


def test_D_incomplete_matrix_is_rejected_not_silently_imputed():
    d = np.array([[0, 1, np.nan], [1, 0, 2], [np.nan, 2, 0]], dtype=float)
    with pytest.raises(ValueError, match="finite"):
        reconstruct_coordinates_1d(d)


def test_D_exact_rational_triangle_checks_without_floating_point():
    points = [Fraction(-5, 3), Fraction(0), Fraction(7, 4), Fraction(11, 2)]
    d = [[abs(a - b) for b in points] for a in points]
    for i in range(len(points)):
        assert d[i][i] == 0
        for j in range(len(points)):
            assert d[i][j] == d[j][i] and d[i][j] >= 0
            for k in range(len(points)):
                assert d[i][j] <= d[i][k] + d[k][j]


# E — minimal directional constraint resolves reflection only.
@pytest.mark.parametrize("relation", ["before", "after"])
@pytest.mark.parametrize("first,second", [(0, 1), (0, 2), (1, 3), (2, 4)])
def test_E_one_directed_relation_selects_global_orientation(relation, first, second):
    x = np.array([-3.0, 0.0, 1.0, 5.0, 12.0])
    d = coordinates_to_distances(x)
    candidate = reconstruct_coordinates_1d(d)
    oriented = orient_from_directed_relation(candidate, first, second, relation=relation)
    assert (oriented[first] < oriented[second]) == (relation == "before")
    np.testing.assert_allclose(coordinates_to_distances(oriented), d, atol=1e-8)


def test_E_orientation_constraint_does_not_change_distances():
    x = np.array([0.0, 1.0, 4.0, 9.0])
    raw = -x + 20
    before = orient_from_directed_relation(raw, 0, 3, relation="before")
    after = orient_from_directed_relation(raw, 0, 3, relation="after")
    np.testing.assert_allclose(coordinates_to_distances(before), coordinates_to_distances(after))


# F — observer/reference origin vs simple inertial proper-time distinction.
@pytest.mark.parametrize("reference", range(6))
def test_F_designated_now_changes_origin_not_distance(reference):
    x = np.array([-10.0, -2.0, 0.0, 1.5, 7.0, 12.0])
    tau = coordinate_origin(x, reference)
    assert tau[reference] == pytest.approx(0)
    np.testing.assert_allclose(np.abs(tau), coordinates_to_distances(x)[reference])
    np.testing.assert_allclose(coordinates_to_distances(tau), coordinates_to_distances(x))


@pytest.mark.parametrize("speed", [-0.95, -0.8, -0.3, 0, 0.3, 0.8, 0.95])
def test_F_inertial_proper_time_is_even_in_velocity(speed):
    assert inertial_proper_time(10, speed) == pytest.approx(inertial_proper_time(10, -speed))


# G — no physical/quantum claim is inferred from geometric code tests.
def test_G_magnitude_geometry_has_no_implemented_quantum_prediction():
    import mftm
    assert not hasattr(mftm, "quantum_prediction")
    assert not hasattr(mftm, "page_wootters_prediction")


# H — explicit no-direction controls, not a claim about any physical estimator.
def test_H_novel_prediction_requires_external_specification():
    import pathlib
    project_root = pathlib.Path(__file__).resolve().parents[1]
    text = (project_root / "HYPOTHESES.md").read_text(encoding="utf-8")
    lowered = text.lower()
    assert any(term in lowered for term in ("no observable prediction", "no prediction", "not specified"))
    assert "unresolved" in lowered


# I — exact invariance and representation equivalence.
@pytest.mark.parametrize("seed", range(20))
def test_I_coordinates_related_by_isometry_have_same_distances(seed):
    rng = np.random.default_rng(12100 + seed)
    x = rng.normal(size=3 + seed % 20)
    shift = rng.normal() * 10
    np.testing.assert_allclose(coordinates_to_distances(x), coordinates_to_distances(-x + shift), rtol=1e-12, atol=1e-12)


@pytest.mark.parametrize("first,second", [(0, 1), (1, 2), (2, 3), (3, 4)])
def test_I_reference_origin_preserves_all_pairwise_distances(first, second):
    x = np.array([-2.0, 0.0, 4.5, 4.5, 10.0])
    shifted = coordinate_origin(x, second)
    assert shifted[second] == 0
    assert abs(shifted[first]) == pytest.approx(coordinates_to_distances(x)[first, second])
    np.testing.assert_allclose(coordinates_to_distances(shifted), coordinates_to_distances(x))


# J — noise, residual metrics and uncertainty characterization.
@pytest.mark.parametrize("sigma", [0.0, 1e-5, 1e-3, 0.01, 0.1, 0.3, 0.7])
def test_J_symmetric_noise_produces_finite_diagnostics(sigma):
    rng = np.random.default_rng(13100)
    x = np.sort(rng.uniform(-5, 5, size=18))
    true_d = coordinates_to_distances(x)
    noise = rng.normal(0, sigma, size=true_d.shape)
    noise = (noise + noise.T) / 2
    np.fill_diagonal(noise, 0)
    observed = np.maximum(0, true_d + noise)
    recovered = reconstruct_coordinates_1d(observed, strict=False)
    metrics = reconstruction_residuals(observed, recovered)
    assert all(np.isfinite(v) and v >= 0 for v in metrics.values())


def test_J_zero_noise_limit_is_numerically_exact():
    x = np.array([-9.0, -3.0, 0.0, 0.125, 6.0, 12.0])
    d = coordinates_to_distances(x)
    assert reconstruction_residuals(d, reconstruct_coordinates_1d(d))["max_abs_error"] < 1e-8


def test_J_known_error_metrics():
    metrics = distance_metrics([[0, 1], [1, 0]], [[0, 2], [2, 0]])
    assert metrics["max_abs_error"] == pytest.approx(1)
    assert metrics["mae"] == pytest.approx(0.5)
    assert metrics["rmse"] == pytest.approx(np.sqrt(0.5))


def test_J_metrics_reject_empty_or_nonfinite_comparisons():
    with pytest.raises(ValueError):
        distance_metrics([], [])
    with pytest.raises(ValueError):
        distance_metrics([[0, np.nan]], [[0, 1]])
