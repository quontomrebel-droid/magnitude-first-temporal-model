# Baseline Execution Report

**Classification:** software and synthetic-data checks only; no empirical physics result.

## Test suite

The suite covers `tests/test_distances.py`, `tests/test_properties.py`, `tests/test_specification_extended.py`, and `tests/test_partial_order.py`. Coverage includes pseudometric axioms, randomized invariance, MDS reconstruction, reflection-blindness controls, directed relations, proper-time example checks, synthetic noise diagnostics, and partial-order closure/incomparability.

- Command: `PYTHONPATH=src pytest -q --junitxml=results/junit.xml`
- Tests: 502 passed, 0 failures, 0 errors, 0 skipped.
- Python: 3.13.5; NumPy: 2.3.5.

## Exact line reconstruction

For seeded synthetic line embeddings with 2, 3, 5, 10, 20, 50 and 100 events, maximum pairwise reconstruction error ranged from zero to approximately 7.55e-15 in this run. This is floating-point reconstruction behavior for known synthetic coordinates.

## Noise sweep

The experiment used 50 replicates at each of eight symmetric Gaussian noise levels with 20 events and master seed 20261009. Mean RMSE of reconstructed distances relative to the generating true distance matrix rose from about 2.74e-15 at zero noise to 0.177 at sigma 0.5 in this specific design. These figures describe this estimator/noise protocol only; they do not establish a universal noise law or provide evidence about physical time. Full metrics are in `experiment_results.csv` and `experiment_results.json`.

## Hypothesis decisions

H1–H3 and H9 are mathematical/representational results under the assumptions stated in THEORY.md. H4 is tested computationally, with a proof sketch. H5 is characterized under one synthetic noise model. H6, H7, H8 and H10 remain unresolved. The results do not establish ontological priority, a universal present, an explanation of aging, quantum relevance, or empirical novelty.

## Reproduction commands

```bash
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
PYTHONPATH=src python experiments/run_baseline.py
```
