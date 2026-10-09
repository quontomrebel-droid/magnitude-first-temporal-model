# Preregistered Hypothesis Registry (MFTM)

This registry follows the current formal specification. It separates mathematical propositions from representational, statistical, philosophical, and physical hypotheses. Statuses describe the evidence actually available in this repository; synthetic computations are not empirical physical evidence.

| ID | Hypothesis | Classification | Current status | What would change the status |
|---|---|---|---|---|
| H1 | Distance sufficiency: exact complete distances from points known to lie on a line determine the configuration up to translation/reflection | Mathematical proposition | **Proved under stated assumptions** | A counterexample under the exact assumptions; proof and computational checks are in THEORY.md and tests |
| H2 | Orientation non-identifiability: global reflection preserves all pairwise magnitudes | Mathematical proposition | **Proved** | The defining absolute-distance identity would have to fail; exact proof in THEORY.md |
| H3 | Reference-point sufficiency: setting one event to zero changes origin but adds no global orientation information | Representational claim | **Proved as a coordinate identity** | A stated model in which changing origin changes orientation information without adding a directional constraint |
| H4 | Ordering recovery: one directed relation between distinct positions breaks global reflection ambiguity of a non-degenerate line reconstruction | Mathematical proposition | **Proved under stated assumptions; implementation tested** | Counterexample under complete exact line distances plus stated assumptions; ties need separate treatment |
| H5 | Noise-dependent identifiability: reconstruction residual and reliability depend on noise level/structure | Statistical inference problem | **Characterized computationally; not a universal monotonicity theorem** | Replicated protocols, uncertainty intervals, alternative noise models, and held-out validation |
| H6 | Relativistic compatibility: the representation can be compared with relativity without conflating coordinate intervals with proper time | Physical/theoretical question | **Unresolved** | A fully specified relativistic mapping and consistency analysis against established formalism |
| H7 | Quantum relevance: MFTM supplies a nontrivial connection to relational clocks or indefinite causal order | Literature/physical hypothesis | **Unresolved** | A derivation adding explanatory or predictive content beyond cited frameworks; analogy alone is insufficient |
| H8 | Empirical novelty: MFTM produces an observable prediction different from an established baseline | Empirical hypothesis | **Unresolved; no prediction specified** | Explicit observable, model, parameterization, baseline, test protocol, and evidence |
| H9 | Representational equivalence: complete exact 1-D distance data and coordinates represent the same configuration modulo isometries | Mathematical proposition | **Proved under stated assumptions** | Counterexample under complete exact line-distance assumptions |
| H10 | Novel structure: magnitude-first formalization introduces a nontrivial structure not already captured by distance geometry/equivalent formulations | Mathematical/novelty question | **Unresolved** | Formal definition, prior-art review, and a theorem or consequence not equivalent to known results |

## Scoring vocabulary

- **Proved:** a mathematical argument establishes the proposition under explicit assumptions.
- **Disproved:** a counterexample violates the proposition under those assumptions.
- **Supported computationally:** implemented tests pass for tested cases; this does not replace a proof.
- **Unresolved:** available evidence does not decide the claim.
- **Not empirically testable (as currently stated):** no operational observable or discriminating test has been specified.

These statuses are versioned research bookkeeping. Physical hypotheses H6–H8 and the novelty question H10 must not be promoted based solely on unit tests.
