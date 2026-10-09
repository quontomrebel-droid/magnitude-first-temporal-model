# Magnitude-First Temporal Model (MFTM)
## Mathematical and Computational Baseline Report

**Author:** Khaled Al-Mahdy  
**Report date:** 9 October 2026  
**Project version:** 0.2.0  
**Repository:** https://github.com/quontomrebel-droid/magnitude-first-temporal-model  
**Evidence status:** Reproducible mathematical and synthetic-computational baseline; no empirical physical finding or novel physical prediction established.

---

## Technical summary

The current MFTM implementation is behaving as expected on its stated mathematical domain. The final local verification run passed **515 pytest cases**; the test-coverage run covered **all 171 statements and all 84 branches** in the four production modules under src/mftm. Editable package installation and Python byte-compilation also succeeded. These results support implementation correctness for the tested inputs, not the truth of a new physical theory.

The central mathematical conclusions are already standard consequences of one-dimensional distance geometry. Given a complete, exact pairwise distance matrix known to come from points on a Euclidean line, the coordinates are determined up to translation and reflection. Translation leaves the choice of origin undetermined; reflection leaves global orientation undetermined. A single reliable directed relation between two distinct positions selects one of the two orientations. The classical multidimensional-scaling Gram matrix gives a corresponding positive-semidefinite, rank-at-most-one diagnostic. The distance/Gram connection underlying this result is established prior work, not a novelty claim for MFTM [5].

A seeded simulation with 50 replicates at each of eight noise levels shows that projecting a noisy complete distance matrix onto a one-dimensional MDS representation reduced mean distance-matrix RMSE by approximately **47.9% at noise σ = 0.5** compared with the raw noisy matrix. All 50 paired replicates showed lower RMSE after reconstruction at each non-zero noise level in this particular synthetic design. This is a useful algorithmic result about rank-one projection under the chosen Gaussian-noise protocol; it is not evidence about real clocks, aging, quantum time, or the ontology of time.

**Bottom line:** MFTM currently supplies a clear representation, a tested implementation, and a more disciplined experimental programme. It does not yet supply an established new mathematical structure, a complete relativistic or quantum extension, or a measurable prediction that distinguishes it from existing theory. The next research gate is not to run more redundant tests of the absolute-value identity; it is to define an additional structure or observable whose consequences are not already contained in distance geometry and established physics.

## 1. Question, scope, and evidence standard

This report assesses what can be established from the current formal model, Python package, automated tests, and seeded synthetic experiments. It also places the core equations against a small set of verified primary or scholarly reference anchors. It is a baseline review, not a peer-reviewed publication, not a complete literature review, and not an empirical study of time.

The report keeps four kinds of claim separate:

- **Mathematical result:** follows from definitions and stated assumptions.
- **Implementation result:** the program exhibits specified behaviour on tests that were actually run.
- **Synthetic computational finding:** describes the declared simulation, its random seeds, and its metric.
- **Physical or ontological hypothesis:** requires a physical model, an operational observable, comparison against established theory, and—where empirical claims are made—evidence capable of discriminating between them.

A passing unit test cannot establish the last category. A large number of software tests can expose implementation errors, but cannot turn a known mathematical identity into a new law of nature.

### Evidence inventory

The review used the current package under src/mftm, five pytest modules, the MDS reconstruction and noise-sweep experiment, the generated JSON/CSV outputs, the claim ledger, and the available hypothesis registry. The tests and computations were rerun locally for this report on Python 3.13.5, NumPy 2.3.5, and pytest 9.0.2. The simulation uses master seed 20261009, 50 replicates per noise level, and 20 synthetic events per replicate.

This is an evidence-bounded report. It does not claim that GitHub Actions has run successfully, that another independent machine has reproduced the outputs, that mutation testing has been completed, or that a full scholarly novelty search has been finished.

## 2. Formal model and mathematical conclusions

### 2.1 Definition and pseudometric result

Let E = {e₁, …, eₙ} be a finite set of event labels. Each event has a real-valued coordinate tᵢ on a conventional one-dimensional time coordinate. Define

\[
D(e_i,e_j)=|t_i-t_j|.
\]

This construction immediately gives:

- Non-negativity: D(eᵢ,eⱼ) ≥ 0.
- Identity on the diagonal: D(eᵢ,eᵢ) = 0.
- Symmetry: D(eᵢ,eⱼ) = D(eⱼ,eᵢ).
- Triangle inequality: D(eᵢ,eₖ) ≤ D(eᵢ,eⱼ) + D(eⱼ,eₖ).

Therefore D is a **pseudometric** on event labels. It is a metric precisely when the event-to-coordinate assignment is injective: distinct event labels must have distinct timestamps. If two distinct events share a timestamp, their distance is zero, which violates the identity-of-indiscernibles condition for a metric but does not violate the pseudometric axioms.

This is a consequence of the definition. It does not imply that temporal magnitude is ontologically prior to direction.

### 2.2 P1 / H1 — distance sufficiency

**Proposition.** A complete, exact, labelled pairwise-distance matrix generated by points known to lie on a Euclidean line determines their coordinates uniquely up to translation and reflection.

Let D² denote the elementwise squared-distance matrix. Define

\[
J=I-\frac{1}{n}\mathbf{1}\mathbf{1}^{\mathsf T},
\qquad
B=-\frac12 JD^{(2)}J.
\]

If t is the coordinate vector and x = Jt is its centred version, then for exact one-dimensional Euclidean distances,

\[
B=xx^{\mathsf T}.
\]

Thus B is positive semidefinite and has rank at most one. In the non-degenerate rank-one case, a factorisation of B recovers x up to its sign: x or −x. The original coordinates are x + c1 for an arbitrary constant c. The constant is the translation ambiguity; the sign is the reflection ambiguity. If every point coincides, B has rank zero and the configuration is still determined up to translation.

This argument proves P1 under its stated assumptions. It is not a theorem that arbitrary noisy or incomplete matrices uniquely reconstruct coordinates. Such data can be inconsistent with a line embedding and may need approximation, additional constraints, or a different model. The Euclidean-distance-matrix / Gram-matrix connection used here is standard distance geometry [5].

### 2.3 P2 / H2 — orientation non-identifiability

For any constant c, reflect the coordinates by setting t′ᵢ = c − tᵢ. Then

\[
|t'_i-t'_j|
=|(c-t_i)-(c-t_j)|
=|t_j-t_i|
=|t_i-t_j|.
\]

Every pairwise magnitude is unchanged. Therefore a magnitude-only dataset cannot distinguish the configuration from its global reflection. Any deterministic estimator that receives only D must return the same result for both members of a reflected pair. For distinct endpoints, that result cannot be correctly oriented for both cases.

This is a statement about the information represented by D. It does **not** demonstrate that physical time has no direction. It demonstrates that this representation omits signed direction information.

### 2.4 P3 / H3 — reference-point sufficiency

Choose a reference event k and define centred coordinates τᵢ = tᵢ − tₖ. Then τₖ = 0 and

\[
|\tau_i-\tau_j|=|t_i-t_j|,\qquad |\tau_i|=D(e_i,e_k).
\]

The reference event fixes the coordinate origin. Pairwise separations do not change, and orientation remains ambiguous under τ → −τ. Distances to the reference event alone provide |τᵢ|, not each signed τᵢ; a complete exact line-distance matrix can reconstruct the configuration up to the same global reflection.

Calling the reference event “now” is a coordinate convention. It does not, without additional physical structure and evidence, establish a universal or privileged present.

### 2.5 P4 / H4 — minimal orientation recovery

Assume that a valid non-degenerate line configuration has already been reconstructed from complete exact distances. The remaining global ambiguity is reflection. Supply one reliable directed relation between distinct positions, for example “event i is earlier than event j”. Exactly one of the two reflected orientations satisfies that relation. The relation therefore selects the global orientation.

The assumptions matter: the two events must occupy distinct positions; the directional constraint must be reliable and refer to the same chronology; and the complete line reconstruction must be valid. Equal-timestamp events cannot be ordered by this coordinate relation. One constraint does not, by itself, resolve every ambiguity in a general incomplete, noisy, or higher-dimensional problem.

This result is a minimal information statement, not evidence that orientation is recoverable from magnitudes alone. The direction is supplied by the added directed relation.

### 2.6 P5 / H9 — higher-dimensional configurations

Without the prior assumption that points lie on a line, a distance matrix does not by itself impose a one-dimensional chronology. A configuration with points such as (0,0), (1,0), and (0,1) has pairwise distances 1, 1, and √2. Its centred Gram matrix has rank two, so it is not exactly embeddable on a line.

A complete exact Euclidean distance matrix can determine a Euclidean configuration up to isometries in its minimal embedding space. That is not the same as selecting a linear temporal ordering or a physically preferred temporal direction. If the MFTM application needs a chronology, the model must state where the one-dimensional assumption comes from and what additional structure supports it.

## 3. Implementation and test design

### 3.1 What the software implements

The package provides:

- Pairwise magnitude construction from a finite coordinate vector.
- Matrix checks for square shape, finite values, symmetry, non-negativity, and a zero diagonal.
- Separate pseudometric validation, including the triangle inequality.
- The classical MDS centred Gram-matrix calculation.
- One-dimensional rank-one spectral reconstruction, with a strict validation mode and an explicitly approximate non-strict mode.
- Coordinate alignment under translation and reflection.
- Global orientation selection from a supplied directed relation.
- Reference-origin transformations.
- A limited special-relativistic inertial proper-time calculator.
- Strict partial-order transitive closure and incomparable-pair reporting for relations supplied explicitly by the caller.
- Distance-matrix residual metrics and reproducible synthetic noise experiments.

The partial-order functions do not infer causal edges from D. They calculate consequences of a directed relation provided as input. Likewise, the proper-time utility checks a standard formula; it does not constitute a derived MFTM relativistic extension.

### 3.2 Final automated test result

**515 tests passed; zero failures.** The final pytest run completed in 0.59 seconds in the local environment.

| Test module | Pytest cases |
|---|---:|
| Core distance utilities | 11 |
| Randomized property-style tests | 211 |
| Formal-specification tests | 207 |
| Partial-order tests | 73 |
| Validation and error-path tests | 13 |
| **Total** | **515** |

The property-style tests use seeded NumPy generation and parameterized cases; the optional Hypothesis package is not installed, and the suite does not depend on it. Mutation testing has not been run.

### 3.3 Code coverage and build checks

The final branch-aware coverage run reported:

| Package coverage measure | Result |
|---|---:|
| Production statements exercised | 171 / 171 (100%) |
| Production branches exercised | 84 / 84 (100%) |
| Production modules with 100% coverage | 4 / 4 |
| Python byte-compilation | Pass |
| Editable package installation | Pass |

Coverage applies to the executed source under src/mftm, not to every possible input, every mathematical consequence, the whole repository, or any physical hypothesis. It should be read as evidence that each measured production statement and branch was visited by the present tests—not as proof of correctness for all conceivable inputs.

The package successfully built and installed as version 0.2.0. A separate global pip check did not return clean: the preinstalled environment has a dependency conflict because moviepy 2.2.1 requires Pillow below version 12, while Pillow 12.3.0 is present. Pillow/moviepy are not MFTM dependencies. This environment-level issue should be isolated from the successful MFTM package installation.

## 4. Exact reconstruction results

The exact reconstruction experiment generated one-dimensional coordinates using fixed seeds, computed their pairwise magnitudes, reconstructed coordinates by classical MDS, and compared the reconstructed pairwise-distance matrix with the original. It used seven event counts; it was a finite diagnostic sweep, not an exhaustive proof over all configurations.

| Events | Maximum absolute pairwise error | Pairwise RMSE |
|---:|---:|---:|
| 2 | 0 | 0 |
| 3 | 2.22 × 10⁻¹⁶ | 1.17 × 10⁻¹⁶ |
| 5 | 1.78 × 10⁻¹⁵ | 1.10 × 10⁻¹⁵ |
| 10 | 1.33 × 10⁻¹⁵ | 4.98 × 10⁻¹⁶ |
| 20 | 2.66 × 10⁻¹⁵ | 8.00 × 10⁻¹⁶ |
| 50 | 2.89 × 10⁻¹⁵ | 6.38 × 10⁻¹⁶ |
| 100 | 7.55 × 10⁻¹⁵ | 1.18 × 10⁻¹⁵ |

The largest reported maximum absolute error across these seven configurations was approximately 7.55 × 10⁻¹⁵. Those errors are consistent with floating-point round-off for the scales involved. The result shows that the implementation reconstructs these known synthetic line configurations to numerical precision; it does not establish a new theorem beyond P1.

## 5. Noise experiment: rank-one projection reduced error under the declared synthetic model

### 5.1 Design

The experiment used 20 synthetic events per replicate; 50 seeded replicates per noise level; and eight Gaussian perturbation scales: σ ∈ {0, 0.0001, 0.001, 0.01, 0.05, 0.1, 0.25, 0.5}. Coordinates were sampled on a real line from a fixed distribution. Independent standard-normal perturbation arrays were symmetrized, added to the complete distance matrix, and clipped at zero. The reconstruction then used the leading spectral component of the centred Gram matrix in non-strict mode.

The same replicate seed was reused across all noise levels. This creates a paired comparison: within a replicate, the coordinate sample and standardized noise draw are held constant while σ changes. For each replicate, the raw noisy-matrix RMSE and reconstructed-matrix RMSE were both measured against the generating true distance matrix. A two-sided 95% Student-t interval with 49 degrees of freedom was calculated for each mean across the 50 replicate-level values. Intervals quantify the simulation design only.

### 5.2 Main quantitative result

At the largest tested noise level, σ = 0.5, the raw noisy distance matrix had mean RMSE **0.3400** against the true distance matrix. The one-dimensional reconstruction had mean RMSE **0.1771**. The reduction in mean RMSE was **47.93%**. The paired reduction in RMSE was 0.1630, with a 95% t interval of approximately [0.1529, 0.1730]. The reconstructed matrix had lower RMSE than the raw noisy matrix in **50 of 50 replicates** at that non-zero noise level.

| Noise σ | Raw matrix RMSE vs true (mean; 95% t CI) | Reconstructed RMSE vs true (mean; 95% t CI) | Reduction in mean RMSE | Replicates where reconstruction improved |
|---:|---|---|---:|---:|
| 0 | 0; exact raw input | 2.74 × 10⁻¹⁵ (round-off) | Not applicable | 0 / 50 |
| 0.0001 | 0.0000686 [0.0000675, 0.0000697] | 0.0000355 [0.0000337, 0.0000374] | 48.18% | 50 / 50 |
| 0.001 | 0.000686 [0.000675, 0.000697] | 0.000355 [0.000337, 0.000374] | 48.18% | 50 / 50 |
| 0.01 | 0.00686 [0.00675, 0.00697] | 0.00355 [0.00337, 0.00374] | 48.18% | 50 / 50 |
| 0.05 | 0.03428 [0.03372, 0.03484] | 0.01777 [0.01686, 0.01868] | 48.18% | 50 / 50 |
| 0.1 | 0.06849 [0.06737, 0.06961] | 0.03549 [0.03367, 0.03731] | 48.18% | 50 / 50 |
| 0.25 | 0.17076 [0.16794, 0.17358] | 0.08858 [0.08405, 0.09312] | 48.12% | 50 / 50 |
| 0.5 | 0.34001 [0.33437, 0.34566] | 0.17706 [0.16796, 0.18615] | 47.93% | 50 / 50 |

### 5.3 Interpretation and limitations

The reduction is expected to be possible because the generating configurations really are one-dimensional, and the reconstruction explicitly projects the perturbed data onto a rank-one line model. The raw input contains perturbations inconsistent with that structure; enforcing the known structural constraint filters some of that error.

The result supports a limited algorithmic conclusion: **for this full-matrix, symmetric Gaussian-noise design, the rank-one reconstruction is a better estimate of the synthetic generating distance matrix than the raw perturbed matrix under the chosen RMSE metric.** It does not show that this estimator is optimal, that the effect generalizes to other noise processes, or that real temporal measurements follow this model.

Important limits:

- Points, perturbations, and their units are synthetic and arbitrary.
- Only complete matrices are tested in the experiment; missing entries are rejected rather than imputed.
- Non-negative clipping modifies the Gaussian noise distribution, especially for small underlying distances.
- The model dimension is known to be one because the data were generated from a line.
- The study does not compare alternative denoisers, noise distributions, outlier models, clock datasets, or physical predictions.
- Repetition across noise levels uses paired seeds, so rows are designed to be compared but are not independent across levels.
- The near-constant percentage reduction across several levels is a property of this simulation and estimator; it is not a universal error law.

## 6. Orientation control: magnitude-only data cannot select a global arrow

The deterministic paired-reflection control used 100 seeded line configurations, each presented in both orientations: 200 timeline cases in total. Each pair produced exactly the same distance matrix. The fixed eigensolver-based reconstruction classified 100 of the 200 timelines with the correct endpoint order, or 50%.

That 50% is not a measured limitation of all possible algorithms. It is the expected identifiability control for a deterministic rule that receives identical input for two opposite true orientations: its output is the same for both, so one of the two must be wrong whenever the endpoints differ. Additional direction-sensitive information can resolve that symmetry; the magnitude matrix cannot.

The orientation tests also checked that a supplied directed relation selects the reflected coordinate solution that satisfies the chosen “before” or “after” constraint while preserving the distance matrix. Again, direction is restored by the new relation, not discovered inside D.

## 7. Partial orders and alternative structures

The implementation includes a small, explicit strict-partial-order utility. It computes transitive closure and incomparable event pairs from supplied directed edges. Tests cover chains, antichains, diamonds, redundant transitive edges, cycle detection, malformed input, and 30 seeded random directed acyclic graphs.

This is useful scaffolding for comparing magnitude representations with order-based representations. It does not establish that causal sets, partial orders, or graphs emerge from MFTM. The crucial data distinction remains: a symmetric distance matrix and a directed precedence relation are different inputs with different information content. Any proposed mapping between them must be specified and tested rather than assumed.

## 8. H1–H10 status assessment

| ID | Hypothesis | Classification | Current assessment |
|---|---|---|---|
| H1 | Distance sufficiency | Mathematical proposition | **Proved under assumptions.** Complete, exact, labelled line distances determine the coordinates up to translation/reflection; tested numerically. |
| H2 | Orientation non-identifiability | Mathematical proposition | **Proved.** Reflection invariance follows algebraically; the paired-reflection control illustrates the consequence for a deterministic estimator. |
| H3 | Reference-point sufficiency | Representational claim | **Proved as a coordinate identity.** A named origin removes translation freedom but not global reflection. |
| H4 | Ordering recovery with minimal extra information | Mathematical proposition | **Proved under stated assumptions; implementation tested.** One reliable directed relation between distinct positions selects the global orientation of a valid line reconstruction. |
| H5 | Noise-dependent identifiability | Statistical inference problem | **Characterized computationally for one synthetic design.** The rank-one projection reduced RMSE in these paired replicates; generalization is unresolved. |
| H6 | Relativistic compatibility | Physical/theoretical question | **Unresolved.** The code contains only the standard inertial proper-time relation; there is no completed MFTM spacetime formulation. |
| H7 | Quantum relevance | Literature/physical hypothesis | **Unresolved.** Related work exists, but no MFTM-specific derivation or testable consequence has been produced. |
| H8 | Empirical novelty | Empirical hypothesis | **Unresolved; no observable prediction specified.** No physical data or distinctive prediction is present. |
| H9 | Representational equivalence | Mathematical proposition | **Proved under assumptions; established prior art.** The line-distance/MDS reconstruction is standard distance geometry [5]. |
| H10 | Novel structure | Mathematical/novelty question | **Unresolved.** The current core definition does not itself supply a structure beyond absolute coordinate differences; full prior-art review remains necessary. |

“Proved” here means a mathematical statement follows under the listed assumptions. “Supported computationally” means tested implementation behaviour. Neither label means an empirical physical hypothesis has been confirmed. H6–H8 and H10 should not be promoted based on software tests.

## 9. Literature review and novelty audit

### 9.1 Distance geometry is the nearest mathematical prior art

The equation Dᵢⱼ = |tᵢ − tⱼ| is the ordinary Euclidean distance between real coordinates. The centring identity B = −½JD²J is the classical distance/Gram relationship used in multidimensional scaling. Schoenberg’s foundational work and modern distance-geometry accounts establish the link between Euclidean distance matrices and positive-semidefinite Gram matrices [5]. As a consequence, the rank-one reconstruction and reflection ambiguity in this report should be treated as re-derived known mathematics, not as new MFTM theorems.

The novelty test is therefore stronger than “can the model be written in terms of unsigned distances?” The project must identify some additional axiom, invariant, empirical consequence, or formal structure that is not equivalent to standard distance geometry plus a coordinate convention. Until that is done, **novelty of the core mathematical representation is unestablished and the risk of restatement is high**. This is a preliminary audit, not a claim that every possible extension has already been found in the literature.

### 9.2 Relational quantum time does not imply unsigned temporal magnitude

Page and Wootters proposed describing observed dynamics through correlations with readings of an internal clock in a globally stationary formalism [1]. Later work has developed the Page–Wootters approach for tasks such as parallel-in-time quantum simulation, including a 2025 *Physical Review Research* publication [2]. Those results motivate research into relational time, but they do not derive Dᵢⱼ = |tᵢ − tⱼ| as a fundamental ontology, establish that ordering can be discarded, or supply an MFTM-specific prediction.

### 9.3 Indefinite causal order is a separate concept

The quantum-switch framework considers processes that cannot be represented as inserting operations into one predefined causal order in the usual circuit description [3]. Rubino and colleagues reported an experimental verification of indefinite causal order in a quantum-switch setting [4]. These are important operational results, but neither implies that ordinary past and future are generally interchangeable or that a symmetric temporal-distance matrix can replace all causal or directional structure.

### 9.4 Relativity requires an explicit mapping

For inertial motion at constant speed v in flat spacetime, the standard relation is

\[
\Delta\tau=\Delta t\sqrt{1-v^2/c^2}.
\]

Proper time is accumulated along a clock’s worldline; a coordinate-time difference is assigned relative to a chosen coordinate frame. The implementation’s helper function tests this standard example. It does not show that MFTM is compatible with every relativistic setting. A real extension must specify the events, worldline, spacetime metric, observer or coordinate frame, and observable to which the magnitude-first quantities correspond.

## 10. Adversarial red-team assessment

The strongest skeptical reading is currently straightforward:

1. **The central formula is familiar.** Absolute differences on the real line are standard distances. The MDS Gram calculation is classical. Renaming this representation “magnitude-first” does not alone create a new theorem.
2. **The orientation result is a symmetry, not a discovery about physical time.** D intentionally discards the sign of each coordinate difference. Its inability to recover the global sign follows from that information loss.
3. **The minimal extra-direction result is structurally simple.** A directed relation chooses one of two reflected reconstructions. The relation is external information; the magnitudes did not generate it.
4. **The noise result depends on the assumed model class.** The coordinates are deliberately generated on a line and reconstructed on a line. The observed RMSE reduction is relevant to this estimator under this noise model, but has not been compared with competing estimators or validated with physical observations.
5. **Quantum literature is motivation, not validation.** Relational-clock and indefinite-causal-order work involves defined physical frameworks, quantum states or processes, and operational predictions. The MFTM code currently contains none of that machinery.
6. **The relativistic example is standard physics.** A helper calculation is a consistency illustration, not a new result of MFTM.
7. **The evidence chain stops before the physical claim.** No new observable, baseline discrepancy, measured dataset, or pre-specified falsification threshold is defined.

The strongest justified positive conclusion is that the current mathematical baseline is explicitly specified and its implementation is heavily tested. The strongest justified negative conclusion is that no novel physical prediction has yet been established. Both should remain visible in all future presentations.

## 11. Limitations and uncertainty

- The code and tests check mathematical and implementation behaviours, not whether temporal magnitude is ontologically more fundamental.
- Complete, finite distance matrices are the main input domain. Incomplete matrices are rejected; a completion algorithm is not implemented.
- The numerical tolerances are software choices. The present test scale range is finite; extreme scale/conditioning behaviour still deserves dedicated analysis.
- The synthetic noise model is symmetric Gaussian perturbation followed by non-negative clipping. It is not a validated model of clock measurement errors.
- Confidence intervals estimate replicate-level simulation means for a fixed design. They are not confidence intervals for any physical constant or general MFTM claim.
- No mutation-testing campaign or independent external reproduction is reported.
- The partial-order extension operates only on supplied relation edges.
- The quantum and relativity connections have not been derived formally.
- The reference list below is a set of verified anchors, not an exhaustive bibliography; the novelty audit remains open.
- The environment-wide pip check reported an unrelated moviepy/Pillow version conflict; MFTM itself installed successfully.

## 12. Recommended next steps

### Priority 1 — Freeze the claim boundaries

Keep the formal model, hypotheses, and claim ledger versioned. For each claim, record the assumptions, evidence class, test, possible counterexample, and status-change rule. Preserve the distinction between signed coordinate chronology, causal precedence, thermodynamic arrow, proper time, and any proposed universal present.

### Priority 2 — Harden computational verification

Add mutation testing and an independent implementation of the one-dimensional reconstruction theorem. Evaluate extreme magnitudes, clustered timestamps, near-ties, non-Euclidean matrices, perturbed symmetry, and invalid tolerances. Record environment versions and logs from independent CI runs. The present 100% branch coverage is strong implementation evidence but should not end the validation programme.

### Priority 3 — Expand noise methodology, not just the test count

Compare raw data and rank-one MDS with multiple defensible baselines. Add independently designed noise models (outliers, heteroscedastic errors, correlated errors, and missing pairs), assess calibration and uncertainty, and report both failures and successes. Predeclare the error metrics and comparison rules. Do not infer a universal denoising theorem from one Gaussian experiment.

### Priority 4 — Complete the prior-art audit

Build a structured bibliography of distance geometry, one-dimensional embedding and reconstruction, multidimensional scaling, metric and pseudometric spaces, relational-clock approaches, quantum switch/indefinite causal order, relativistic proper time, and the problem of time. For each source, record the precise theorem or empirical result and how it overlaps—or does not overlap—with each MFTM claim.

### Priority 5 — Require a concrete physical proposition before extending the model

For any relativistic or quantum extension, specify mathematical objects and observables first. Derive the mapping from MFTM quantities into an established theory. Identify a consequence that is not algebraically equivalent to the baseline model. State the experimental regime, expected magnitude, uncertainty, and possible falsifying observation before evaluating results.

## 13. Ten decision questions (A–J)

| Gate | Question | Current answer |
|---|---|---|
| A | What mathematical object or axiom does MFTM introduce beyond Dᵢⱼ = |tᵢ − tⱼ|? | None beyond the representation has been established in this baseline. |
| B | Which theorem is not already contained in one-dimensional distance geometry or MDS? | None identified yet; H1/H2/H9 are known mathematical results. |
| C | Which information is lost when signed differences are replaced with magnitudes? | The sign of coordinate differences and the global reflection orientation. |
| D | Does selecting an origin called “now” recover a physical universal present? | No such inference follows from the coordinate transformation alone. |
| E | What restores chronology in the implemented model? | An externally supplied directed relation between distinct positions, or other explicit directional structure. |
| F | Does a distance matrix determine a causal partial order? | No; partial-order edges are separate inputs in the current software. |
| G | Is there a complete relativistic mapping? | No; only a standard inertial proper-time example is implemented. |
| H | Is there a derived quantum mechanism or discriminating prediction? | No; H7 remains unresolved. |
| I | Is there an empirically measurable difference from a standard baseline? | No observable or numerical prediction has been specified; H8 remains unresolved. |
| J | What would falsify the physical claim, and what is the preregistered threshold? | Not defined yet; this is a blocking requirement before a physical test. |

## 14. Reproducibility

The following commands were run successfully in the local project directory:

~~~bash
python -m pip install -e . --no-build-isolation
PYTHONPATH=src pytest -q --junitxml=results/junit.xml
python -m compileall -q src tests experiments
coverage erase
coverage run --branch --source=src/mftm -m pytest -q
coverage report -m
coverage json -o results/coverage_branch.json
PYTHONPATH=src python experiments/run_baseline.py
~~~

The environment was Python 3.13.5, NumPy 2.3.5, pytest 9.0.2, and coverage.py 7.13.3. The final test run recorded 515 passing tests. Branch-aware coverage reported 171 of 171 statements and 84 of 84 branches. The experiment used seed 20261009, 50 replicates per level, and eight noise levels. Generated files include experiment_results.json, experiment_results.csv, junit.xml, coverage_branch.json, coverage reports, and console logs.

Reproduction does not depend on a claim of new physics. It should reproduce the reported software and synthetic-data behaviour. A full independent reproduction, mutation-testing report, and completed literature audit remain future work.

## References

1. D. N. Page and W. K. Wootters, “Evolution without evolution: Dynamics described by stationary observables,” *Physical Review D* 27, 2885–2892 (1983). https://doi.org/10.1103/PhysRevD.27.2885  
2. N. L. Diaz, P. Braccia, M. Larocca, J. M. Matera, R. Rossignoli, and M. Cerezo, “Parallel-in-time quantum simulation via Page and Wootters quantum time,” *Physical Review Research* 7, 033294 (2025); arXiv:2308.12944. https://arxiv.org/abs/2308.12944  
3. G. Chiribella, G. M. D’Ariano, P. Perinotti, and B. Valiron, “Quantum computations without definite causal structure,” *Physical Review A* 88, 022318 (2013). https://doi.org/10.1103/PhysRevA.88.022318  
4. G. Rubino et al., “Experimental verification of an indefinite causal order,” *Science Advances* 3, e1602589 (2017). https://doi.org/10.1126/sciadv.1602589  
5. L. Liberti and C. Lavor, “Six mathematical gems from the history of distance geometry,” *International Transactions in Operational Research* 23, 897–920 (2016). https://doi.org/10.1111/itor.12170. This review discusses Schoenberg’s equivalence between Euclidean distance matrices and positive-semidefinite Gram matrices, which underlies classical MDS.  
6. MIT OpenCourseWare, “Coordinates and Proper Time,” 8.224 Exploring Black Holes, General Relativity & Astrophysics (2003). https://ocw.mit.edu/courses/8-224-exploring-black-holes-general-relativity-astrophysics-spring-2003/3982882af388dae3407906357a419cba_coordsproptime.pdf

**Final determination:** MFTM’s representation and test programme are sufficiently specified for the next phase of mathematical and computational investigation. The current evidence supports the expected distance-geometry results and one synthetic denoising observation. It does not yet support a claim that MFTM changes established physics. The decisive next step is to formalize a novel structure or a quantitative, falsifiable prediction and show exactly where it differs from the standard baseline.
