"""Generate reproducible synthetic MFTM reconstruction diagnostics.

Run: PYTHONPATH=src python experiments/run_baseline.py
These experiments are synthetic algorithm checks, not empirical physics.
"""
from __future__ import annotations

import csv
import json
import platform
from pathlib import Path

import numpy as np

from mftm import (
    align_coordinates,
    coordinates_to_distances,
    reconstruct_coordinates_1d,
    reconstruction_residuals,
)

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)
MASTER_SEED = 20261009
REPLICATES = 50
NOISE_LEVELS = [0.0, 1e-4, 1e-3, 1e-2, 5e-2, 0.1, 0.25, 0.5]
# Two-sided 95% Student-t critical value for 49 degrees of freedom.
T_CRITICAL_975_DF49 = 2.009575237


def _summary(values: list[float]) -> dict[str, float]:
    """Summarize replicate-level values with a t interval for the mean."""
    arr = np.asarray(values, dtype=np.float64)
    mean = float(np.mean(arr))
    sd = float(np.std(arr, ddof=1)) if arr.size > 1 else 0.0
    half_width = T_CRITICAL_975_DF49 * sd / np.sqrt(arr.size) if arr.size > 1 else 0.0
    return {
        "mean": mean,
        "median": float(np.median(arr)),
        "sd": sd,
        "ci95_t_low": float(mean - half_width),
        "ci95_t_high": float(mean + half_width),
    }


def noise_experiment() -> list[dict[str, float | int | None]]:
    """Compare raw noisy data with a rank-one MDS reconstruction.

    Each replicate uses the same seed across noise levels, forming a paired
    design over the same underlying coordinate sample and standardized noise.
    The t intervals describe replicate-to-replicate means under this synthetic
    design; they do not quantify uncertainty about physical time.
    """
    rows: list[dict[str, float | int | None]] = []
    for sigma in NOISE_LEVELS:
        raw_input_rmse: list[float] = []
        reconstructed_rmse_true: list[float] = []
        reconstructed_rmse_observed: list[float] = []
        aligned_coordinate_rmse: list[float] = []
        paired_rmse_improvement: list[float] = []
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

            raw_rmse = float(np.sqrt(np.mean(np.square(observed - true_d))))
            fitted_rmse = float(np.sqrt(np.mean(np.square(reconstructed_d - true_d))))
            raw_input_rmse.append(raw_rmse)
            reconstructed_rmse_true.append(fitted_rmse)
            reconstructed_rmse_observed.append(float(np.sqrt(np.mean(np.square(reconstructed_d - observed)))))
            aligned_coordinate_rmse.append(float(np.sqrt(np.mean(np.square(aligned - x)))))
            paired_rmse_improvement.append(raw_rmse - fitted_rmse)

        raw_summary = _summary(raw_input_rmse)
        reconstruction_summary = _summary(reconstructed_rmse_true)
        improvement_summary = _summary(paired_rmse_improvement)
        relative_improvement = (
            100.0 * (raw_summary["mean"] - reconstruction_summary["mean"]) / raw_summary["mean"]
            if raw_summary["mean"] > 0.0 else None
        )
        rows.append({
            "noise_sigma": sigma,
            "replicates": REPLICATES,
            "raw_input_rmse_vs_true_mean": raw_summary["mean"],
            "raw_input_rmse_vs_true_median": raw_summary["median"],
            "raw_input_rmse_vs_true_sd": raw_summary["sd"],
            "raw_input_rmse_vs_true_ci95_t_low": raw_summary["ci95_t_low"],
            "raw_input_rmse_vs_true_ci95_t_high": raw_summary["ci95_t_high"],
            "reconstructed_rmse_vs_true_mean": reconstruction_summary["mean"],
            "reconstructed_rmse_vs_true_median": reconstruction_summary["median"],
            "reconstructed_rmse_vs_true_sd": reconstruction_summary["sd"],
            "reconstructed_rmse_vs_true_ci95_t_low": reconstruction_summary["ci95_t_low"],
            "reconstructed_rmse_vs_true_ci95_t_high": reconstruction_summary["ci95_t_high"],
            "reconstructed_rmse_vs_observed_mean": float(np.mean(reconstructed_rmse_observed)),
            "coordinate_rmse_after_isometry_mean": float(np.mean(aligned_coordinate_rmse)),
            "coordinate_rmse_after_isometry_median": float(np.median(aligned_coordinate_rmse)),
            "paired_raw_minus_reconstructed_rmse_mean": improvement_summary["mean"],
            "paired_rmse_improvement_ci95_t_low": improvement_summary["ci95_t_low"],
            "paired_rmse_improvement_ci95_t_high": improvement_summary["ci95_t_high"],
            "fraction_replicates_reconstruction_better": float(np.mean(np.asarray(paired_rmse_improvement) > 0.0)),
            "relative_reduction_in_mean_rmse_pct": relative_improvement,
        })
    return rows


def exact_reconstruction_experiment() -> list[dict[str, float | int]]:
    rows: list[dict[str, float | int]] = []
    for n in [2, 3, 5, 10, 20, 50, 100]:
        rng = np.random.default_rng(MASTER_SEED + n)
        x = rng.normal(size=n)
        d = coordinates_to_distances(x)
        rec = reconstruct_coordinates_1d(d)
        metrics = reconstruction_residuals(d, rec)
        rows.append({"n_events": n, **metrics})
    return rows


def main() -> None:
    noise_rows = noise_experiment()
    exact_rows = exact_reconstruction_experiment()
    metadata = {
        "project": "Magnitude-First Temporal Model (MFTM)",
        "run_date": "2026-10-09",
        "classification": "synthetic computational experiment; not empirical physics",
        "python_version": platform.python_version(),
        "numpy_version": np.__version__,
        "master_seed": MASTER_SEED,
        "noise_replicates_per_level": REPLICATES,
        "noise_levels_sigma": NOISE_LEVELS,
        "exact_reconstruction_event_counts": [r["n_events"] for r in exact_rows],
        "methods": {
            "noise": "symmetric Gaussian perturbation of full pairwise distance matrices; clamp at zero; rank-one spectral reconstruction (strict=False)",
            "paired_design": "each replicate seed fixes the underlying coordinate vector and standardized noise across noise levels",
            "alignment": "best of translation/reflection for coordinate RMSE",
            "uncertainty": "two-sided 95% Student-t interval for the mean of 50 replicate-level values (df=49)",
            "metrics": "raw noisy matrix RMSE vs true; rank-one reconstructed matrix RMSE vs true and observed; paired error reduction; coordinate RMSE",
        },
        "caveats": [
            "Input points and perturbations are synthetic, not physical measurements.",
            "Observed symmetric entries use symmetrized Gaussian perturbations and non-negative clipping.",
            "Noise levels are in the same arbitrary coordinate units as the generated synthetic coordinates.",
            "The confidence intervals describe this simulation design only.",
            "No universal monotonicity theorem or physical prediction is asserted.",
        ],
        "exact_reconstruction": exact_rows,
        "noise_sweep": noise_rows,
    }
    (RESULTS / "experiment_results.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    with (RESULTS / "experiment_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(noise_rows[0].keys()))
        writer.writeheader()
        writer.writerows(noise_rows)
    print(f"Seed: {MASTER_SEED}; replicates per noise level: {REPLICATES}; levels: {len(NOISE_LEVELS)}")
    print("Exact reconstruction checks:")
    for row in exact_rows:
        print(f"  n={row['n_events']:>3}: max_abs={row['max_abs_error']:.3e}; RMSE={row['rmse']:.3e}")
    print("Noise sweep (mean distance-matrix RMSE vs true matrix):")
    for row in noise_rows:
        raw = float(row["raw_input_rmse_vs_true_mean"])
        fitted = float(row["reconstructed_rmse_vs_true_mean"])
        reduction = row["relative_reduction_in_mean_rmse_pct"]
        reduction_text = "n/a (zero-noise baseline)" if reduction is None else f"{float(reduction):.2f}%"
        print(
            f"  sigma={row['noise_sigma']:<7g} raw={raw:.6g} reconstructed={fitted:.6g} "
            f"reduction={reduction_text} better_replicates={float(row['fraction_replicates_reconstruction_better']):.0%}"
        )
    print(f"Wrote {RESULTS / 'experiment_results.json'}")
    print(f"Wrote {RESULTS / 'experiment_results.csv'}")


if __name__ == "__main__":
    main()
