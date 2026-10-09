# Magnitude-First Temporal Model (MFTM)

**Status: mathematical specification and baseline computational checks. No new physical theory or empirical prediction is claimed.**

MFTM studies the information content and limits of representing temporal coordinates by non-negative pairwise magnitudes:

\[
D(e_i,e_j)=|t_i-t_j|.
\]

It distinguishes a representational choice from claims about the ontology of time and from physical predictions. Read [THEORY.md](THEORY.md), [HYPOTHESES.md](HYPOTHESES.md), and [the claim ledger](docs/CLAIM_LEDGER.md) before interpreting outputs.

## Main mathematical result

For a finite, complete, exact distance matrix known to come from points on a Euclidean line, coordinates are determined up to translation and reflection. Translation sets the origin; reflection reverses orientation without changing any pairwise magnitude. A single directed relation between two distinct positions chooses the global orientation under these assumptions. See the proof sketches and assumptions in THEORY.md.

The matrix \(D\) is a **pseudometric** on event labels when multiple labels may share a timestamp. It is a metric only when distinct labels have distinct coordinates. Classical MDS uses

\[
B=-\frac12 JD^{(2)}J,\qquad J=I-\frac1n\mathbf1\mathbf1^T.
\]

For an exact line embedding, \(B\) is positive semidefinite and has rank at most one, apart from numerical tolerance.

## What the code can establish

The Python implementation computes pairwise magnitudes, validates matrix properties and pseudometric axioms, reconstructs a rank-one line embedding through MDS, aligns reconstruction under translation/reflection, applies a directed-order constraint, provides an explicitly limited inertial proper-time example, and computes explicitly supplied partial-order closure without inferring order from distances. The test suite checks mathematical identities and code behavior. The synthetic noise sweep measures reconstruction behavior for one declared simulation design.

The tests do **not** establish that magnitude is ontologically more fundamental, identify a universal present, explain aging, validate a quantum connection, or demonstrate a novel physical prediction. H6–H8 and H10 remain unresolved.

## Reproduce

Requires Python 3.10+, NumPy, and pytest for tests.

```bash
python -m pip install -e '.[test]'
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
PYTHONPATH=src python experiments/run_baseline.py
```

The committed result files record the synthetic experiment and test execution. Fixed random seeds are used. For exact details and caveats, see experiments/README.md and results/experiment_results.json.

The expanded local suite currently passes 502 tests across the core, property-style, specification, and partial-order modules. This is software-level evidence only. The partial-order helper tests alternative order structures as explicitly supplied constraints; it does not infer causal edges from magnitudes.\n\n## Hypothesis registry

The formal registry is H1–H10 in HYPOTHESES.md. Each item has a classification, current status, and status-change criterion. Status labels distinguish proof from computational support and from empirical physical evidence.

## Prior art

A review protocol is in literature/REVIEW_PROTOCOL.md. Relational quantum clocks, indefinite causal order, special relativity, and classical distance geometry are research leads, not evidence that MFTM is novel. A full sourced bibliography and novelty review remain outstanding.

## License

No license has been selected. All rights are reserved by the copyright holder unless a license is subsequently added.
