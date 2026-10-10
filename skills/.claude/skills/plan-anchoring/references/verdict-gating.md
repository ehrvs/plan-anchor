---
name: verdict-gating
version: 0.1.0
description: How jev_judge.py turns independent Jev answers into one verdict per anchor and item, the role contract, thresholds, severity order, coverage, pass criteria, and run diffs.
---

# Verdict gating

Jev cannot gate one question on another inside a request, and it cannot count. Both happen in `scripts/jev_judge.py`, so they are deterministic and testable with fixtures.

## The role contract

A question set maps roles to question IDs:

```json
"roles": {"relevance": "relevant", "compliance": "addressed", "conflict": "contradicted"}
```

`relevance`, `compliance`, and `conflict` are required; `evidence` is optional and used by the development gate. Overrides may rename question IDs only if they update `roles` to match. The script refuses a set whose roles do not resolve (`QUESTIONS.ROLES`).

## From answers to a verdict

Each `choice` answer gives a `choice` and a `confidence` in [0, 1]. The threshold `t` defaults to 0.6 (`--threshold`, or `PLAN_ANCHOR_CONFIDENCE_THRESHOLD`). Evaluated in order; the first match wins:

| # | Condition | Verdict |
| --- | --- | --- |
| 1 | relevance is `no` with confidence >= t | `not_applicable` |
| 2 | conflict is `yes` with confidence >= t | `contradicted` |
| 3 | relevance or compliance is `unclear`, or either confidence < t | `underspecified` |
| 4 | compliance is `no` | `not_addressed` |
| 5 | compliance is `yes` and an evidence role exists and evidence is `no` with confidence >= t | `asserted_only` |
| 6 | compliance is `yes` | `satisfied` |
| 7 | anything else | `underspecified` |

Contradiction outranks underspecification because a confident conflict is actionable even when relevance was shaky. A `noul` answer, if a set uses one, is mapped to yes/no at 0.5 with confidence `abs(p - 0.5) * 2`.

`min_confidence` on each result is the lowest confidence across the three required roles; it is reported so an `underspecified` verdict can be read as "the anchor needs sharper wording" when it recurs across beads.

## Severity order

`contradicted` > `not_addressed` > `asserted_only` > `underspecified` > `satisfied` > `not_applicable`. Results in a run are sorted by severity then anchor ID; reports show failing verdicts first.

## Pass criteria

- A **run** (one item) passes when no result is `contradicted`, `not_addressed`, `asserted_only`, `underspecified`, or `error`.
- The **planning gate** passes when every planning bead's latest run passes and `coverage` lists no uncovered locked anchor.
- The **development gate** passes when the sprint's latest run passes and each returned deterministic check has been run and recorded.

## Coverage, in code

```bash
python3 scripts/jev_judge.py coverage --runs doc/plan/phase-current/anchor-runs --gate plan --format md
```

Takes the latest non-dry run per (gate, item), builds the anchor x item matrix, and lists anchors with no `satisfied` cell. "Is ANC-012 satisfied anywhere?" is answered here, never by Jev. An anchor that is `not_applicable` to every bead is reported as uncovered on purpose: either its scope is wrong or the plan lacks the bead that should carry it.

## Diffing runs

```bash
python3 scripts/jev_judge.py diff --prev anchor-runs/plan-...-bd-42.json --next anchor-runs/plan-...-bd-42.json
```

Lists changed, added, and removed verdicts for the same gate and item, flags regressions, and shows pass before and after. Run it after every plan edit so the planning agent sees exactly what its change did.

## Fixtures and offline runs

`--answers-file` injects Jev-shaped answers keyed by anchor ID (or `*` for all) and skips the network. Use it to:

- unit-test the gating table (see `assets/examples/answers.fixture.json`);
- check that an anchor's `fixtures.pass` and `fixtures.fail` sentences would land as `satisfied` and `not_addressed` or `contradicted`;
- run the skill in CI without an API key.

`--dry-run` writes the exact requests and no verdicts. Dry runs are never counted by `coverage`.
