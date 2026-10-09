# Experiment Protocols

## Baseline reconstruction and noise sweep

Run from repository root:

```bash
PYTHONPATH=src python experiments/run_baseline.py
```

The fixed-seed noise sweep uses 50 replicates per level, 20 events, and levels 0, 1e-4, 1e-3, 1e-2, 5e-2, 0.1, 0.25 and 0.5. It writes `results/experiment_results.json` and `results/experiment_results.csv`. Metrics include pairwise RMSE against the generating true matrix, pairwise RMSE against the perturbed input, and coordinate RMSE after translation/reflection alignment.

This is a synthetic algorithmic experiment, not an experiment on physical time. Results describe the stated noise model and estimator; no universal monotonicity theorem is assumed.

## Test suite

```bash
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
```

The test suite covers Families A–J: metric axioms; transformations; reflection; MDS/reconstruction; directed constraints; an inertial proper-time illustration; quantum-scope and novelty-scope guards; reference origin/equivalence; and noise/metrics. Seeded randomized property checks are used without an additional test-generation dependency.

## Not executed

Mutation testing, exhaustive tests over all finite configurations, independent reproduction by another environment, real-world physical measurements, and a complete scholarly novelty audit are not claimed as completed.
