# Live Jev experiments on the sc-lint phase-h plan (2026-10-10)

Recorded as measured; the skill references cite these numbers. 245 requests against jev-1.13.0 with flint's six phase-i anchors and the ten open phase-h sprint beads. Run files and texts stayed in the session scratchpad; this is the analysis.

---

# Live Jev experiments on the plan-anchoring skill (phase-i anchors x phase-h sprint beads)

Date: 2026-10-10. Model answered: `jev-1.13.0` (requested `jev-latest`). Script A = upstream HEAD of
`skills/.claude/skills/plan-anchoring/scripts/jev_judge.py` (plan-anchor `9a765fb`); script B = flint's
variant on sc-lint `origin/feature/plan-anchoring-plan-size` (PR 218). Default plan question set
(`assets/questions/plan.json`, identical in A and B), threshold 0.6, gate `plan`. Every judge call used
`--max-item-chars 200000 --max-request-bytes 200000 --min-item-chars 200000` so nothing was shortened client-side.

Material: the six locked phase-i anchors (`scratchpad/phasei/anchors.json`) and the ten open phase-h sprint
beads (lint-h-1,2,3,4,5,7,11,12,13,14), composed with `compose-item` (`texts/*.full.txt`). Variants built
from the bead JSON in compose-item's layout: `*.descac.txt` (description + acceptance criteria), `*.desc.txt`
(description only), `*.reduced.txt` (script B's `--max-code-lines 8` output, taken from the dry-run request
body). All run files are under `runs/<experiment>/`; one-line-per-cell extracts are `runs/*.rows.jsonl`.
Live Jev requests recorded under runs/: 245; total input tokens 1867730.

A note on the material that matters for every table below: the beads are phase-h sprints that implement
GitHub #193-#204, judged against anchors whose text says "phase-i". A control (E4-B) shows the label does
not move any answer. More important: the beads use the word "layer" almost exclusively in the gh-stack
sense ("Root sprint (planned layer 1)", "the h-7 layer", "every layer above h-14") and in the consumer
sense ("test *layer"); **no bead names an architectural layer (a)-(d)**. That homonym drives most of
ANC-003's results.

---

## E1. Size sensitivity

Compose-item sizes: lint-h-3 full 63,537 chars (desc 5,547 / design 41,374 / AC 16,344); desc+AC 22,013;
desc 5,643; B-reduced 57,279 (7 blocks, 144 code lines dropped). lint-h-11 full 99,385 (design 65,619);
desc+AC 33,616; desc 7,500; B-reduced 70,226 (26 blocks, 681 lines dropped). Script B's dry run reported
these in `item.chars_before_reduction` / `item.code_reduced`; script B refused nothing at
`--max-item-chars 200000` and would have refused both full beads at its 24,000 default (PLAN.TOO_LARGE).

### E1-A. Size grid (script A, default questions). Cell = verdict; rel/add/con = choice/confidence (p_yes)

| bead | variant | item chars | req bytes | input tokens | 422? | anchor | verdict | min_conf | relevant | addressed | contradicted |
|---|---|---:|---:|---:|---|---|---|---:|---|---|---|
| lint-h-3 | (a) full | 63537 | 68401 | 20615 | no | ANC-003 | satisfied | 0.62 | yes/0.79 (p_yes 0.86) | yes/0.77 (p_yes 0.85) | no/0.62 (p_yes 0.24) |
| lint-h-3 | (a) full | 63537 | 68442 | 20631 | no | ANC-005 | underspecified | 0.30 | no/0.30 (p_yes 0.47) | no/0.52 (p_yes 0.30) | yes/0.31 (p_yes 0.54) |
| lint-h-3 | (a) full | 63537 | 68397 | 20614 | no | ANC-006 | underspecified | 0.33 | no/0.33 (p_yes 0.45) | no/0.72 (p_yes 0.18) | yes/0.48 (p_yes 0.65) |
| lint-h-3 | (b) desc+AC | 22013 | 25656 | 7862 | no | ANC-003 | satisfied | 0.69 | yes/0.98 (p_yes 0.99) | yes/0.69 (p_yes 0.79) | no/0.91 (p_yes 0.05) |
| lint-h-3 | (b) desc+AC | 22013 | 25697 | 7878 | no | ANC-005 | underspecified | 0.34 | yes/0.61 (p_yes 0.74) | no/0.34 (p_yes 0.42) | no/0.43 (p_yes 0.35) |
| lint-h-3 | (b) desc+AC | 22013 | 25652 | 7861 | no | ANC-006 | underspecified | 0.40 | no/0.41 (p_yes 0.38) | no/0.89 (p_yes 0.07) | yes/0.40 (p_yes 0.60) |
| lint-h-3 | (c) desc | 5643 | 8703 | 2776 | no | ANC-003 | satisfied | 0.70 | yes/0.98 (p_yes 0.99) | yes/0.70 (p_yes 0.80) | no/0.86 (p_yes 0.08) |
| lint-h-3 | (c) desc | 5643 | 8744 | 2792 | no | ANC-005 | underspecified | 0.34 | yes/0.55 (p_yes 0.70) | no/0.34 (p_yes 0.42) | no/0.38 (p_yes 0.38) |
| lint-h-3 | (c) desc | 5643 | 8699 | 2775 | no | ANC-006 | underspecified | 0.34 | no/0.34 (p_yes 0.43) | no/0.89 (p_yes 0.07) | yes/0.48 (p_yes 0.65) |
| lint-h-3 | (d) code-reduced (B) | 57279 | 61933 | 18885 | no | ANC-003 | satisfied | 0.55 | yes/0.72 (p_yes 0.81) | yes/0.64 (p_yes 0.76) | no/0.55 (p_yes 0.28) |
| lint-h-3 | (d) code-reduced (B) | 57279 | 61974 | 18901 | no | ANC-005 | underspecified | 0.23 | yes/0.25 (p_yes 0.50) | no/0.53 (p_yes 0.29) | yes/0.23 (p_yes 0.49) |
| lint-h-3 | (d) code-reduced (B) | 57279 | 61929 | 18884 | no | ANC-006 | underspecified | 0.46 | no/0.46 (p_yes 0.36) | no/0.73 (p_yes 0.17) | yes/0.51 (p_yes 0.67) |
| lint-h-11 | (a) full | 99385 | 107541 | 31484 | no | ANC-003 | underspecified | 0.34 | yes/0.82 (p_yes 0.88) | no/0.34 (p_yes 0.41) | no/0.72 (p_yes 0.17) |
| lint-h-11 | (a) full | 99385 | 107582 | 31500 | no | ANC-005 | satisfied | 0.76 | yes/0.98 (p_yes 0.99) | yes/0.76 (p_yes 0.84) | no/0.80 (p_yes 0.12) |
| lint-h-11 | (a) full | 99385 | 107537 | 31483 | no | ANC-006 | underspecified | 0.27 | yes/0.86 (p_yes 0.91) | yes/0.27 (p_yes 0.51) | yes/0.30 (p_yes 0.53) |
| lint-h-11 | (b) desc+AC | 33616 | 37800 | 11571 | no | ANC-003 | underspecified | 0.45 | yes/0.85 (p_yes 0.90) | no/0.45 (p_yes 0.32) | no/0.79 (p_yes 0.11) |
| lint-h-11 | (b) desc+AC | 33616 | 37841 | 11587 | no | ANC-005 | satisfied | 0.83 | yes/1.00 (p_yes 1.00) | yes/0.83 (p_yes 0.89) | no/0.89 (p_yes 0.07) |
| lint-h-11 | (b) desc+AC | 33616 | 37796 | 11570 | no | ANC-006 | underspecified | 0.30 | yes/0.64 (p_yes 0.76) | no/0.59 (p_yes 0.26) | yes/0.30 (p_yes 0.53) |
| lint-h-11 | (c) desc | 7500 | 10613 | 3436 | no | ANC-003 | underspecified | 0.23 | yes/0.89 (p_yes 0.93) | no/0.23 (p_yes 0.47) | no/0.82 (p_yes 0.08) |
| lint-h-11 | (c) desc | 7500 | 10654 | 3452 | no | ANC-005 | satisfied | 0.80 | yes/1.00 (p_yes 1.00) | yes/0.80 (p_yes 0.87) | no/0.85 (p_yes 0.09) |
| lint-h-11 | (c) desc | 7500 | 10609 | 3435 | no | ANC-006 | underspecified | 0.40 | yes/0.73 (p_yes 0.82) | no/0.58 (p_yes 0.25) | yes/0.40 (p_yes 0.60) |
| lint-h-11 | (d) code-reduced (B) | 70226 | 75618 | 22941 | no | ANC-003 | underspecified | 0.28 | yes/0.88 (p_yes 0.92) | yes/0.28 (p_yes 0.52) | no/0.73 (p_yes 0.16) |
| lint-h-11 | (d) code-reduced (B) | 70226 | 75659 | 22957 | no | ANC-005 | satisfied | 0.71 | yes/0.95 (p_yes 0.97) | yes/0.74 (p_yes 0.83) | no/0.71 (p_yes 0.17) |
| lint-h-11 | (d) code-reduced (B) | 70226 | 75614 | 22940 | no | ANC-006 | underspecified | 0.30 | yes/0.67 (p_yes 0.78) | no/0.30 (p_yes 0.46) | yes/0.52 (p_yes 0.68) |

### E1-B. Verdict stability across compositions (same bead, same anchor)

| bead | anchor | full | desc+AC | desc | code-reduced | p_yes(addressed) full / desc+AC / desc / reduced |
|---|---|---|---|---|---|---|
| lint-h-3 | ANC-003 | satisfied | satisfied | satisfied | satisfied | 0.85 / 0.79 / 0.80 / 0.76 |
| lint-h-3 | ANC-005 | underspecified | underspecified | underspecified | underspecified | 0.30 / 0.42 / 0.42 / 0.29 |
| lint-h-3 | ANC-006 | underspecified | underspecified | underspecified | underspecified | 0.18 / 0.07 / 0.07 / 0.17 |
| lint-h-11 | ANC-003 | underspecified | underspecified | underspecified | underspecified | 0.41 / 0.32 / 0.47 / 0.52 |
| lint-h-11 | ANC-005 | satisfied | satisfied | satisfied | satisfied | 0.84 / 0.89 / 0.87 / 0.83 |
| lint-h-11 | ANC-006 | underspecified | underspecified | underspecified | underspecified | 0.51 / 0.26 / 0.25 / 0.46 |


**Interpretation (grid).** Jev never returned a context error: the largest request was 107,582 bytes /
31,500 input tokens (lint-h-11 full) and it answered in one attempt, so script A's 24,000-byte default is a
client-side bound, not a Jev limit, and the halve-and-retry path never fired. Verdicts were identical across
all four compositions for all six (bead, anchor) pairs; p(addressed=yes) moved by at most 0.20 between
compositions (h-11/ANC-003: 0.32-0.52), comparable to the run-to-run noise measured in E3-B. So on the default questions,
length neither helps nor hurts the verdict: the signal Jev uses lives in the first few thousand characters
(the Goal paragraph), and the 40-65k-char design fields add tokens without changing the answer. Script B's
code reduction (10-30% smaller) likewise changed nothing, which is consistent with Jev not reading the code
blocks for these questions at all. Input tokens scale linearly at about 0.31 tokens per char.

### Planted contradiction control

Sentence planted: "This sprint also replaces the sc-lint-types crate with a new shared-types crate and
moves attribute handling into the CLI." Baseline p(contradicted) for ANC-001 on unplanted h-3 is 0.29
(full) / 0.19 (desc+AC); for ANC-004 0.29 / 0.12.

### E1-C. Planted contradiction (lint-h-3). p(contradicted=yes) and verdict for ANC-001 and ANC-004

| variant | item chars | plant offset | ANC-001 verdict | ANC-001 contradicted | ANC-001 relevant | ANC-004 verdict | ANC-004 contradicted | ANC-004 relevant |
|---|---:|---|---|---|---|---|---|---|
| full, unplanted (baseline) | 63537 | none | underspecified | no/0.55 (p_yes 0.29) | yes/0.41 (p_yes 0.61) | underspecified | no/0.53 (p_yes 0.29) | yes/0.35 (p_yes 0.57) |
| desc+AC, unplanted (baseline) | 22013 | none | underspecified | no/0.70 (p_yes 0.19) | yes/0.25 (p_yes 0.50) | underspecified | no/0.77 (p_yes 0.12) | yes/0.37 (p_yes 0.58) |
| full, start of description | 63662 | 94 (0%) | not_addressed | yes/0.52 (p_yes 0.68) | yes/0.69 (p_yes 0.79) | underspecified | no/0.55 (p_yes 0.27) | no/0.37 (p_yes 0.42) |
| full, middle of design | 63662 | 27818 (43%) | underspecified | no/0.28 (p_yes 0.46) | no/0.27 (p_yes 0.49) | underspecified | no/0.49 (p_yes 0.32) | no/0.31 (p_yes 0.46) |
| full, end of acceptance | 63662 | 63400 (99%) | underspecified | no/0.37 (p_yes 0.40) | yes/0.35 (p_yes 0.57) | underspecified | no/0.53 (p_yes 0.29) | no/0.31 (p_yes 0.46) |
| desc+AC, start of description | 22137 | 94 (0%) | contradicted | yes/0.69 (p_yes 0.79) | yes/0.67 (p_yes 0.78) | underspecified | no/0.49 (p_yes 0.28) | no/0.28 (p_yes 0.48) |
| desc+AC, middle of acceptance | 22137 | 21254 (96%) | underspecified | no/0.34 (p_yes 0.42) | yes/0.35 (p_yes 0.57) | underspecified | no/0.61 (p_yes 0.22) | yes/0.28 (p_yes 0.52) |
| desc+AC, end of acceptance | 22137 | 22013 (99%) | underspecified | no/0.43 (p_yes 0.36) | yes/0.34 (p_yes 0.56) | underspecified | no/0.70 (p_yes 0.15) | yes/0.41 (p_yes 0.61) |
| desc only, start | 5767 | 94 (2%) | contradicted | yes/0.66 (p_yes 0.77) | yes/0.70 (p_yes 0.80) | underspecified | no/0.51 (p_yes 0.28) | yes/0.28 (p_yes 0.52) |
| desc only, end | 5767 | 5650 (98%) | underspecified | yes/0.33 (p_yes 0.55) | yes/0.55 (p_yes 0.70) | underspecified | no/0.64 (p_yes 0.19) | yes/0.36 (p_yes 0.57) |
| the sentence alone (ceiling) | 218 | sentence only | contradicted | yes/0.94 (p_yes 0.96) | yes/1.00 (p_yes 1.00) | not_addressed | no/0.31 (p_yes 0.23) | yes/0.97 (p_yes 0.98) |

### E1-D. Run-to-run noise on two planted cells (same request sent three times)

| variant | run | ANC-001 verdict | ANC-001 p(contradicted) | ANC-001 min_conf | ANC-004 p(contradicted) |
|---|---|---|---|---|---|
| desc+AC, start of description | 1 | contradicted | 0.79 | 0.67 | 0.28 |
| desc+AC, start of description | 2 | contradicted | 0.76 | 0.64 | 0.31 |
| desc+AC, start of description | 3 | contradicted | 0.79 | 0.61 | 0.26 |
| full, middle of design | 1 | underspecified | 0.46 | 0.27 | 0.32 |
| full, middle of design | 2 | underspecified | 0.45 | 0.30 | 0.36 |
| full, middle of design | 3 | underspecified | 0.42 | 0.28 | 0.37 |


**Interpretation (plant).** Position dominates, not length. At the start of the description the plant is
found at every length: p(contradicted) 0.68 (full, 63k), 0.79 (desc+AC, 22k), 0.77 (desc, 5.7k), 0.96
alone. Buried in the middle of the design (27.8k chars deep) it drops to 0.46 and 0.42-0.45 on repeats;
at the end of the acceptance criteria to 0.40 (full) / 0.36 (desc+AC); even at the end of a 5.7k
description it falls to 0.55. So Jev does not find a contradiction 30k chars deep, and it loses half the
signal within 5k chars of the start. Only the desc+AC-start cell produced the `contradicted` verdict;
full-start reached p=0.68 but confidence 0.52 (<0.6), so `decide()` fell through to `not_addressed`,
a miss at the verdict level. ANC-004 never fired at any position, not even with the sentence alone
(p=0.23): its statement is conditional ("unless Rand approved ... first") and the item says nothing
about approval, so Jev correctly cannot call it a contradiction. A prohibition-with-exception anchor is
not contradictable by a bead that is silent about the exception. Three repeats of two cells (E1-D) vary
by at most 0.05 in p, so the position effect is far outside noise.

**Composition chosen for E2:** full text did not produce a `contradicted` verdict even for a start-of-text
plant, so by the rule given, the smallest variant that kept the plant detectable is used. Both desc+AC and
desc-only detect it at the start (0.79 and 0.77); E2's primary matrix uses desc+AC (keeps the deliverable
list, issue citations and acceptance criteria that ANC-003/005 need), with desc-only as a comparison matrix.
ANC-006 is additionally judged on the full text (E2-D) because its scope is the design field, which both
short variants omit.

---

## E2. Default questions on real anchors (10 beads x 6 anchors)

### E2-A. Verdict matrix, description+acceptance (primary). Cell = verdict (min_conf)

| anchor | h-1 | h-2 | h-3 | h-4 | h-5 | h-7 | h-11 | h-12 | h-13 | h-14 |
|---|---|---|---|---|---|---|---|---|---|---|
| ANC-001 | N/A (0.67) | N/A (0.66) | UNDER (0.25) | UNDER (0.41) | UNDER (0.52) | UNDER (0.58) | UNDER (0.45) | UNDER (0.53) | N/A (0.67) | UNDER (0.46) |
| ANC-002 | UNDER (0.23) | UNDER (0.25) | N/A (0.61) | UNDER (0.43) | UNDER (0.38) | UNDER (0.36) | UNDER (0.27) | UNDER (0.52) | UNDER (0.56) | UNDER (0.23) |
| ANC-003 | UNDER (0.46) | SAT (0.62) | SAT (0.72) | SAT (0.85) | UNDER (0.28) | UNDER (0.56) | UNDER (0.27) | UNDER (0.58) | UNDER (0.58) | UNDER (0.33) |
| ANC-004 | UNDER (0.48) | UNDER (0.45) | UNDER (0.48) | UNDER (0.41) | UNDER (0.30) | UNDER (0.46) | NOT_ADDR (0.76) | UNDER (0.33) | UNDER (0.31) | UNDER (0.30) |
| ANC-005 | SAT (0.62) | SAT (0.85) | UNDER (0.25) | UNDER (0.48) | UNDER (0.59) | UNDER (0.53) | SAT (0.83) | UNDER (0.41) | UNDER (0.55) | UNDER (0.33) |
| ANC-006 | UNDER (0.31) | UNDER (0.38) | UNDER (0.35) | UNDER (0.27) | NOT_ADDR (0.27) | UNDER (0.27) | UNDER (0.28) | UNDER (0.23) | UNDER (0.30) | N/A (0.36) |

Coverage (`coverage --format md`, primary): uncovered anchors ANC-001, ANC-002, ANC-004, ANC-006; covered
ANC-003 (h-2, h-3, h-4) and ANC-005 (h-1, h-2, h-11). File: `runs/e2-descac.coverage.md`.

### E2-B. Verdict matrix, description only (comparison)

| anchor | h-1 | h-2 | h-3 | h-4 | h-5 | h-7 | h-11 | h-12 | h-13 | h-14 |
|---|---|---|---|---|---|---|---|---|---|---|
| ANC-001 | UNDER (0.58) | N/A (0.69) | UNDER (0.27) | UNDER (0.43) | UNDER (0.45) | UNDER (0.56) | UNDER (0.49) | UNDER (0.38) | N/A (0.69) | UNDER (0.37) |
| ANC-002 | UNDER (0.45) | N/A (0.72) | N/A (0.89) | N/A (0.79) | UNDER (0.59) | N/A (0.70) | UNDER (0.35) | UNDER (0.49) | UNDER (0.45) | N/A (0.82) |
| ANC-003 | UNDER (0.46) | UNDER (0.59) | SAT (0.69) | SAT (0.79) | UNDER (0.49) | UNDER (0.49) | UNDER (0.23) | NOT_ADDR (0.70) | UNDER (0.49) | UNDER (0.27) |
| ANC-004 | UNDER (0.34) | UNDER (0.30) | UNDER (0.48) | UNDER (0.49) | UNDER (0.37) | UNDER (0.46) | NOT_ADDR (0.64) | UNDER (0.30) | UNDER (0.34) | UNDER (0.43) |
| ANC-005 | UNDER (0.53) | SAT (0.69) | UNDER (0.33) | UNDER (0.49) | UNDER (0.58) | UNDER (0.59) | SAT (0.83) | SAT (0.67) | UNDER (0.58) | UNDER (0.37) |
| ANC-006 | UNDER (0.28) | UNDER (0.35) | UNDER (0.38) | UNDER (0.41) | UNDER (0.33) | UNDER (0.28) | UNDER (0.38) | UNDER (0.27) | UNDER (0.27) | N/A (0.53) |

Desc-only coverage (`runs/e2-desc.coverage.md`): same uncovered set; ANC-003 covered by h-3, h-4;
ANC-005 by h-2, h-11, h-12. Ten cells differ between the two compositions, all of them
underspecified <-> decided swaps at confidences within 0.1 of the threshold (desc-only also gave ANC-002 a false N/A on h-2, the kit-justfile bead).

### E2-C. Per-question detail, description+acceptance (primary)

| anchor | bead | chars | verdict | min_conf | relevant | addressed | contradicted |
|---|---|---:|---|---:|---|---|---|
| ANC-001 | lint-h-1 | 13920 | not_applicable | 0.67 | no/0.67 (p_yes 0.22) | no/0.95 (p_yes 0.02) | no/0.97 (p_yes 0.02) |
| ANC-001 | lint-h-2 | 15232 | not_applicable | 0.66 | no/0.66 (p_yes 0.23) | no/0.97 (p_yes 0.01) | no/0.97 (p_yes 0.02) |
| ANC-001 | lint-h-3 | 22013 | underspecified | 0.25 | no/0.25 (p_yes 0.49) | no/0.86 (p_yes 0.06) | no/0.70 (p_yes 0.19) |
| ANC-001 | lint-h-4 | 13532 | underspecified | 0.41 | yes/0.41 (p_yes 0.61) | no/0.94 (p_yes 0.02) | no/0.98 (p_yes 0.01) |
| ANC-001 | lint-h-5 | 21914 | underspecified | 0.52 | no/0.52 (p_yes 0.32) | no/0.95 (p_yes 0.01) | no/0.74 (p_yes 0.16) |
| ANC-001 | lint-h-7 | 18475 | underspecified | 0.58 | yes/0.58 (p_yes 0.72) | no/0.89 (p_yes 0.05) | no/0.94 (p_yes 0.04) |
| ANC-001 | lint-h-11 | 33616 | underspecified | 0.45 | yes/0.45 (p_yes 0.63) | no/0.86 (p_yes 0.07) | no/0.92 (p_yes 0.04) |
| ANC-001 | lint-h-12 | 21882 | underspecified | 0.53 | no/0.53 (p_yes 0.31) | no/0.97 (p_yes 0.01) | no/0.79 (p_yes 0.13) |
| ANC-001 | lint-h-13 | 13571 | not_applicable | 0.67 | no/0.67 (p_yes 0.22) | no/1.00 (p_yes 0.00) | no/0.97 (p_yes 0.02) |
| ANC-001 | lint-h-14 | 9631 | underspecified | 0.46 | yes/0.46 (p_yes 0.64) | no/0.91 (p_yes 0.04) | no/0.97 (p_yes 0.02) |
| ANC-002 | lint-h-1 | 13920 | underspecified | 0.23 | yes/0.86 (p_yes 0.91) | no/0.23 (p_yes 0.39) | no/0.82 (p_yes 0.12) |
| ANC-002 | lint-h-2 | 15232 | underspecified | 0.25 | yes/0.56 (p_yes 0.71) | no/0.25 (p_yes 0.42) | no/0.76 (p_yes 0.15) |
| ANC-002 | lint-h-3 | 22013 | not_applicable | 0.61 | no/0.70 (p_yes 0.20) | no/0.61 (p_yes 0.21) | no/0.89 (p_yes 0.07) |
| ANC-002 | lint-h-4 | 13532 | underspecified | 0.43 | no/0.56 (p_yes 0.29) | no/0.43 (p_yes 0.30) | no/0.89 (p_yes 0.07) |
| ANC-002 | lint-h-5 | 21914 | underspecified | 0.38 | yes/0.85 (p_yes 0.90) | no/0.38 (p_yes 0.33) | no/0.70 (p_yes 0.19) |
| ANC-002 | lint-h-7 | 18475 | underspecified | 0.36 | yes/0.36 (p_yes 0.57) | no/0.41 (p_yes 0.33) | no/0.86 (p_yes 0.09) |
| ANC-002 | lint-h-11 | 33616 | underspecified | 0.27 | yes/0.98 (p_yes 0.99) | yes/0.27 (p_yes 0.51) | no/0.80 (p_yes 0.13) |
| ANC-002 | lint-h-12 | 21882 | underspecified | 0.52 | yes/0.70 (p_yes 0.80) | no/0.52 (p_yes 0.25) | no/0.82 (p_yes 0.12) |
| ANC-002 | lint-h-13 | 13571 | underspecified | 0.56 | yes/0.56 (p_yes 0.71) | no/0.69 (p_yes 0.17) | no/0.86 (p_yes 0.09) |
| ANC-002 | lint-h-14 | 9631 | underspecified | 0.23 | no/0.28 (p_yes 0.48) | no/0.23 (p_yes 0.37) | no/0.88 (p_yes 0.08) |
| ANC-003 | lint-h-1 | 13920 | underspecified | 0.46 | yes/0.76 (p_yes 0.84) | yes/0.46 (p_yes 0.64) | no/0.89 (p_yes 0.06) |
| ANC-003 | lint-h-2 | 15232 | satisfied | 0.62 | yes/0.86 (p_yes 0.91) | yes/0.62 (p_yes 0.75) | no/0.89 (p_yes 0.05) |
| ANC-003 | lint-h-3 | 22013 | satisfied | 0.72 | yes/0.98 (p_yes 0.99) | yes/0.72 (p_yes 0.81) | no/0.91 (p_yes 0.05) |
| ANC-003 | lint-h-4 | 13532 | satisfied | 0.85 | yes/0.97 (p_yes 0.98) | yes/0.85 (p_yes 0.90) | no/0.91 (p_yes 0.05) |
| ANC-003 | lint-h-5 | 21914 | underspecified | 0.28 | yes/0.79 (p_yes 0.86) | no/0.28 (p_yes 0.44) | no/0.89 (p_yes 0.05) |
| ANC-003 | lint-h-7 | 18475 | underspecified | 0.56 | yes/0.97 (p_yes 0.98) | yes/0.56 (p_yes 0.71) | no/0.88 (p_yes 0.07) |
| ANC-003 | lint-h-11 | 33616 | underspecified | 0.27 | yes/0.92 (p_yes 0.95) | yes/0.27 (p_yes 0.51) | no/0.83 (p_yes 0.08) |
| ANC-003 | lint-h-12 | 21882 | underspecified | 0.58 | yes/0.58 (p_yes 0.72) | no/0.72 (p_yes 0.15) | no/0.91 (p_yes 0.04) |
| ANC-003 | lint-h-13 | 13571 | underspecified | 0.58 | yes/0.72 (p_yes 0.81) | no/0.58 (p_yes 0.25) | no/0.94 (p_yes 0.03) |
| ANC-003 | lint-h-14 | 9631 | underspecified | 0.33 | yes/0.97 (p_yes 0.98) | yes/0.33 (p_yes 0.55) | no/0.89 (p_yes 0.06) |
| ANC-004 | lint-h-1 | 13920 | underspecified | 0.48 | yes/0.48 (p_yes 0.65) | no/0.56 (p_yes 0.24) | no/0.92 (p_yes 0.04) |
| ANC-004 | lint-h-2 | 15232 | underspecified | 0.45 | yes/0.45 (p_yes 0.63) | no/0.69 (p_yes 0.16) | no/0.85 (p_yes 0.07) |
| ANC-004 | lint-h-3 | 22013 | underspecified | 0.48 | yes/0.48 (p_yes 0.65) | no/0.86 (p_yes 0.07) | no/0.70 (p_yes 0.18) |
| ANC-004 | lint-h-4 | 13532 | underspecified | 0.41 | yes/0.41 (p_yes 0.61) | no/0.66 (p_yes 0.15) | no/0.72 (p_yes 0.15) |
| ANC-004 | lint-h-5 | 21914 | underspecified | 0.30 | no/0.30 (p_yes 0.47) | no/0.85 (p_yes 0.07) | no/0.80 (p_yes 0.11) |
| ANC-004 | lint-h-7 | 18475 | underspecified | 0.46 | yes/0.46 (p_yes 0.64) | no/0.85 (p_yes 0.07) | no/0.89 (p_yes 0.06) |
| ANC-004 | lint-h-11 | 33616 | not_addressed | 0.76 | yes/0.76 (p_yes 0.84) | no/0.97 (p_yes 0.01) | no/0.92 (p_yes 0.03) |
| ANC-004 | lint-h-12 | 21882 | underspecified | 0.33 | yes/0.33 (p_yes 0.55) | no/0.88 (p_yes 0.05) | no/0.83 (p_yes 0.09) |
| ANC-004 | lint-h-13 | 13571 | underspecified | 0.31 | yes/0.31 (p_yes 0.54) | no/0.92 (p_yes 0.03) | no/0.85 (p_yes 0.09) |
| ANC-004 | lint-h-14 | 9631 | underspecified | 0.30 | no/0.30 (p_yes 0.47) | no/0.91 (p_yes 0.04) | no/0.80 (p_yes 0.11) |
| ANC-005 | lint-h-1 | 13920 | satisfied | 0.62 | yes/0.73 (p_yes 0.82) | yes/0.62 (p_yes 0.75) | no/0.89 (p_yes 0.06) |
| ANC-005 | lint-h-2 | 15232 | satisfied | 0.85 | yes/0.88 (p_yes 0.92) | yes/0.85 (p_yes 0.90) | no/0.95 (p_yes 0.03) |
| ANC-005 | lint-h-3 | 22013 | underspecified | 0.25 | yes/0.74 (p_yes 0.83) | no/0.25 (p_yes 0.47) | no/0.51 (p_yes 0.30) |
| ANC-005 | lint-h-4 | 13532 | underspecified | 0.48 | yes/0.91 (p_yes 0.94) | yes/0.48 (p_yes 0.65) | no/0.73 (p_yes 0.17) |
| ANC-005 | lint-h-5 | 21914 | underspecified | 0.59 | yes/1.00 (p_yes 1.00) | yes/0.59 (p_yes 0.73) | no/0.72 (p_yes 0.18) |
| ANC-005 | lint-h-7 | 18475 | underspecified | 0.53 | yes/0.94 (p_yes 0.96) | yes/0.53 (p_yes 0.69) | no/0.91 (p_yes 0.05) |
| ANC-005 | lint-h-11 | 33616 | satisfied | 0.83 | yes/1.00 (p_yes 1.00) | yes/0.83 (p_yes 0.89) | no/0.88 (p_yes 0.08) |
| ANC-005 | lint-h-12 | 21882 | underspecified | 0.41 | yes/1.00 (p_yes 1.00) | yes/0.41 (p_yes 0.61) | no/0.89 (p_yes 0.07) |
| ANC-005 | lint-h-13 | 13571 | underspecified | 0.55 | yes/0.98 (p_yes 0.99) | yes/0.55 (p_yes 0.70) | no/0.95 (p_yes 0.03) |
| ANC-005 | lint-h-14 | 9631 | underspecified | 0.33 | yes/0.71 (p_yes 0.81) | yes/0.33 (p_yes 0.55) | no/0.83 (p_yes 0.10) |
| ANC-006 | lint-h-1 | 13920 | underspecified | 0.31 | no/0.37 (p_yes 0.42) | no/0.88 (p_yes 0.08) | yes/0.31 (p_yes 0.54) |
| ANC-006 | lint-h-2 | 15232 | underspecified | 0.38 | yes/0.83 (p_yes 0.89) | no/0.53 (p_yes 0.29) | no/0.38 (p_yes 0.40) |
| ANC-006 | lint-h-3 | 22013 | underspecified | 0.35 | no/0.35 (p_yes 0.42) | no/0.91 (p_yes 0.06) | yes/0.41 (p_yes 0.61) |
| ANC-006 | lint-h-4 | 13532 | underspecified | 0.27 | yes/0.27 (p_yes 0.51) | no/0.73 (p_yes 0.16) | yes/0.48 (p_yes 0.65) |
| ANC-006 | lint-h-5 | 21914 | not_addressed | 0.27 | yes/0.61 (p_yes 0.74) | no/0.76 (p_yes 0.14) | no/0.27 (p_yes 0.48) |
| ANC-006 | lint-h-7 | 18475 | underspecified | 0.27 | yes/0.51 (p_yes 0.67) | no/0.70 (p_yes 0.19) | yes/0.27 (p_yes 0.51) |
| ANC-006 | lint-h-11 | 33616 | underspecified | 0.28 | yes/0.72 (p_yes 0.81) | no/0.59 (p_yes 0.26) | yes/0.28 (p_yes 0.52) |
| ANC-006 | lint-h-12 | 21882 | underspecified | 0.23 | yes/0.46 (p_yes 0.64) | no/0.74 (p_yes 0.16) | no/0.23 (p_yes 0.49) |
| ANC-006 | lint-h-13 | 13571 | underspecified | 0.30 | no/0.43 (p_yes 0.38) | no/0.88 (p_yes 0.08) | no/0.30 (p_yes 0.46) |
| ANC-006 | lint-h-14 | 9631 | not_applicable | 0.36 | no/0.89 (p_yes 0.07) | no/0.98 (p_yes 0.01) | no/0.36 (p_yes 0.43) |

### E2-D. ANC-006 judged on the FULL composed text (design field included)

| bead | chars | fenced blocks in design | verdict | min_conf | relevant | addressed | contradicted | input tokens |
|---|---:|---:|---|---:|---|---|---|---:|
| lint-h-1 | 32329 | 6 | underspecified | 0.31 | yes/0.31 (p_yes 0.54) | no/0.85 (p_yes 0.10) | yes/0.46 (p_yes 0.64) | 11033 |
| lint-h-2 | 88495 | 13 | underspecified | 0.46 | yes/0.53 (p_yes 0.69) | no/0.66 (p_yes 0.22) | yes/0.46 (p_yes 0.64) | 25951 |
| lint-h-3 | 63537 | 9 | underspecified | 0.53 | no/0.53 (p_yes 0.31) | no/0.77 (p_yes 0.14) | yes/0.53 (p_yes 0.69) | 20614 |
| lint-h-4 | 37877 | 16 | underspecified | 0.45 | yes/0.53 (p_yes 0.69) | no/0.66 (p_yes 0.22) | yes/0.45 (p_yes 0.63) | 12137 |
| lint-h-5 | 65467 | 12 | not_addressed | 0.48 | yes/0.64 (p_yes 0.76) | no/0.67 (p_yes 0.21) | yes/0.48 (p_yes 0.65) | 20872 |
| lint-h-7 | 44599 | 12 | underspecified | 0.38 | yes/0.51 (p_yes 0.67) | no/0.61 (p_yes 0.25) | yes/0.38 (p_yes 0.59) | 15416 |
| lint-h-11 | 99385 | 33 | underspecified | 0.28 | yes/0.83 (p_yes 0.89) | yes/0.28 (p_yes 0.52) | yes/0.51 (p_yes 0.67) | 31483 |
| lint-h-12 | 56691 | 13 | underspecified | 0.28 | yes/0.67 (p_yes 0.78) | no/0.43 (p_yes 0.37) | yes/0.28 (p_yes 0.52) | 18508 |
| lint-h-13 | 33154 | 7 | underspecified | 0.25 | yes/0.46 (p_yes 0.64) | no/0.70 (p_yes 0.19) | yes/0.25 (p_yes 0.50) | 10835 |
| lint-h-14 | 28534 | 14 | not_applicable | 0.25 | no/0.92 (p_yes 0.05) | no/0.97 (p_yes 0.02) | yes/0.25 (p_yes 0.50) | 9449 |

### E2-E. Offline threshold sensitivity (recomputed from the recorded answers, primary matrix)

| threshold | satisfied | not_addressed | contradicted | not_applicable | underspecified | decided cells |
|---|---:|---:|---:|---:|---:|---:|
| 0.4 | 13 | 19 | 2 | 9 | 17 | 43/60 |
| 0.5 | 10 | 10 | 0 | 8 | 32 | 28/60 |
| 0.6 | 6 | 2 | 0 | 5 | 47 | 13/60 |
| 0.7 | 4 | 1 | 0 | 2 | 53 | 7/60 |


### Per-cell human reading (primary matrix; ANC-006 read on the full text, table E2-D)

Ground truth was read from the bead JSON (`phaseh/beads/*.json`); evidence lines are quoted in
`runs/` extracts and were produced by grepping each bead for the anchor's subject.
Legend: **FP** = gate passes the bead but it should not (includes a false `not_applicable`);
**FN** = gate fails or would fail a compliant bead; **UND** = Jev's verdict is `underspecified`
(gate still fails), with the direction Jev leaned noted.

**ANC-001 (four layers).** Scope names CLI commands, crate dependencies and the kit template, so every
bead is in scope; no bead states the layering, so the literal correct verdict is `not_addressed`
(or `satisfied` only by implication for h-3/h-7, which place a contract in `sc-lint-schema` and have
backends/CLI call down).
- h-1 N/A: wrong. h-1 changes `sc-lint lint` exit codes (layer c). **FP (false N/A)**.
- h-2 N/A: wrong. h-2 is the kit `.sc-lint/justfile` (layer d). **FP (false N/A)**.
- h-3 UND, relevant=no 0.25: wrong direction; h-3 is the most layer-shaped bead (contract in sc-lint-schema, adopted by portability/runtime). **UND**.
- h-4 UND, relevant=yes 0.41: right direction, under-confident. **UND**.
- h-5 UND, relevant=no 0.52: wrong direction (CLI step model is layer c). **UND**.
- h-7 UND, relevant=yes 0.58: right direction, 0.02 short. **UND**.
- h-11 UND, relevant=yes 0.45: right direction. **UND**.
- h-12 UND, relevant=no 0.53: wrong direction (`sc-lint provision` is layer c). **UND**.
- h-13 N/A: wrong; parallel consumer steps live in the CLI. **FP (false N/A)**.
- h-14 UND, relevant=yes 0.46: right direction. **UND**.

**ANC-002 (repo owns `just test`).** Scope: kit template, any CLI test command, helpers for consumer test
recipes. In scope: h-2 (kit justfile), h-5 (`sc-lint test`, selectors), h-11 (kit + bootstrap test
forwarding), h-12/h-13 partly. Out of scope: h-1, h-3, h-4, h-7, h-14 (they only run `just test` as a CI check).
- h-1 UND, relevant=yes 0.86: wrong direction; lint exit code is not test. **UND** (true: N/A).
- h-2 UND, relevant 0.56, addressed=no 0.25: h-2's justfile renders consumer-owned test commands verbatim, which is this anchor's content; addressed should lean yes. **UND** (FN-leaning).
- h-3 N/A: **correct**.
- h-4 UND, relevant=no 0.56: right direction. **UND**.
- h-5 UND, relevant 0.85, addressed=no 0.38, contradicted=no 0.70: h-5 adds selector groups, `default`, `keep_going`, `test --list` to crates/sc-lint, i.e. consumer test orchestration inside sc-lint, which the anchor's deterministic check forbids. A human would at least raise `contradicted`; Jev gave 0.19. **UND**, likely missed contradiction.
- h-7 UND, relevant=yes 0.36: wrong direction. **UND**.
- h-11 UND, relevant 0.98, addressed p=0.51: relevance right, addressed on the fence. **UND**.
- h-12 UND, relevant 0.70, addressed=no 0.52: `requires`/python runner are test-adjacent; defensible. **UND**.
- h-13 UND, relevant 0.56: parallel steps include test steps; same orchestration concern as h-5. **UND**.
- h-14 UND, relevant=no 0.28: right direction. **UND**.

**ANC-003 (lowest layer; bead names it).** No bead names an (a)-(d) layer; "layer 1" is a stack position.
Correct verdict for all ten: `not_addressed`.
- h-2 SAT (addressed 0.62): "Root sprint (planned layer 1, branch ...)" is gh-stack vocabulary. **FP**.
- h-3 SAT (0.72): names `sc-lint-schema` and the backends but never calls them a layer. **FP**.
- h-4 SAT (0.85): "Root sprint (layer 1)". **FP**.
- h-1 UND addressed=yes 0.46, h-7 yes 0.56, h-11 yes 0.27, h-14 yes 0.33: all FP-leaning. **UND x4**.
- h-5 addressed=no 0.28, h-12 no 0.72 (relevant 0.58 blocked it), h-13 no 0.58: right direction. **UND x3**. (Desc-only gave h-12 `not_addressed`, the correct verdict.)

**ANC-004 (no redesign without Rand's prior approval).** Scope: all plan-bead changes, so all ten are in
scope. Every bead states it "implements against the already-committed texts" and h-1/h-2/h-3 add "The
sprint never amends a requirement, ADR or contract doc": the directive is preserved explicitly, so a human
reads `satisfied`.
- h-11 NOT_ADDR (addressed=no 0.97): h-11 does not restate the no-amendment constraint, so by the letter of the question "silent" is right, but the gate blocks a compliant bead. **FN**.
- h-1, h-2, h-3, h-4, h-7, h-12, h-13, h-14 UND, addressed=no 0.56-0.92: Jev does not read "never amends a requirement, ADR or contract doc" as the directive's content. **UND x8**, all FN-leaning.
- h-5 UND relevant=no 0.30: wrong direction. **UND**.
A prohibition cannot be "present as a step"; the default `addressed` question asks for presence of content, so a compliant bead can only reach `satisfied` by restating the prohibition.

**ANC-005 (targeted addition for a named issue).** Every bead cites its issue numbers in sentence one.
- h-1 SAT (#200), h-2 SAT (#193, #194), h-11 SAT (#193-#204): **correct x3**.
- h-3 UND, addressed=no 0.25 (p 0.47): cites #201 and #202 in the first sentence; the "(reduced: ...)" parenthetical and the REQ/ADR cross-references seem to dilute it. **UND**, FN-leaning.
- h-4 UND, addressed=yes 0.48, contradicted p=0.17: cites #203 but "Also closes PLAN-SCOPE-R2-M1 (neutral fixture vocabulary ...)", an addition those issues do not require; a human would raise `contradicted`. **UND**, missed contradiction.
- h-5 (0.59), h-7 (0.53), h-13 (0.55), h-14 (0.33) UND addressed=yes: right direction, under-confident. **UND x4**.
- h-12 UND addressed=yes 0.41: cites #196-#198 but also "fixes the bootstrap's existing exit-2 defect". **UND**, borderline like h-4.

**ANC-006 (design gives code for each deliverable), read on the full text (E2-D).** Designs carry 6-33
fenced blocks against 3-8 numbered deliverables; a human reads `satisfied` for all ten.
- h-5 NOT_ADDR (addressed=no 0.67, 12 blocks): **FN**.
- h-14 N/A (relevant=no 0.92, 14 blocks): the scope is "every sprint bead's design field". **FP (false N/A)**.
- h-1, h-2, h-3, h-4, h-7, h-11, h-12, h-13 UND with addressed=no 0.43-0.85 and contradicted leaning yes 0.50-0.69: **UND x8**, all FN-leaning, with a spurious contradiction signal. In the desc+AC matrix the design was absent, so those ten cells are undecidable by construction; notably Jev still leaned `contradicted` (p 0.40-0.65) rather than `unclear`.

**Counts (60 cells).** Correct 4 (ANC-002 h-3; ANC-005 h-1, h-2, h-11). False pass 7 (ANC-001 h-1/h-2/h-13
false N/A; ANC-003 h-2/h-3/h-4 satisfied; ANC-006 h-14 false N/A). False negative 2 (ANC-004 h-11;
ANC-006 h-5). Undecidable 47, of which 27 lean the wrong way at threshold 0, 15 lean the right way, 5 I could not call, and 2 (ANC-002 h-5, ANC-005 h-4) hide a
contradiction a reader would raise. The limiting question in the 47 underspecified cells: `relevant` in 23,
`addressed` in 19, both in 5; `contradicted` never limited a verdict.

**Verbatim speech vs requirement form.** Mean relevance confidence: ANC-001 (verbatim list with "w/",
"i.e.") 0.52, ANC-002 (verbatim "I expect ...") 0.64, versus ANC-003 0.85, ANC-004 0.43, ANC-005 0.89,
ANC-006 0.54. Form is not the main determinant. The two anchors Jev handles best (ANC-003, ANC-005) are
positive requirements with concrete matchable tokens ("names that layer", "#193-#204"); the two it handles
worst are a requirement written as a conditional prohibition (ANC-004) and a requirement about the shape of
the bead rather than its content (ANC-006). The verbatim anchors sit in between: ANC-001's shorthand costs
it relevance (three false N/A, six relevant=no leanings on in-scope beads), ANC-002's first-person
phrasing did not hurt relevance but its vague object ("patterns and general helper functions") left
`addressed` at 0.23-0.69 on every in-scope bead. The threshold table (E2-E) shows how little the default
questions decide at 0.6: 13 of 60 cells; even at 0.5 only 28.

---

## E3. One tuning round: ANC-003 `addressed`

ANC-003 had the worst E2 result in the dangerous direction (three confident false passes, four more leaning
that way) and `addressed` was its weakest question. Override (`overrides-anc003.json`, same id, same
yes/no/unclear): the instructions list the four layers with their crate names, say that "layer" in the
beads usually means a stacked-PR position or a consumer test layer and that those do not count, and that a
crate or path counts only if the text also identifies it as the layer; criteria carry the vocabulary
variants ("shared types layer", "analyzer crate layer", "CLI layer", "kit layer", "lowest layer able to
carry"). Re-judged all ten beads, all six anchors, desc+AC, with `--overrides-file`.

### E3-A. ANC-003 before/after the `addressed` override (description+acceptance)

| bead | verdict before | verdict after | addressed before | addressed after | relevant before | relevant after | min_conf before | min_conf after |
|---|---|---|---|---|---|---|---:|---:|
| lint-h-1 | underspecified | not_addressed | yes/0.46 (p_yes 0.64) | no/0.98 (p_yes 0.01) | yes/0.76 (p_yes 0.84) | yes/0.91 (p_yes 0.94) | 0.46 | 0.89 |
| lint-h-2 | satisfied | not_addressed | yes/0.62 (p_yes 0.75) | no/0.97 (p_yes 0.02) | yes/0.86 (p_yes 0.91) | yes/0.98 (p_yes 0.99) | 0.62 | 0.92 |
| lint-h-3 | satisfied | not_addressed | yes/0.72 (p_yes 0.81) | no/0.97 (p_yes 0.02) | yes/0.98 (p_yes 0.99) | yes/0.98 (p_yes 0.99) | 0.72 | 0.92 |
| lint-h-4 | satisfied | not_addressed | yes/0.85 (p_yes 0.90) | no/0.98 (p_yes 0.01) | yes/0.97 (p_yes 0.98) | yes/0.97 (p_yes 0.98) | 0.85 | 0.92 |
| lint-h-5 | underspecified | underspecified | no/0.28 (p_yes 0.44) | no/1.00 (p_yes 0.00) | yes/0.79 (p_yes 0.86) | yes/0.48 (p_yes 0.65) | 0.28 | 0.48 |
| lint-h-7 | underspecified | not_addressed | yes/0.56 (p_yes 0.71) | no/1.00 (p_yes 0.00) | yes/0.97 (p_yes 0.98) | yes/0.97 (p_yes 0.98) | 0.56 | 0.91 |
| lint-h-11 | underspecified | not_addressed | yes/0.27 (p_yes 0.51) | no/0.97 (p_yes 0.02) | yes/0.92 (p_yes 0.95) | yes/0.94 (p_yes 0.96) | 0.27 | 0.79 |
| lint-h-12 | underspecified | underspecified | no/0.72 (p_yes 0.15) | no/0.98 (p_yes 0.01) | yes/0.58 (p_yes 0.72) | yes/0.56 (p_yes 0.71) | 0.58 | 0.56 |
| lint-h-13 | underspecified | not_addressed | no/0.58 (p_yes 0.25) | no/1.00 (p_yes 0.00) | yes/0.72 (p_yes 0.81) | yes/0.73 (p_yes 0.82) | 0.58 | 0.73 |
| lint-h-14 | underspecified | not_addressed | yes/0.33 (p_yes 0.55) | no/0.97 (p_yes 0.02) | yes/0.97 (p_yes 0.98) | yes/0.97 (p_yes 0.98) | 0.33 | 0.92 |

### E3-B. Untouched anchors in the same re-judge (pure run-to-run noise, 50 cells)

| anchor | bead | before | after | d conf relevant | d conf addressed | d conf contradicted |
|---|---|---|---|---:|---:|---:|
| ANC-001 | lint-h-1 | not_applicable | not_applicable | +0.12 | +0.02 | +0.00 |
| ANC-001 | lint-h-2 | not_applicable | underspecified **FLIP** | -0.07 | +0.00 | +0.00 |
| ANC-001 | lint-h-3 | underspecified | underspecified | +0.12 | +0.03 | +0.00 |
| ANC-001 | lint-h-4 | underspecified | underspecified | -0.03 | -0.02 | +0.00 |
| ANC-001 | lint-h-5 | underspecified | underspecified | -0.03 | +0.02 | +0.05 |
| ANC-001 | lint-h-7 | underspecified | underspecified | -0.07 | -0.01 | +0.01 |
| ANC-001 | lint-h-11 | underspecified | underspecified | +0.09 | -0.03 | -0.04 |
| ANC-001 | lint-h-12 | underspecified | underspecified | +0.02 | +0.00 | +0.12 |
| ANC-001 | lint-h-13 | not_applicable | not_applicable | +0.10 | +0.00 | +0.00 |
| ANC-001 | lint-h-14 | underspecified | underspecified | -0.08 | +0.01 | +0.00 |
| ANC-002 | lint-h-1 | underspecified | underspecified | +0.00 | -0.05 | -0.08 |
| ANC-002 | lint-h-2 | underspecified | underspecified | -0.07 | +0.13 | -0.03 |
| ANC-002 | lint-h-3 | not_applicable | underspecified **FLIP** | -0.15 | +0.00 | -0.07 |
| ANC-002 | lint-h-4 | underspecified | underspecified | -0.08 | +0.03 | +0.00 |
| ANC-002 | lint-h-5 | underspecified | underspecified | -0.06 | +0.00 | +0.00 |
| ANC-002 | lint-h-7 | underspecified | underspecified | -0.03 | -0.04 | +0.00 |
| ANC-002 | lint-h-11 | underspecified | underspecified | +0.00 | +0.14 | -0.03 |
| ANC-002 | lint-h-12 | underspecified | underspecified | -0.06 | +0.07 | -0.03 |
| ANC-002 | lint-h-13 | underspecified | underspecified | -0.03 | -0.02 | +0.00 |
| ANC-002 | lint-h-14 | underspecified | underspecified | +0.05 | -0.05 | +0.04 |
| ANC-004 | lint-h-1 | underspecified | underspecified | -0.15 | -0.04 | -0.01 |
| ANC-004 | lint-h-2 | underspecified | underspecified | -0.07 | +0.07 | +0.04 |
| ANC-004 | lint-h-3 | underspecified | not_addressed **FLIP** | +0.16 | -0.03 | -0.06 |
| ANC-004 | lint-h-4 | underspecified | underspecified | +0.07 | +0.06 | +0.02 |
| ANC-004 | lint-h-5 | underspecified | underspecified | -0.05 | +0.03 | -0.04 |
| ANC-004 | lint-h-7 | underspecified | underspecified | -0.16 | -0.03 | -0.01 |
| ANC-004 | lint-h-11 | not_addressed | not_addressed | -0.07 | +0.00 | +0.00 |
| ANC-004 | lint-h-12 | underspecified | underspecified | +0.01 | +0.00 | +0.03 |
| ANC-004 | lint-h-13 | underspecified | underspecified | +0.03 | +0.00 | +0.01 |
| ANC-004 | lint-h-14 | underspecified | underspecified | +0.03 | -0.06 | +0.00 |
| ANC-005 | lint-h-1 | satisfied | underspecified **FLIP** | +0.13 | -0.09 | +0.02 |
| ANC-005 | lint-h-2 | satisfied | satisfied | +0.09 | +0.00 | +0.02 |
| ANC-005 | lint-h-3 | underspecified | underspecified | -0.12 | +0.10 | +0.04 |
| ANC-005 | lint-h-4 | underspecified | underspecified | +0.06 | -0.05 | +0.01 |
| ANC-005 | lint-h-5 | underspecified | satisfied **FLIP** | +0.00 | +0.07 | -0.02 |
| ANC-005 | lint-h-7 | underspecified | satisfied **FLIP** | +0.03 | +0.17 | +0.00 |
| ANC-005 | lint-h-11 | satisfied | satisfied | +0.00 | +0.05 | +0.01 |
| ANC-005 | lint-h-12 | underspecified | underspecified | +0.00 | +0.00 | +0.03 |
| ANC-005 | lint-h-13 | underspecified | underspecified | +0.00 | +0.00 | +0.00 |
| ANC-005 | lint-h-14 | underspecified | underspecified | +0.14 | +0.19 | +0.06 |
| ANC-006 | lint-h-1 | underspecified | underspecified | +0.00 | +0.03 | +0.04 |
| ANC-006 | lint-h-2 | underspecified | underspecified | -0.21 | +0.06 | +0.00 |
| ANC-006 | lint-h-3 | underspecified | underspecified | +0.08 | +0.00 | +0.04 |
| ANC-006 | lint-h-4 | underspecified | underspecified | +0.13 | +0.01 | +0.03 |
| ANC-006 | lint-h-5 | not_addressed | underspecified **FLIP** | -0.08 | -0.04 | -0.02 |
| ANC-006 | lint-h-7 | underspecified | underspecified | +0.07 | +0.02 | +0.00 |
| ANC-006 | lint-h-11 | underspecified | not_addressed **FLIP** | -0.11 | +0.11 | +0.05 |
| ANC-006 | lint-h-12 | underspecified | underspecified | +0.12 | -0.04 | +0.11 |
| ANC-006 | lint-h-13 | underspecified | underspecified | -0.16 | -0.09 | -0.03 |
| ANC-006 | lint-h-14 | not_applicable | not_applicable | -0.12 | -0.01 | -0.01 |

### E3-C. `jev_judge.py diff` output per bead (prev = E2 primary run, next = E3 override run)

| bead | changed (anchor: from -> to) | diff calls it | pass before -> after |
|---|---|---|---|
| lint-h-1 | ANC-003: underspecified -> not_addressed; ANC-005: satisfied -> underspecified | regressions=['ANC-003', 'ANC-005'] | False -> False |
| lint-h-2 | ANC-001: not_applicable -> underspecified; ANC-003: satisfied -> not_addressed | regressions=['ANC-001', 'ANC-003'] | False -> False |
| lint-h-3 | ANC-002: not_applicable -> underspecified; ANC-003: satisfied -> not_addressed; ANC-004: underspecified -> not_addressed | regressions=['ANC-002', 'ANC-003', 'ANC-004'] | False -> False |
| lint-h-4 | ANC-003: satisfied -> not_addressed | regressions=['ANC-003'] | False -> False |
| lint-h-5 | ANC-005: underspecified -> satisfied; ANC-006: not_addressed -> underspecified | regressions=[] | False -> False |
| lint-h-7 | ANC-003: underspecified -> not_addressed; ANC-005: underspecified -> satisfied | regressions=['ANC-003'] | False -> False |
| lint-h-11 | ANC-003: underspecified -> not_addressed; ANC-006: underspecified -> not_addressed | regressions=['ANC-003', 'ANC-006'] | False -> False |
| lint-h-12 | (none) | regressions=[] | False -> False |
| lint-h-13 | ANC-003: underspecified -> not_addressed | regressions=['ANC-003'] | False -> False |
| lint-h-14 | ANC-003: underspecified -> not_addressed | regressions=['ANC-003'] | False -> False |

Live Jev requests recorded under runs/: 245; total input tokens 1867730.


**Interpretation.** The override did exactly what it was written to do: `addressed` went from
yes/0.27-0.85 or no/0.28-0.72 to no/0.97-1.00 on all ten beads, eight verdicts flipped to
`not_addressed` (the correct verdict) including the three false `satisfied`, and `contradicted` was
untouched (0.79-0.92 before and after). The two beads that stayed `underspecified` (h-5, h-12) did so
because `relevant` dipped to 0.48/0.56; relevance is a separate question whose text did not change, so
that is noise (h-12 was 0.58 before) or cross-talk from the longer override in the same request. No
previously correct ANC-003 verdict regressed because none was correct before. On the five untouched
anchors (E3-B) 8 of 50 verdicts changed with identical text and questions; `relevant` confidence moved by
more than 0.10 in 15 of 50 cells (max 0.21), `addressed` in 5, `contradicted` in 2. Thirteen of the fifty
had min_confidence within 0.1 of the threshold before the re-run, and those are where the flips are. Note
that `jev_judge.py diff` reports every satisfied -> not_addressed as a "regression" (E3-C): it measures
pass/fail direction, not correctness, so a tuning round that removes false passes reads as 100% regressions.

---

## E4. Relevance and scope

### E4-A. not_applicable per anchor vs a human reading of `scope`

| anchor | scope (verbatim) | Jev N/A desc+AC | Jev N/A desc-only | relevant=no leanings (desc+AC) | mean relevant conf | human: beads in scope | scope flag |
|---|---|---:|---:|---|---:|---|---|
| ANC-001 | every phase-i change: architecture documentation, crate dependencies, CLI commands, and the adoption-kit just template | 3 ['h-1', 'h-2', 'h-13'] | 2 ['h-2', 'h-13'] | 6 ['h-1', 'h-2', 'h-3', 'h-5', 'h-12', 'h-13'] | 0.52 | 10 (all touch CLI, crates or kit) | scope right but too broad for the statement to carry; Jev matches the layer list, not the scope |
| ANC-002 | the adoption-kit just template, any sc-lint CLI test command, and any helper sc-lint ships for consumer test recipes | 1 ['h-3'] | 5 ['h-2', 'h-3', 'h-4', 'h-7', 'h-14'] | 3 ['h-3', 'h-4', 'h-14'] | 0.64 | 3-5 (h-2, h-5, h-11; h-12/h-13 partly) | narrow and right; Jev over-reads 'CLI test command' as 'runs tests' |
| ANC-003 | every phase-i sprint bead and its delivered diff | 0 [] | 0 [] | 0 [] | 0.85 | 10 | right |
| ANC-004 | all phase-i documentation, ADR and plan-bead changes | 0 [] | 0 [] | 2 ['h-5', 'h-14'] | 0.43 | 10 (every plan bead) | too narrow in effect: beads are plan-bead changes but read as code work |
| ANC-005 | every phase-i sprint bead and deliverable | 0 [] | 0 [] | 0 [] | 0.89 | 10 | right |
| ANC-006 | every phase-i sprint bead's design field | 1 ['h-14'] | 1 ['h-14'] | 4 ['h-1', 'h-3', 'h-13', 'h-14'] | 0.54 | 10 (every bead has a design) | exact but unusable by the relevance question (names a field, not a subject) |


**E4-B. Phase-label control.** Anchors text with "phase-i" replaced by "phase-h", ANC-001/ANC-004 on
h-1/h-5/h-12: every verdict unchanged, relevance confidence moved -0.08..+0.07, inside noise. The label is
not why relevance is low (`runs/e4-phaselabel/`).

**Interpretation.** ANC-003 and ANC-005 (scope "every phase-i sprint bead ...") got relevant=yes on all
ten beads at 0.85-0.89 mean confidence: the scope matches what a sprint bead is, and Jev agrees. ANC-001's
scope ("every phase-i change: architecture documentation, crate dependencies, CLI commands, and the
adoption-kit just template") is in words as broad as ANC-003's, yet Jev said relevant=no on six beads and
produced three N/A verdicts; the beads never mention architecture or dependencies, they describe features,
so Jev matches the statement's subject (a layer list) and not the scope's. The scope is right and too
broad for the statement to carry: it should either enumerate the bead-level signals (a bead that adds a
CLI command, touches a Cargo.toml, or edits the kit justfile) or the anchor should be judged by its
deterministic check only. ANC-002's scope is correctly narrow (kit template, CLI test command, test helpers)
and Jev's N/A on h-3 is right, but it also leaned relevant=yes on h-1 (0.86) and h-7 (0.36) which only run
`just test` in CI; "any sc-lint CLI test command" is read as "anything that runs tests". ANC-004's scope
("all phase-i documentation, ADR and plan-bead changes") is too narrow in its effect: the bead itself is a
plan-bead change, so relevance should be certain, but Jev gave 0.43 mean and relevant=no on h-5/h-14,
because the beads talk about code, not documents. ANC-006's scope ("every sprint bead's design field")
is exact, yet Jev gave N/A on h-14 at 0.92 and relevant=no on three others when reading the full design;
a scope that names a field of the bead is not something the relevance question knows how to use, since
the question asks about subject-matter overlap and the design field is about everything.

---

## Recommendations for the skill

1. **Do not rely on long beads being judged whole; put anchor-relevant statements first.** The planted
   contradiction scored p=0.68-0.79 at the start of the description and 0.36-0.46 when 22-28k chars deep
   (E1-C), with run noise of 0.05 (E1-D). The skill should tell planners that the Goal paragraph is what
   Jev reads, and the compose-item order (Description first) should be kept.
2. **Keep flint's refuse-and-split at the plan gate, but for a different reason than context size.** Jev
   accepted 107,582 bytes / 31,500 tokens with no 422 (E1-A), so the 24,000-byte default is not protecting
   against Jev; it is a cost/attention bound. A 63k bead buried a contradiction that a 22k bead surfaced
   (E1-C full-middle 0.46 vs descac-start 0.79), so splitting is right, but the limit should be stated
   as "what Jev will actually read", about 20-25k chars, not as a transport limit.
3. **Raise `--max-request-bytes` for the dev gate (where evidence is long) to at least 110,000** since
   Jev handled that size in one attempt (E1-A lint-h-11 full); the halve-and-retry path never fired in
   245 requests.
4. **Judge the plan gate on description + acceptance criteria by default, not the full composed text.**
   Verdicts were identical across all four compositions (E1-B), tokens fell 2.6x (20.6k -> 7.9k for h-3) and 2.7x for h-11,
   and the plant was detected only in the shorter variants. Add a `compose-item --sections` option or a
   plan-gate default that drops Design and Notes.
5. **Script B's code reduction does not change verdicts and should not be the plan gate's main lever**
   (E1-B reduced column equals full for all six pairs; 7-26 blocks removed). Keep it as a size tool, not an
   accuracy tool.
6. **The default `addressed` question fails prohibitions and structural anchors.** ANC-004 (prohibition)
   scored addressed=no on all ten beads although eight say they amend nothing (E2-C); ANC-006 (shape of the
   design) scored addressed=no on nine of ten full-text beads with 6-33 code blocks (E2-D). Add a per-anchor
   `kind` (directive / prohibition / structural): for prohibitions, `decide()` should return `satisfied`
   when `contradicted`=no at or above threshold and `relevant`=yes, without requiring `addressed`=yes; for
   structural anchors, route to the deterministic check and skip the Jev `addressed` question.
7. **The default `addressed` question should name what "the directive's specific content" means for
   this anchor.** The ANC-003 override (concrete layer list, the gh-stack homonym called out, vocabulary
   variants in criteria) moved `addressed` from 0.27-0.85 mixed to no/0.97-1.00 on all ten beads (E3-A)
   and fixed three false passes. The anchor-capture step should generate this override at lock time for
   every anchor rather than leaving `question_overrides` empty, as all six were here.
8. **Make relevance anchor-specific too.** `relevant` limited 23 of 47 underspecified cells (E2-C) and
   produced four false `not_applicable` (ANC-001 h-1/h-2/h-13, ANC-006 h-14). The override should list
   bead-level signals from the scope ("adds a CLI command", "edits Cargo.toml", "has a design field")
   instead of the abstract scope sentence, which Jev does not use (E4).
9. **The 0.6 threshold decides 13 of 60 cells and sits where the confidences are densest** (E2-E: 0.5
   decides 28, 0.4 decides 43; 13 of 50 untouched cells were within 0.1 of 0.6 and 8 flipped on a re-run,
   E3-B). Either lower the plan-gate threshold to 0.5 once overrides are in place (the override pushed
   ANC-003 to 0.97+, where threshold no longer matters), or report `underspecified` cells with the leaning
   so the reviewer sees direction, not just "not confident".
10. **Judge-noise is large enough that a single run should not flip a gate.** Relevance confidence moved
    >0.10 in 15 of 50 identical re-judged cells (max 0.21, E3-B). For gate decisions near the threshold,
    the skill should re-judge once and require agreement, or treat a verdict that differs from the previous
    run on an unchanged anchor as noise before calling it a regression.
11. **`diff` should distinguish "verdict changed" from "regressed".** It labelled all eight correct
    satisfied -> not_addressed flips as regressions (E3-C). Either compare against a recorded expected
    verdict per cell, or rename the field `pass_to_fail`.
12. **Anchor wording guidance: positive, concrete, matchable tokens win over form.** ANC-003 and ANC-005
    (requirements with "names that layer", "#193-#204") got relevant 0.85-0.89 and the only correct
    satisfieds; ANC-001's verbatim shorthand got 0.52 and three false N/A; ANC-004's conditional
    "unless Rand approved" could not be contradicted even by the sentence alone (p=0.23, E1-C). When a
    verbatim statement is kept (as it should be), the `summary` and overrides must carry the concrete
    tokens, and conditional prohibitions should be split into a prohibition plus an approval record.
13. **Resolve the "layer" homonym in this repo's anchors before the dev gate.** Every bead uses "layer"
    for stack position; ANC-003's deterministic check ("each sprint bead names one layer (a)-(d)") will
    fail all ten beads, and the plan gate with default questions passed three of them (E2-C). Add
    "architectural layer (a)-(d)" to the ANC-003 summary and overrides, and ask the planner to add a
    one-line "Layer: (c) CLI" to each bead.
14. **Two real scope findings for phase-i's reviewers that the gate did not raise:** h-4 "Also closes
    PLAN-SCOPE-R2-M1" and h-12 "fixes the bootstrap's existing exit-2 defect" are additions outside
    #193-#204 (ANC-005), and h-5/h-13 add consumer test orchestration to crates/sc-lint (ANC-002's
    deterministic check). Jev gave contradicted p=0.17-0.19 on these; a `contradicted` override that
    lists "additions not tied to an issue number" and "test orchestration in crates/sc-lint" as
    examples is the next tuning round.
