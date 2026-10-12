# Sprint A0 implementation changes required by calibration

## Testability state machine

1. Run deterministic requirement-form lint before live semantic judgment. A failure is `needs_work`; it is not a Jev vote.
2. Send the same five semantic questions (`single_constraint`, `observable`, `faithful`, `scoped`, `self_contained`) in two byte-identical requests.
3. For each cell, if the first two choices agree and both confidences are at least `0.6`, confirm that choice. Confirmed `yes` is positive; confirmed `no` or `unclear` is negative.
4. If the first two choices agree but either confidence is below `0.6`, classify the cell `inconclusive`; do not average confidences or make a third call.
5. If the first two choices disagree, make exactly one third call for the disputed question. Resolve only when one label has two answers at or above `0.6` and no other label has a confident answer. If distinct labels have confident answers, classify `unstable`. If no label has two confident answers, classify `inconclusive`.
6. Aggregate semantic cells as `unstable` if any cell is unstable, otherwise `inconclusive` if any cell is inconclusive, otherwise `needs_work` if any confirmed cell is `no` or `unclear`, otherwise `testable`.
7. Preserve every request, response, run ID, confidence, disagreement, and resolution. Never average or silently discard a dissenting answer.

Authority ambiguity: Sprint A0 does not explicitly define whether a third answer may override an earlier confident disagreement. The calibrated conservative rule above does not: competing confident labels remain `unstable`. User approval should make that policy authoritative before implementation closes.

## Deterministic requirement-form lint

- Remove `requirement_form` from the Jev question set and `RUBRIC_QUESTIONS`.
- Treat first/second-person speech, wishes/suggestions/hedges, questions, imperatives, and absence of a declarative requirement verb as deterministic requirement-form failures rather than advisory warnings.
- Keep declarative `must`, `shall`, `is`, `are`, `requires`, `uses`, and concrete prohibitions valid.
- Do not count `must never` as two constraints. Remove modal-count bundling from requirement-form lint; the calibrated `single_constraint` semantic question owns atomicity.
- A deterministic form failure should short-circuit to `needs_work` before live calls. Sprint A0 does not explicitly state this precedence, so record it as the second clarity-only authority recommendation.

## Statement-based duplicate detection

- Change deterministic duplicate preselection and `add` similarity checks to compare normalized `statement` tokens with normalized `statement` tokens only.
- Do not compare `quote` tokens in `best_similarity` or use quote overlap to refuse an anchor.
- Send only `a.statement` and `b.statement` to the Jev duplicate question; provenance quotes must not enter the request.
- Use the selected mutual-entailment question. Same quote plus distinct statements is not duplicate; equivalent statements with different quotes are duplicate.

## Sealed rubric shape

The smallest accepted production rubric contains five semantic questions plus deterministic requirement-form lint and one statement-only duplicate question. Production confidence is `0.6`; `0.8` remains diagnostic only. The selected questions and evidence are in `selected-rubric.json` and `acceptance-table.json`.
