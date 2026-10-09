# Theory and Definitions

## 1. Scope

MFTM begins with a representational question: what information is retained when observations are expressed as non-negative pairwise temporal magnitudes rather than signed differences or absolute coordinate labels?

This document does not assume that time is fundamentally a distance matrix. That is a separate ontological claim and is not established by the definitions below.

## 2. Definitions

Let events be indexed by \(i=1,\ldots,n\), with real-valued coordinate labels \(t_i\in\mathbb R\).

**Signed difference**
\[
\Delta_{ij}=t_j-t_i.
\]

**Magnitude-only separation**
\[
D_{ij}=|t_j-t_i|.
\]

The matrix \(D\) is symmetric, has nonnegative entries, and has zero diagonal. It is a one-dimensional Euclidean distance matrix if there exist real coordinates \(x_i\) such that \(D_{ij}=|x_i-x_j|\).

## 3. Proposition: translation and reflection ambiguity

If \(x_i\) realize a given one-dimensional distance matrix, then for any constant \(c\), the coordinates \(x_i+c\) realize the same matrix. Likewise, \(-x_i+c\) realizes the same matrix.

**Consequence:** pairwise magnitudes alone do not identify a unique origin or orientation. If event identities are fixed and the distance data are exact and fully labeled, the reconstruction is unique up to these isometries, subject to the ordinary degenerate cases.

## 4. Ordering is not generally directly observed

Magnitude-only observations do not include the sign of \(t_j-t_i\). For a complete exact line-distance matrix, a global coordinate arrangement may often be reconstructed up to reflection, but a single pairwise magnitude does not tell which event came first. In noisy, incomplete, or non-line-consistent data, reconstruction may be non-unique or fail.

## 5. Classical MDS consistency check

Let \(D^{(2)}\) denote elementwise squared distances, \(I\) the \(n\times n\) identity, and
\[
J=I-\frac1n\mathbf1\mathbf1^T.
\]
Define
\[
B=-\frac12 JD^{(2)}J.
\]

For exact Euclidean distances, \(B\) is a centered Gram matrix and is positive semidefinite. For points on a line, its rank is at most one. Floating-point computations require tolerances. This is a diagnostic, not a standalone proof that the input is a valid temporal dataset.

## 6. Coordinate time versus proper time

A difference between coordinate labels in a chosen frame is not generally equal to elapsed proper time along an arbitrary worldline. Proper time in relativity depends on the spacetime metric and path. Any MFTM comparison with relativity must specify the events, worldline, metric, coordinate system, and observable.

## 7. Claims requiring additional work

The following are not established by the definitions or propositions above:

- that a magnitude-first representation is ontologically more fundamental;
- that a physically privileged present exists or does not exist;
- that the representation yields a new prediction in relativity or quantum theory;
- that aging is explained by pairwise separation alone;
- that a mathematical analogy implies a physical mechanism.

Each would require a precise claim, comparison with existing theory, and a discriminating test.
