---
name: report-format
version: 0.1.0
description: The provenance-quoting report format for gate results and what the planning agent or quality manager should do with each verdict.
---

# Report format

Every failing verdict names the fact and quotes the statement behind it, so the planning agent gets the user's intent back in the user's own words. `scripts/jev_judge.py report --run <file> --format md` renders it; nothing is written by hand.

## Shape

```markdown
## Anchor gate: plan · bd-42 - Sprint 2 runtime

Run `plan-20261009T183000Z-bd-42`, model `jev-1.13.0`, threshold 0.6. Counts: not_addressed 1, satisfied 3, not_applicable 9.

> **bd-42 · ANC-012 · not addressed** You said (planning session, Oct 9): "copy the libraries from ATM as the starting point and remove the ATM-specific code" This bead does not carry the directive forward.

> **bd-42 · REQ-014 · contradicted** REQ REQ-014 says: "All public CLI commands must support --json output with a stable schema." This bead proposes something the anchor rules out.
```

Line anatomy: `item · anchor · verdict`, then provenance (`You said (<context>, <date>)` for ANC; `<REQ|ADR> <id> says` for register facts), the verbatim statement in quotes, then a one-sentence explanation that depends only on the verdict, because Jev does not explain itself. Satisfied and not-applicable rows are omitted unless `--all` is passed.

## What to do with each verdict

| Verdict | Planning gate (planning agent) | Development gate (quality manager) |
| --- | --- | --- |
| `contradicted` | Rewrite the bead's approach to match the directive, or escalate to the user if the user has changed their mind (then retire the anchor and lock a new one) | Block acceptance. The work must change, or the user must retire the anchor explicitly |
| `not_addressed` | Add the directive's specific content to the bead: the starting point, the constraint, the step | Block acceptance until the sprint report shows the directive was followed, then re-run |
| `asserted_only` | n/a at this gate | Ask for evidence (paths, diff, command, test) or run the paired `deterministic_check` and record it |
| `underspecified` | Read `min_confidence`. If the same anchor is underspecified across several beads, sharpen its `scope` or override its questions in the plan-questions bead. If only this bead, the bead is vague: add detail | Same; vague sprint reports are a reporting defect, not an anchor defect |
| `satisfied` | Nothing | Run the paired deterministic check if any |
| `not_applicable` | Nothing. If the anchor should have applied, its `scope` is too narrow | Same |
| `error` | Read `results[].error`; usually credentials, opt-in, or rate limiting | Same |

Three runs on the same bead with the same failing set is a hard stop: escalate to the user rather than editing again.

## Where reports go

- Planning gate: comment on the judged planning bead (`bd comment <bead> --body-file <report.md>`) so the next planning session finds it with the bead.
- Development gate: comment on the sprint bead and, when there is a PR, on the PR.
- Both: the run JSON stays in `doc/plan/phase-current/anchor-runs/` and is committed with the plan.

Posting is done by the skill in the main session after the agent returns. Agents return JSON and never write to beads or PRs.

## Coverage report

`coverage --format md` renders the anchor x item matrix with a Covered column and a closing list of uncovered anchors. Include it at the end of a planning-gate pass so the user sees the whole plan's state, not one bead's.
