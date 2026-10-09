"""Reproducible synthetic MFTM reconstruction diagnostics; not empirical physics."""
from __future__ import annotations
import csv, json, platform
from pathlib import Path
import numpy as np
from mftm import align_coordinates, coordinates_to_distances, reconstruct_coordinates_1d, reconstruction_residuals

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
MASTER_SEED = 20261009
REPLICATES = 50
NOISE_LEVELS = [0.0, 1e-4, 1e-3, 1e-2, 5e-2, 0.1, 0.25, 0.5]


def noise_experiment():
    rows = []
    for sigma in NOISE_LEVELS:
        err_true, err_observed, err_coordinates = [], [], []
        for replicate in range(REPLICATES):
            rng = np.random.default_rng(MASTER_SEED + replicate)
            x = np.sort(rng.uniform(-10.0, 10.0, size=20))
            true_d = coordinates_to_distances(x)
            noise = rng.normal(0.0, sigma, size=true_d.shape)
            noise = (noise + noise.T) / 2.0
            np.fill_diagonal(noise, 0.0)
            observed = np.maximum(0.0, true_d + noise)
            reconstructed = reconstruct_coordinates_1d(observed, strict=False)
            reconstructed_d = coordinates_to_distances(reconstructed)
            aligned = align_coordinates(x, reconstructed)
            err_true.append(float(np.sqrt(np.mean((reconstructed_d - true_d) ** 2))))
            err_observed.append(float(np.sqrt(np.mean((reconstructed_d - observed) ** 2))))
            err_coordinates.append(float(np.sqrt(np.mean((aligned - x) ** 2))))
        rows.append({
            "noise_sigma": sigma, "replicates": REPLICATES,
            "pairwise_rmse_vs_true_mean": float(np.mean(err_true)),
            "pairwise_rmse_vs_true_median": float(np.median(err_true)),
            "pairwise_rmse_vs_true_sd": float(np.std(err_true, ddof=1)),
            "pairwise_rmse_vs_observed_mean": float(np.mean(err_observed)),
            "coordinate_rmse_after_isometry_mean": float(np.mean(err_coordinates)),
            "coordinate_rmse_after_isometry_median": float(np.median(err_coordinates)),
        })
    return rows


def exact_reconstruction_experiment():
    rows = []
    for n in [2, 3, 5, 10, 20, 50, 100]:
        rng = np.random.default_rng(MASTER_SEED + n)
        x = rng.normal(size=n)
        d = coordinates_to_distances(x)
        rec = reconstruct_coordinates_1d(d)
        rows.append({"n_events": n, **reconstruction_residuals(d, rec)})
    return rows


def main():
    noise_rows = noise_experiment()
    exact_rows = exact_reconstruction_experiment()
    result = {
        "project": "Magnitude-First Temporal Model (MFTM)",
        "generated_date": "2026-10-09",
        "classification": "synthetic computational experiment; not empirical physics",
        "python_version": platform.python_version(), "numpy_version": np.__version__,
        "master_seed": MASTER_SEED, "noise_replicates_per_level": REPLICATES,
        "noise_levels_sigma": NOISE_LEVELS,
        "methods": {
            "noise": "symmetric Gaussian perturbation of complete pairwise distances; clamp at zero; rank-one spectral reconstruction (strict=False)",
            "alignment": "best of translation/reflection against synthetic generating coordinates",
            "metrics": "pairwise RMSE vs true and observed matrices; coordinate RMSE",
        },
        "caveats": [
            "Input points and noise are synthetic.",
            "Observed symmetric entries reuse symmetrized Gaussian noise.",
            "No universal monotonicity law is asserted.",
            "Results assess this code and noise protocol, not physical time.",
        ],
        "exact_reconstruction": exact_rows, "noise_sweep": noise_rows,
    }
    (RESULTS / "experiment_results.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    with (RESULTS / "experiment_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(noise_rows[0].keys()))
        writer.writeheader()
        writer.writerows(noise_rows)
    print(f"Seed: {MASTER_SEED}; replicates per noise level: {REPLICATES}; levels: {len(NOISE_LEVELS)}")
    print("Exact reconstruction checks:")
    for r in exact_rows:
        print(f"  n={r['n_events']:>3}: max_abs={r['max_abs_error']:.3e}; RMSE={r['rmse']:.3e}")
    print("Noise sweep (synthetic; RMSE vs true distance matrix):")
    for r in noise_rows:
        print(f"  sigma={r['noise_sigma']:<7g} mean={r['pairwise_rmse_vs_true_mean']:.6g} median={r['pairwise_rmse_vs_true_median']:.6g} sd={r['pairwise_rmse_vs_true_sd']:.6g}")
    print(f"Wrote {RESULTS / 'experiment_results.json'}")
    print(f"Wrote {RESULTS / 'experiment_results.csv'}")


if __name__ == "__main__":
    main()
