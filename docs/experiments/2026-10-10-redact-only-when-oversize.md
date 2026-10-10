# Planning gate: reduce code only when a bead does not fit (2026-10-10)

Recorded as measured; `references/measured-behaviour.md` (Size) and `references/plan-size-and-shape.md` (Long code) cite these numbers. Live requests against Jev on a real plan; run files and bead texts stayed in the session scratchpad, so this is the analysis only.

---

## Question

Until 0.3.0 the planning gate always sent every fenced code block longer than `--max-code-lines` (8) as its signature lines plus a redaction marker, even when the whole bead fit one request. Does sending the code whole, where the bead fits, change what Jev decides?

## Material and protocol

- A 13-bead plan judged against 6 anchors at the planning gate: 78 cells per arm.
- Arm A, always reduce: the 0.3.0 script, `--max-code-lines 8`.
- Arm B, reduce only when oversize: the same beads, sent whole where the bead fit `--max-item-chars` and `--max-request-bytes` for every anchor (11 of 13 beads), reduced as in arm A otherwise (2 of 13).
- Identical bead text and anchors in both arms; only the code sent differs.

## Results

| Measure | A: always reduce | B: reduce only when oversize |
| --- | ---: | ---: |
| Beads sent whole | 0 of 13 | 11 of 13 |
| `underspecified` cells (of 78) | 15 | 8 |
| Beads passing the gate | 1 of 13 | 6 of 13 |

The largest single movement was the structural-style anchor "every sprint design gives the code for each deliverable". Under A its `addressed` confidence was 0.28 to 0.59 on beads whose code was redacted: Jev saw a marker saying code existed but could not read it. Under B it cleared on 5 beads.

## Interpretation

The earlier finding that code reduction changed no verdict (six pairs of large, full-text beads; `2026-10-10-phase-h-jev-experiments.md`, E1) holds for beads that do not fit anyway. On beads that fit, reduction removes evidence Jev uses: an anchor about code is judged on the code, and a redaction marker is not evidence. Reduction is a size tool, so it is applied only when size requires it.

## Rule adopted

A plan bead that fits one Jev request is sent whole. Otherwise blocks longer than `--max-code-lines` are reduced to signatures one at a time, longest first, until it fits; a bead that does not fit with all of them reduced is `PLAN.TOO_LARGE`. The run records `item.chars_before_reduction` and `item.code_reduced` for what was actually reduced.

## Limits

One plan, one run per arm; run-to-run noise moves about 8 of 50 cells on identical input (measured-behaviour.md), so the cell counts carry that noise. Re-run when the model version changes.
