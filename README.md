# plan-anchor

A Claude Code skill that keeps plans, and the code built from them, anchored to what you actually said while planning. Facts you state are captured verbatim as numbered **anchors**, turned into typed questions for [TypeSafe's Jev](https://typesafe.ai) decision model, and enforced mechanically at two gates: once against the plan, once against the delivered work. When something drifts, the report quotes your own words back.

> **Data leaves the machine only when you say so.** A gate run sends the anchor statement and the plan or work text to `api.typesafe.ai`. It requires `TYPESAFE_API_KEY` and an explicit per-session opt-in, `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1`; without both, the skill refuses and sends nothing. The key is never printed, logged or written to disk by the skill.

## The problem

Over a long planning conversation the specific things you say get compressed out of an agent's context. You ask for something concrete, "copy these crates from the legacy repo as the starting point and strip the legacy-specific code", the agent writes it down, and several rounds later it quietly writes a new implementation from scratch. Nothing checks that the plan still says what you said, or that the delivered work matches the plan, so you re-state the same facts every time you re-open the plan.

## How it works

1. **Capture.** While you plan, the orchestrator watches for directives about *how* the work must be done. For each one it writes one testable requirement (the anchor `statement`), keeps your exact words as the `quote`, checks the statement against a testability rubric and existing anchors, and proposes both. Nothing is locked until you confirm. A phase needs five to fifteen anchors, not one per sentence.
2. **Record and tune.** Locked anchors are numbered (`ANC-001`...) and stored with provenance in `doc/plan/phase-current/anchors.json`, rendered to `anchors.md`, and given a small bead tree so their questions version alongside the work. Existing requirements (`REQ-*`) and ADRs (`ADR-*`) join the same record under their own IDs. A background agent then tests the generic Jev questions against each anchor's pass and fail fixtures and rewrites them until Jev judges that anchor reliably.
3. **Planning gate.** Each planning bead is judged against every anchor by three orthogonal Jev questions: is the anchor relevant to this bead, does the bead address it, does the bead contradict it. Answers are gated in code into one verdict per anchor, coverage is computed across beads, and you iterate until nothing is forgotten or contradicted.
4. **Development gate.** When a sprint is delivered, the same anchors are judged against the account of the work (sprint report, PR, diff summary, tests) with a fourth question: is compliance *evidenced*, not just asserted. Each satisfied anchor is paired with a deterministic check, because Jev judges text and only a diff proves the code.
5. **Report and iterate.** A failing verdict reads: `bd-42 · ANC-012 · not addressed  Anchor: The runtime crates are created by copying the legacy repo's runtime crates and deleting the legacy-specific modules. You said (planning session, Oct 9): "copy the libraries from the legacy repo as the starting point and remove the legacy-specific code" This bead does not carry the directive forward.` Each finding is triaged (plan defect, anchor defect, question defect, or Jev error), fixed where the defect is, and re-run. An oversized bead is treated as a symptom: unapproved work is removed first, then prose and ceremony, and only remaining approved work is split.

The design is documented in [docs/design/architecture-and-call-graphs.md](docs/design/architecture-and-call-graphs.md) (components, call graphs and fan-out for both gates, retry policy) and [docs/design/data-model-and-gating.md](docs/design/data-model-and-gating.md) (record schema, verdict gating, lifecycle). The original PRD is [docs/plan-anchor-prd.md](docs/plan-anchor-prd.md).

## Use cases

- **Long or multi-session planning.** You re-open a phase plan next week; the skill loads the anchors first and nothing you said has to be repeated.
- **Multi-agent delivery.** A planning agent drafts beads, dev agents implement, a quality manager reviews. The planning gate stops forgotten directives before code exists; the development gate stops the quality manager accepting work that planned the directive and then abandoned it.
- **Requirement and ADR enforcement.** Numbered requirements and decisions you already maintain are judged bead by bead with the same machinery, so "REQ-014 is satisfied somewhere in this plan" is computed, not remembered.
- **Pull request review against the plan.** Point the development gate at a PR and get, per anchor, whether the PR description shows the directive was followed and where to look to confirm it.
- **CI without a key.** Fixture answers exercise the whole pipeline offline, so the gating logic and report format are testable and a failing gate exits non-zero.
- **Promoting decisions.** An anchor that proves durable is promoted to an ADR and keeps its ID and history.

Not for: general code review, style review, or plan hardening without anchors. It composes with plan-hardening workflows rather than replacing them.

## Installation

Copy `skills/.claude/` into your project as `.claude/`, or install through a marketplace once one is published (Claude Code, Codex and Cursor packaging is planned).

| Need | For | Notes |
| --- | --- | --- |
| `python3` 3.9+ | everything | The script is standard-library only |
| `bd` ([beads](https://github.com/steveyegge/beads)) 1.x | the bead tree and reading beads | Agents use it read-only; the skill creates anchor beads and posts comments from the main session |
| `TYPESAFE_API_KEY` | live gate runs | Get a key at typesafe.ai. Export it in the shell that launches Claude Code |
| `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` | live gate runs | Per-session opt-in; set it only when sending this plan's text to TypeSafe is acceptable |

Capture, locking, dry runs and fixture runs need neither the key nor the opt-in.

## Quick start

```bash
S=.claude/skills/plan-anchoring/scripts/jev_judge.py
A=doc/plan/phase-current/anchors.json

# lock the first anchor (creates anchors.json) and render the human view
python3 $S add --anchors $A --quote "copy the libraries from the legacy repo as the starting point and remove the legacy-specific code" \
  --statement "The runtime crates are created by copying the legacy repo's runtime crates and deleting the legacy-specific modules; no runtime crate is written from scratch." \
  --stated-by "<name>" --context "planning session" --summary "Runtime crates copied, not rewritten" \
  --scope "any bead that creates the runtime crates" --status locked
python3 $S validate --anchors $A && python3 $S render --anchors $A

# see exactly what a planning-gate request would send, without a key
python3 $S judge --anchors $A --gate plan --all --item-id bd-42 --item-file /tmp/bd-42.txt --dry-run

# run the planning gate for a bead (needs the key and the opt-in), then read the report
PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1 python3 $S judge --anchors $A --gate plan --all --item-id bd-42 --item-file /tmp/bd-42.txt
python3 $S report --run doc/plan/phase-current/anchor-runs/<run>.json --format md

# coverage across all judged beads
python3 $S coverage --runs doc/plan/phase-current/anchor-runs --gate plan --format md
```

In a Claude Code session the skill does this for you: say "anchor this" or "lock this" while planning, then "run the planning gate on the sprint 2 beads" or "review sprint 2 against the anchors". The gates run in the `anchor-plan-review` and `anchor-sprint-review` subagents; under Codex or Cursor, which have no subagents, the skill follows the agent's steps itself.

## What you get back

| Verdict | Meaning | Planning gate | Development gate |
| --- | --- | --- | --- |
| `contradicted` | The item proposes or did what the anchor rules out | Change the approach or escalate | Block acceptance |
| `not_addressed` | The item is silent on the directive | Add the directive's specific content | Block until the work shows it |
| `asserted_only` | Compliance is claimed with nothing checkable | n/a | Get evidence or run the deterministic check |
| `underspecified` | Jev was not confident | Sharpen the anchor's scope or the bead | Usually a vague report |
| `satisfied` | The directive is carried forward or followed | Nothing | Run the paired deterministic check |
| `not_applicable` | The anchor does not govern this item | Nothing | Nothing |

Every run is stored in `anchor-runs/` so edits can be diffed against the last run. Coverage, counts and "satisfied anywhere" are computed from run files, never asked of Jev. Verdicts are gate outcomes, but before editing on one, the caller re-reads the exact text that was sent and says so in the report if Jev looks wrong.

## Repository layout

```
docs/
├── plan-anchor-prd.md                     product requirements
└── design/                                architecture, call graphs, data model, gating
skills/.claude/
├── skills/plan-anchoring/
│   ├── SKILL.md                           entry point and table of contents
│   ├── references/                        one document per aspect
│   │   ├── anchor-capture.md              detecting, proposing, confirming, wording anchors
│   │   ├── anchor-document.md             intent.md, anchors.json, anchors.md, IDs, lifecycle
│   │   ├── bead-layout.md                 the anchor bead tree and bd commands
│   │   ├── plan-anchor-questions.md       planning-gate question set
│   │   ├── code-review-questions.md       development-gate question set and evidence
│   │   ├── verdict-gating.md              answers to verdicts, coverage, diffs
│   │   ├── report-format.md               the provenance-quoting report
│   │   ├── jev-api.md                     endpoint, limits, retries, privacy opt-in
│   │   └── installation-and-troubleshooting.md
│   ├── scripts/jev_judge.py               deterministic core (see below)
│   ├── assets/questions/{plan,dev}.json   question wording of record
│   ├── assets/templates/                  intent.md and question-bead templates
│   └── assets/examples/                   worked anchors.json and fixture answers
└── agents/
    ├── anchor-plan-review.md              planning gate, one bead per run
    ├── anchor-sprint-review.md            development gate, one sprint per run
    └── registry.yaml
```

### The script

`jev_judge.py` owns everything that must not be left to a language model.

| Subcommand | Does |
| --- | --- |
| `add`, `update`, `retire`, `promote` | Maintain the anchor record; `add` allocates the next `ANC-NNN`, lints the statement and refuses near-duplicates |
| `lint`, `rubric`, `dedupe`, `shape` | Testability lint (deterministic); Jev-judged testability rubric; duplicate detection (lexical, optionally Jev); per-bead size and ceremony metrics |
| `validate`, `render` | Check the record; write `anchors.md` |
| `set-beads` | Record the anchor tree's bead IDs |
| `compose-item` | Turn `bd show --json` output into the labelled item text the agents send |
| `judge` | One Jev request per anchor for one item; gating; writes the run file. Exit 0 pass, 1 failing gate, 2 fatal |
| `check-fixtures` | Judge each anchor's pass and fail fixture sentences and confirm they land as expected |
| `report`, `coverage`, `diff` | Render a run; anchors × items matrix; what changed between runs |

Requests stay under 24,000 bytes; an item that still exceeds Jev's context window is halved and retried down to 2,000 characters; transient API failures get three attempts with backoff before an anchor is marked `error`. Credential and opt-in failures abort immediately and are never retried.

## Development

```bash
python3 -m unittest discover -s skills/.claude/skills/plan-anchoring/tests -v
```

Tests use fixture answers and a stub transport; they cover ID allocation, gating, overrides, retries and context shortening, response validation, report format, coverage and diffs, not Jev's judgment. CI runs them on Linux, macOS and Windows with Python 3.9 and the latest 3.x. A smoke run with no key (exits 1 because the example gate fails by design):

```bash
S=skills/.claude/skills/plan-anchoring/scripts/jev_judge.py
X=skills/.claude/skills/plan-anchoring/assets/examples
python3 $S judge --anchors $X/anchors.example.json --gate plan --all --item-id smoke --item-file README.md \
  --answers-file $X/answers.fixture.json --out /tmp/anchor-smoke.json && python3 $S report --run /tmp/anchor-smoke.json --format md
```

## Status

Revision 0.3, shaped by first use on a real multi-sprint plan and by 245 live Jev requests against it ([docs/experiments/2026-10-10-phase-h-jev-experiments.md](docs/experiments/2026-10-10-phase-h-jev-experiments.md)). What that round changed:

- Anchors are testable requirements with the user's words kept as a `quote`; a testability lint, a Jev-judged rubric and deduplication guard capture, because the first live use minted untestable, duplicated anchors from raw sentences.
- Anchor kinds: prohibitions are judged on contradiction only and structural anchors by their deterministic check, because the generic "addressed" question failed both on every bead.
- The planning gate judges a bead's description and acceptance criteria; a planted contradiction scored 0.79 near the top of a bead and 0.46 when buried 28k characters into its design. An oversized bead is a symptom, triaged as unapproved work, then prose and ceremony, then split last; `shape` measures it first.
- Per-anchor question tuning is a background agent's job with fixtures and known beads as the acceptance test; one tuned question corrected three false passes on a real plan.
- Near-threshold cells are re-asked once because run-to-run noise flipped one cell in six; every cell reports its leaning.

The script has 117 offline tests on Linux, macOS and Windows in CI. Marketplace packaging for Claude Code, Codex and Cursor is next.

## Versioning

One version for everything: `SKILL.md`, every reference, every agent, `registry.yaml`, and the plugin and marketplace manifests once they exist. `VERSION` holds it; `scripts/check_version_sync.py` runs in CI and fails on any drift or on a release without a `CHANGELOG.md` entry. Bump only at a release, all artifacts together; never one file on its own.

## License

MIT. See [LICENSE](LICENSE).
