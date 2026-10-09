"""Tests for explicitly supplied partial-order structure, not inferred time."""
import numpy as np
import pytest
from mftm import incomparable_pairs, transitive_closure


def test_empty_partial_order():
    assert transitive_closure(0, []).shape == (0, 0)
    assert incomparable_pairs(0, []) == []


def test_single_event_is_antichain_without_relations():
    np.testing.assert_array_equal(transitive_closure(1, []), [[False]])
    assert incomparable_pairs(1, []) == []


@pytest.mark.parametrize("size", range(2, 12))
def test_antichain_has_all_distinct_pairs_incomparable(size):
    reach = transitive_closure(size, [])
    assert not reach.any()
    assert len(incomparable_pairs(size, [])) == size * (size - 1) // 2


@pytest.mark.parametrize("size", range(2, 12))
def test_chain_closure_is_total_strict_order(size):
    reach = transitive_closure(size, [(i, i + 1) for i in range(size - 1)])
    for i in range(size):
        assert not reach[i, i]
        for j in range(size):
            assert bool(reach[i, j]) == (i < j)
    assert incomparable_pairs(size, [(i, i + 1) for i in range(size - 1)]) == []


def test_diamond_poset_preserves_incomparability():
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    reach = transitive_closure(4, edges)
    assert reach[0, 3]
    assert not reach[1, 2] and not reach[2, 1]
    assert incomparable_pairs(4, edges) == [(1, 2)]


def test_redundant_transitive_edge_does_not_change_closure():
    base = [(0, 1), (1, 2), (2, 3)]
    redundant = base + [(0, 2), (1, 3), (0, 3)]
    np.testing.assert_array_equal(transitive_closure(4, base), transitive_closure(4, redundant))


@pytest.mark.parametrize("edges", [[(0, 0)], [(0, 1), (1, 0)], [(0, 1), (1, 2), (2, 0)]])
def test_cycles_are_not_strict_partial_orders(edges):
    with pytest.raises(ValueError, match="self-relation|cycle"):
        transitive_closure(3, edges)


@pytest.mark.parametrize("size", [-1, 1.5, True, "3", None])
def test_bad_size_rejected(size):
    with pytest.raises(ValueError): transitive_closure(size, [])


@pytest.mark.parametrize("edges", [[(-1, 0)], [(0, 2)], [(3, 0)]])
def test_out_of_bounds_indices_rejected(edges):
    with pytest.raises(ValueError, match="out of range"):
        transitive_closure(2, edges)


@pytest.mark.parametrize("edges", [[(0,)], [(0,1,2)], ["01"], [None]])
def test_malformed_relations_rejected(edges):
    with pytest.raises(ValueError): transitive_closure(3, edges)


@pytest.mark.parametrize("edges", [[(0, 1.0)], [(True, 1)], [("0", 1)]])
def test_noninteger_indices_rejected(edges):
    with pytest.raises(ValueError, match="integers"):
        transitive_closure(3, edges)


@pytest.mark.parametrize("seed", range(30))
def test_seeded_random_dags_are_irreflexive_antisymmetric_and_transitive(seed):
    rng = np.random.default_rng(15000 + seed)
    n = 2 + seed % 12
    perm = rng.permutation(n)
    edges = []
    for a in range(n):
        for b in range(a + 1, n):
            if rng.random() < 0.2:
                edges.append((int(perm[a]), int(perm[b])))
    reach = transitive_closure(n, edges)
    assert not np.diag(reach).any()
    assert not np.any(reach & reach.T)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if reach[i, j] and reach[j, k]:
                    assert reach[i, k]
    for i, j in incomparable_pairs(n, edges):
        assert not reach[i, j] and not reach[j, i]


def test_magnitude_matrix_does_not_supply_edges_to_partial_order():
    from mftm import coordinates_to_distances
    d = coordinates_to_distances([0, 1, 3])
    np.testing.assert_array_equal(transitive_closure(3, []), np.zeros((3, 3), dtype=bool))
    assert d[0, 1] == 1 and d[1, 2] == 2
    assert transitive_closure(3, [(0, 1), (1, 2)])[0, 2]
