# Claim and Evidence Ledger

| Claim | Epistemic class | Status at this version | Evidence / limitations |
|---|---|---|---|
| `D[i,j] = abs(t[i] - t[j])` defines nonnegative pairwise temporal magnitudes | Definition | Defined | Does not show magnitude is ontologically primary |
| `D` obeys pseudometric axioms on event labels | Theorem | Proved directly from absolute value; tested | It is a metric only if distinct labels have distinct coordinates |
| Complete exact line-distance data determine coordinates up to translation/reflection | Theorem | Proved under assumptions; numerically tested | Requires line embedding, complete labels and exact/noiseless distances |
| Reflection preserves all pairwise magnitudes | Theorem | Proved; computationally tested | Direction cannot be inferred without directional data |
| A reference origin gives a physically privileged “present” | Physical/ontological claim | Not established | Coordinate choice alone has no such implication |
| One directed relation resolves global reflection for distinct positions | Theorem | Proof sketched; computationally tested | Does not solve arbitrary incomplete/noisy layouts or timestamp ties |
| Noise affects reconstruction accuracy | Synthetic computational finding | Characterized under one declared noise model | Results are seed/noise/estimator specific; no universal monotonicity claim |
| Relativistic proper time and coordinate-time difference are generally distinct | Established theoretical distinction; illustrative code | Simple inertial example tested | Not an MFTM prediction or a full relativistic extension |
| MFTM is relevant to quantum relational time or indefinite causal order | Physical/literature hypothesis | Unresolved | Requires derivation beyond analogy and a sourced literature audit |
| MFTM makes a novel empirical prediction | Empirical hypothesis | Unresolved; no model/prediction specified | Requires observable, baseline, protocol and evidence |
| MFTM adds a novel structure beyond distance geometry | Mathematical/novelty claim | Unresolved | Requires formal definition and prior-art review |

## Evidence classes

**Definition**, **Theorem**, **Code test**, **Synthetic computational finding**, **Empirical physical finding**, **Interpretation**, **Speculation**, and **Open question** are not interchangeable. The test log records tested software behavior only. The noise sweep is synthetic and is not physical evidence.
