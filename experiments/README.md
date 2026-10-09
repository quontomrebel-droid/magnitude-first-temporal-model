# Experiment Protocols

## Baseline reconstruction and noise sweep

Run from repository root:

~~~bash
PYTHONPATH=src python experiments/run_baseline.py
~~~

The fixed-seed synthetic noise sweep uses 50 replicates per level, 20 events, and levels 0, 1e-4, 1e-3, 1e-2, 5e-2, 0.1, 0.25, and 0.5. It writes results/experiment_results.json and results/experiment_results.csv. Metrics compare raw input RMSE against the generating distance matrix with RMSE after rank-one MDS reconstruction; the output includes paired improvement and two-sided 95% Student-t intervals for means across the 50 replicates.

Each replicate seed is reused across levels, making the noise comparison paired over the same underlying coordinates and standardized noise. The confidence intervals describe this synthetic design only.

This is a synthetic algorithmic experiment, not an experiment on physical time. Results describe the stated noise model and estimator; no universal monotonicity theorem is assumed.

## Test suite and coverage

~~~bash
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
coverage erase
coverage run --branch --source=src/mftm -m pytest -q
coverage report -m
~~~

The final local run passed 515 tests. Branch-aware coverage was 100% of 171 statements and 84 branches across src/mftm's four production modules. The suite covers metric axioms; affine transformations; reflection; MDS/reconstruction; directed constraints; an inertial proper-time illustration; quantum-scope and novelty-scope guards; reference origins; synthetic noise; partial orders; and validation/error paths.

## Not executed

Mutation testing, exhaustive tests over all finite configurations, independent reproduction by another environment, real-world physical measurements, and a complete scholarly novelty audit are not claimed as completed.
