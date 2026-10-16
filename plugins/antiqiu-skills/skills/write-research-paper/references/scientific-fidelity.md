# Scientific fidelity checks

Use the relevant checks when detailed methods or quantitative claims make them necessary. They support the scientific argument; they are not a compulsory reporting template or a requirement to expose every input record in the manuscript.

## Quantities and comparisons

Keep the measurement, unit, denominator and comparison object together. Distinguish relative percentages from percentage points, latency reduction from throughput speedup, trainable from total or activated parameters, and measured memory from an unstated peak-memory quantity. Metric columns retain their original meaning; a score is not automatically a success rate or percentage.

A comparison must use matching settings. Preserve variant names, retain/prune budget, resolution, number of tokens, data mixture, ID/OOD split, freeze conditions and evaluation protocol. Do not attach one backbone's accuracy to another backbone's efficiency, or turn a single-dataset efficiency point into an across-benchmark result.

If a source-reported delta conflicts with its cells, verify the operands and comparison definition. A recomputed delta is a derived quantity. Resolve a transcription error when evidence establishes one; otherwise present the disagreement without inventing a reconciliation. Rounded or approximate results stay rounded or approximate.

## Methods and theory

Trace each input through the stated modules and distinguish training, initialization and inference. Keep stage-specific data and losses with their own stages. An evaluation proxy does not become an algorithm parameter or output unless the method defines it that way.

Check equations against the explanation immediately following them. Preserve subtraction versus addition, minimum versus maximum, strict versus non-strict inequalities, normalization and the set over which a mean or sum is taken. Do not supply familiar temperatures, priors, tensor dimensions or normalizers when the evidence omits them.

Keep the applicable regime with every theorem, bound and complexity claim, including in the abstract. A sufficient condition and a counterexample do not establish an if-and-only-if statement. A fitted scaling relation does not imply that every discrete experimental point moves monotonically. A qualitative geometric illustration does not establish a topological theorem.

Only reproduce a supplied proof or a faithful supported sketch. Do not use a remembered theorem or a plausible intermediate identity to complete a gap while presenting it as the study's established result.

## Tables, plots and missing information

Keep raw cells attached to their row and column definitions. Do not broadcast an overall average into unknown splits, copy a default-setting score into a different ablation, infer baseline cells from a delta against an unspecified best comparator, or exchange entries of a reported pair.

Differentiate an omitted cell in the writing packet from a reported incompatibility, failed run or unmeasured condition. Use an omission note or a smaller complete table instead of inventing a common dash with several meanings. Source-supplied comparators that establish the argument must not disappear while the superiority claim remains.

A plot without readable coordinates supports only the qualitative trend actually supplied. Preserve local reversals and exceptions; do not replace them with universal improvement. Captions, axes and referenced figure numbers must match the artifact that is present.

## Citations and voice

Copy verified names and bibliography fields; preserve “et al.” when that is all the record supplies. Do not reconstruct famous author lists or alter a title to improve its style. The scope of a cited protocol or metric stays distinct from the current method's implementation.

Write the scientific story in the appropriate author voice, with source attribution preserved. Keep provenance and unresolved extraction questions in accompanying notes. Never turn “not supplied to the writer” into “not reported by the researchers,” and never assert that a missing detail appears in a supplement unless that location is verified.
