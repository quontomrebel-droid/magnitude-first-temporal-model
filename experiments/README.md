# Experiment Protocols

## Baseline reconstruction and noise sweep

Run from repository root:

\`\`\`bash
PYTHONPATH=src python experiments/run_baseline.py
\`\`\`

The script uses fixed seeds, 50 replicates per noise level, 20 events for the noise sweep, and levels `0, 1e-4, 1e-3, 1e-2, 5e-2, 0.1, 0.25, 0.5`. It writes `results/experiment_results.json` and `.csv`. Metrics include pairwise RMSE against the generating true matrix, pairwise RMSE against the perturbed input, and coordinate RMSE after translation/reflection alignment.

This is a synthetic algorithmic experiment, not an experiment on physical time. Results describe the stated noise model and estimator; no universal monotonicity theorem is assumed.

## Test suite

\`\`\`bash
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
\`\`\`

The suite covers Family A–J: metric axioms; affine transformations; reflection; MDS/reconstruction; directed constraints; an inertial proper-time illustration; quantum-scope guard; novelty-scope guard; origin/equivalence; and noise/metrics. Seeded randomized property checks are used without an additional test-generation dependency.

## Not executed in this baseline

Mutation testing, exhaustive tests over all finite configurations, independent reproduction by another environment, real-world physical measurements, and a complete scholarly novelty audit are not claimed as completed.
