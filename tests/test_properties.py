"""Seeded/property checks for Families A-J; not evidence of physical predictions."""
from fractions import Fraction
import numpy as np
import pytest
from mftm import (
    align_coordinates, classical_mds_gram, coordinate_origin,
    coordinates_to_distances, distance_metrics, inertial_proper_time,
    orient_from_directed_relation, reconstruct_coordinates_1d,
    reconstruction_residuals, validate_distance_matrix, validate_pseudometric,
)

# A — pseudometric axioms, input validation and edge cases.
@pytest.mark.parametrize("n", range(2, 14))
def test_A_pseudometric_axioms(n):
    x = np.random.default_rng(1000+n).integers(-20, 21, size=n).astype(float)
    d = coordinates_to_distances(x)
    assert np.all(d >= 0)
    np.testing.assert_array_equal(d, d.T)
    np.testing.assert_array_equal(np.diag(d), np.zeros(n))
    assert all(d[i,k] <= d[i,j] + d[j,k] + 1e-12 for i in range(n) for j in range(n) for k in range(n))
    validate_pseudometric(d)

@pytest.mark.parametrize("x", [[], [7], [2,2], [-5,0,5], [1e-100,0,-1e-100]])
def test_A_coordinate_edge_cases(x):
    d = coordinates_to_distances(x)
    assert d.shape == (len(x), len(x))
    if len(x): np.testing.assert_array_equal(np.diag(d), np.zeros(len(x)))

@pytest.mark.parametrize("bad", [[[1,2],[3,4]], [np.nan], [np.inf], [-np.inf]])
def test_A_invalid_coordinates_rejected(bad):
    with pytest.raises(ValueError): coordinates_to_distances(bad)

def test_A_integer_vector_is_valid():
    np.testing.assert_array_equal(coordinates_to_distances([1,2,3]), [[0,1,2],[1,0,1],[2,1,0]])

def test_A_pairwise_overflow_rejected():
    with pytest.raises(ValueError, match="overflowed"): coordinates_to_distances([-1e308,1e308])

@pytest.mark.parametrize("atol", [-1, np.nan, np.inf])
def test_A_invalid_tolerance_rejected(atol):
    with pytest.raises(ValueError): validate_distance_matrix([[0.]], atol=atol)

@pytest.mark.parametrize("bad", [[[0,1],[2,0]], [[0,-.1],[-.1,0]], [[1,1],[1,0]], [[0,np.nan],[np.nan,0]], [[0,1,2],[1,0,1]]])
def test_A_invalid_matrices_rejected(bad):
    with pytest.raises(ValueError): validate_distance_matrix(bad)

def test_A_triangle_inequality_checked_separately():
    d=[[0,1,3],[1,0,1],[3,1,0]]
    validate_distance_matrix(d)
    with pytest.raises(ValueError, match="triangle"): validate_pseudometric(d)

# B — translations, rescaling and units.
@pytest.mark.parametrize("shift", [-1e6,-100,-1,-.01,0,.125,1,10,100,1e6,1e9])
def test_B_translation_invariance(shift):
    x=np.array([-4.5,-1,.25,3,3.])
    np.testing.assert_allclose(coordinates_to_distances(x), coordinates_to_distances(x+shift), rtol=1e-9, atol=1e-8)

@pytest.mark.parametrize("scale", [1e-6,.001,.1,.5,1,2,10,100,1e3,1e6,1e9])
def test_B_positive_rescaling(scale):
    x=np.array([-2.,0,1.25,9.])
    np.testing.assert_allclose(coordinates_to_distances(scale*x), scale*coordinates_to_distances(x), rtol=2e-8, atol=1e-9)

@pytest.mark.parametrize("scale", [-100,-2,-1,-.01,0,.01,1,2,100])
def test_B_signed_rescaling_uses_abs_scale(scale):
    x=np.array([-3.,0,7.])
    np.testing.assert_allclose(coordinates_to_distances(scale*x), abs(scale)*coordinates_to_distances(x))

def test_B_affine_transform():
    x=np.array([0.,1.,4.,13.])
    np.testing.assert_allclose(coordinates_to_distances(6.5*x-17), 6.5*coordinates_to_distances(x))

# C — reflection ambiguity and orientation controls.
@pytest.mark.parametrize("seed", range(12))
def test_C_reflection_invariance(seed):
    x=np.random.default_rng(seed+600).normal(size=20)
    for shift in (-11.25,0.,3.5):
        np.testing.assert_allclose(coordinates_to_distances(x), coordinates_to_distances(-x+shift), atol=1e-12)

@pytest.mark.parametrize("values", [[0,1],[0,1,2],[-4,0,8],[3,3,9],[-8,5,22,22]])
def test_C_reflected_timelines_share_distances(values):
    x=np.asarray(values,dtype=float)
    np.testing.assert_array_equal(coordinates_to_distances(x), coordinates_to_distances(-x+123))

def test_C_identical_input_cannot_identify_both_global_orientations():
    x=np.array([-2.,-.25,1.,4.])
    a,b=coordinates_to_distances(x),coordinates_to_distances(-x)
    np.testing.assert_array_equal(a,b)
    np.testing.assert_array_equal(reconstruct_coordinates_1d(a),reconstruct_coordinates_1d(b))
    assert np.sign(x[-1]-x[0]) == -np.sign((-x)[-1]-(-x)[0])

# D — MDS, reconstruction, exact examples, rank and scale robustness.
@pytest.mark.parametrize("n", range(2,25))
def test_D_line_reconstruction_up_to_isometry(n):
    x=np.random.default_rng(20000+n).normal(loc=10,scale=3,size=n)
    d=coordinates_to_distances(x); rec=reconstruct_coordinates_1d(d)
    assert np.max(np.abs(align_coordinates(x,rec)-x)) < 1e-7
    assert reconstruction_residuals(d,rec)["max_abs_error"] < 1e-7

@pytest.mark.parametrize("n", range(2,20))
def test_D_line_gram_is_psd_rank_one(n):
    x=np.random.default_rng(30000+n).uniform(-1e3,1e3,size=n)
    vals=np.linalg.eigvalsh(classical_mds_gram(coordinates_to_distances(x)))
    assert vals.min() >= -1e-7
    assert np.count_nonzero(vals>1e-7) <= 1

@pytest.mark.parametrize("x", [[0,1],[0,2,5],[-9,-2,1,17],[4,4,4],[0,1,1,9]])
def test_D_exact_fraction_axioms(x):
    fr=[Fraction(v,1) for v in x]
    d=[[abs(a-b) for b in fr] for a in fr]
    for i in range(len(fr)):
        assert d[i][i]==0
        for j in range(len(fr)):
            assert d[i][j]==d[j][i] and d[i][j]>=0

def test_D_triangle_violator_rejected_by_strict_reconstruction():
    with pytest.raises(ValueError): reconstruct_coordinates_1d([[0,1,3],[1,0,1],[3,1,0]])

def test_D_two_dimensional_embedding_rejected_as_line():
    p=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
    d=np.linalg.norm(p[:,None,:]-p[None,:,:],axis=2)
    with pytest.raises(ValueError,match="rank exceeds one"): reconstruct_coordinates_1d(d)

def test_D_non_strict_mode_approximates_two_dimensional_data():
    p=np.array([[0.,0.],[1.,0.],[0.,1.],[1.,1.]])
    d=np.linalg.norm(p[:,None,:]-p[None,:,:],axis=2)
    x=reconstruct_coordinates_1d(d,strict=False)
    assert x.shape==(4,) and np.all(np.isfinite(x))

@pytest.mark.parametrize("bad", [[], [[0]], [[0,1],[1,0]], [[0,-.01],[-.01,0]]])
def test_D_reconstruction_matrix_edges(bad):
    if bad==[]: assert reconstruct_coordinates_1d(bad).size==0
    elif len(bad)==1: np.testing.assert_array_equal(reconstruct_coordinates_1d(bad),[0.])
    elif bad[0][1]<0:
        with pytest.raises(ValueError): reconstruct_coordinates_1d(bad)
    else: np.testing.assert_allclose(coordinates_to_distances(reconstruct_coordinates_1d(bad)),bad,atol=1e-8)

@pytest.mark.parametrize("scale", [1e-9,1e-6,1e-3,1.,1e6,1e9])
def test_D_scale_robust_reconstruction(scale):
    x=scale*np.array([-2.,-.25,0.,1.5,4.])
    d=coordinates_to_distances(x); rec=reconstruct_coordinates_1d(d)
    assert reconstruction_residuals(d,rec)["max_abs_error"] <= max(1e-15,scale*1e-7)

# E — a directed relation selects one reflection if positions are distinct.
@pytest.mark.parametrize("relation", ["before","after"])
@pytest.mark.parametrize("pair", [(0,1),(0,2),(1,3),(2,4),(3,4)])
def test_E_directed_relation_orients_line(relation,pair):
    x=np.array([0.,1.,4.,8.,11.]); i,j=pair; raw=-x+13
    out=orient_from_directed_relation(raw,i,j,relation=relation)
    assert (out[i]<out[j]) == (relation=="before")
    np.testing.assert_array_equal(np.abs(out[:,None]-out[None,:]),np.abs(raw[:,None]-raw[None,:]))

@pytest.mark.parametrize("relation", ["during","unknown","BEFORE",""])
def test_E_invalid_relations_rejected(relation):
    with pytest.raises(ValueError): orient_from_directed_relation([0,1],0,1,relation=relation)

@pytest.mark.parametrize("pair", [(0,0),(1,1)])
def test_E_same_event_cannot_orient(pair):
    with pytest.raises(ValueError): orient_from_directed_relation([0,1],*pair)

def test_E_ties_cannot_be_ordered_by_timestamp():
    with pytest.raises(ValueError): orient_from_directed_relation([0,0,3],0,1)

def test_E_out_of_range_event_rejected():
    with pytest.raises(IndexError): orient_from_directed_relation([0,1],0,3)

# F — a limited standard inertial proper-time illustration, not an MFTM prediction.
@pytest.mark.parametrize("speed", [0,.1,.25,.5,.75,.9,.99,-.1,-.5,-.9])
def test_F_inertial_proper_time_formula(speed):
    assert inertial_proper_time(12,speed,c=1)==pytest.approx(12*np.sqrt(1-speed**2))

def test_F_stationary_clock(): assert inertial_proper_time(10,0)==pytest.approx(10)
def test_F_moving_clock(): assert inertial_proper_time(10,.8)<10

@pytest.mark.parametrize("args", [(-1,0,1),(1,1,1),(1,-1,1),(1,0,0),(np.nan,0,1),(1,np.inf,1)])
def test_F_invalid_proper_time_args(args):
    with pytest.raises(ValueError): inertial_proper_time(args[0],args[1],c=args[2])

# G/H — scope guards: geometry tests are not quantum or empirical evidence.
def test_G_no_quantum_prediction_api():
    import mftm
    assert not hasattr(mftm,"quantum_prediction")

def test_H_synthetic_reconstruction_is_not_novel_physics():
    d=coordinates_to_distances([0,1,2]); x=reconstruct_coordinates_1d(d)
    assert reconstruction_residuals(d,x)["rmse"]<1e-8

# I — representation equivalence and reference-origin invariance.
@pytest.mark.parametrize("seed", range(15))
def test_I_configuration_equivalent_modulo_isometry(seed):
    rng=np.random.default_rng(7100+seed); x=rng.normal(size=16); y=-x+rng.normal()
    d=coordinates_to_distances(x); np.testing.assert_allclose(d,coordinates_to_distances(y),atol=2e-12)
    aligned=align_coordinates(x,reconstruct_coordinates_1d(coordinates_to_distances(y)))
    assert np.sqrt(np.mean((x-aligned)**2))<1e-7

@pytest.mark.parametrize("idx", range(5))
def test_I_reference_origin_preserves_distances(idx):
    x=np.array([-8.,-2.5,0,4,12.5]); y=coordinate_origin(x,idx)
    assert y[idx]==pytest.approx(0)
    np.testing.assert_allclose(coordinates_to_distances(x),coordinates_to_distances(y))

def test_I_origin_does_not_add_orientation_to_magnitudes():
    x=coordinate_origin(np.array([-2.,1.,6.]),1); y=-x
    np.testing.assert_allclose(np.abs(x),np.abs(y))
    np.testing.assert_allclose(coordinates_to_distances(x),coordinates_to_distances(y))

# J — seeded noise characterization without assuming a universal monotone law.
@pytest.mark.parametrize("sigma", [0,1e-4,1e-3,1e-2,.05,.1,.25,.5])
def test_J_noisy_reconstruction_metrics_finite(sigma):
    rng=np.random.default_rng(9001); x=np.sort(rng.uniform(0,20,size=14)); d=coordinates_to_distances(x)
    noise=rng.normal(0,sigma,size=d.shape); noise=(noise+noise.T)/2; np.fill_diagonal(noise,0)
    observed=np.maximum(0,d+noise); rec=reconstruct_coordinates_1d(observed,strict=False)
    m=reconstruction_residuals(observed,rec)
    assert all(np.isfinite(v) and v>=0 for v in m.values())

def test_J_zero_noise_exact_reconstruction():
    x=np.array([-4.,-2.,0.,1.25,7.,12.]); d=coordinates_to_distances(x)
    assert reconstruction_residuals(d,reconstruct_coordinates_1d(d))["max_abs_error"]<1e-8

def test_J_error_metrics_known_values():
    m=distance_metrics([[0,1],[1,0]],[[0,2],[2,0]])
    assert m["max_abs_error"]==pytest.approx(1)
    assert m["mae"]==pytest.approx(.5)
    assert m["rmse"]==pytest.approx(np.sqrt(.5))

def test_J_error_metrics_reject_shape_mismatch():
    with pytest.raises(ValueError): distance_metrics([[0,1]],[[0,1],[1,0]])
