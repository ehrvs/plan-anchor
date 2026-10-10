# plan-anchor

Plan anchoring skill using TypeSafe's Jev decision model to stop plans and code drifting from what the user actually said.

While a plan is discussed, the facts the user states ("copy the ATM crates as the starting point", "no new dependency for this") are captured verbatim as numbered anchors (`ANC-001`...), alongside existing requirements (`REQ-*`) and ADRs (`ADR-*`). Each becomes a set of orthogonal Jev questions and is judged at two gates: the planning gate (does each plan bead still say what you said?) and the development gate (did the delivered sprint work follow it?). Failing verdicts quote your own words back.

The design is in [docs/plan-anchor-prd.md](docs/plan-anchor-prd.md).

## Layout

```
skills/.claude/
├── skills/plan-anchoring/
│   ├── SKILL.md                      # entry point and table of contents
│   ├── references/                   # one document per aspect
│   ├── scripts/jev_judge.py          # deterministic core: IDs, Jev calls, gating, coverage, diffs, reports
│   └── assets/                       # question sets of record, templates, worked example, fixtures
└── agents/
    ├── anchor-plan-review.md         # planning gate, one bead per run
    ├── anchor-sprint-review.md       # development gate, one sprint per run
    └── registry.yaml
```

Copy `skills/.claude/` into a project as `.claude/`, or install through a marketplace (pending).

## Requirements

- `python3` 3.9+ (the script is standard-library only)
- `bd` (beads) 1.x
- `TYPESAFE_API_KEY`, plus `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` per session for live gate runs; capture, locking, dry runs, and fixture runs need neither

## Quick check

```bash
S=skills/.claude/skills/plan-anchoring/scripts/jev_judge.py
python3 $S judge --anchors skills/.claude/skills/plan-anchoring/assets/examples/anchors.example.json \
  --gate plan --all --item-id smoke --item-file README.md \
  --answers-file skills/.claude/skills/plan-anchoring/assets/examples/answers.fixture.json --out /tmp/anchor-smoke.json
python3 $S report --run /tmp/anchor-smoke.json --format md
```

## Status

Skill, references, script, and agents: drafted, offline-tested against fixtures. Live Jev runs and marketplace packaging (Claude Code, Codex, Cursor): not yet done.
