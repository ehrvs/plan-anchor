---
name: plan-anchoring
version: 0.1.0
description: Capture the facts a user states while planning as numbered, verbatim anchors (ANC-001...) alongside existing requirements (REQ) and ADRs, turn them into Jev-judged questions, and enforce them at two gates. The planning gate checks each plan bead still says what the user said; the development gate checks the delivered sprint work followed it. Use when planning a phase or sprint with beads, when the user says "anchor this", "lock this", "don't let this drift", or "remember I said", when re-opening a plan after context compression, or when reviewing a sprint against its plan. Not for general code review, and not a replacement for plan hardening.
---

# Plan Anchoring

Facts stated during planning get compressed out of context, and plans and code quietly drift from them. This skill makes each stated fact durable: captured verbatim, numbered, turned into orthogonal Jev questions, and judged mechanically at two gates. You state a fact once; the skill holds the plan and the agents to it from then on.

This file is the table of contents. Each aspect has one reference document under `references/`; read the one for the step you are on, not all of them.

## Step 1 - Verify dependencies

Run this before any capture, delegation, or gate. Do not proceed with a missing dependency; surface the gap and stop.

```bash
which python3 && python3 --version          # 3.9 or newer
which bd && bd --version                    # beads CLI, 1.x
test -n "$TYPESAFE_API_KEY" && echo "TYPESAFE_API_KEY set" || echo "TYPESAFE_API_KEY missing"
echo "remote judge opt-in: ${PLAN_ANCHOR_ALLOW_REMOTE_JUDGE:-unset}"
```

If `bd` is not on PATH, Claude Code's bash may not share your shell's PATH. Check common locations:

```bash
for p in "/opt/homebrew/bin/bd" "$HOME/go/bin/bd" "$HOME/.local/bin/bd" "/usr/local/bin/bd"; do
  [ -x "$p" ] && echo "Found at: $p" && break
done
```

If found at a non-PATH location, `export PATH="<dir>:$PATH"` for the session. If anything is missing, read `references/installation-and-troubleshooting.md` before proceeding. Capture and locking (steps A and B) need only `python3` and `bd`; the gates (steps C and D) also need the API key and the explicit opt-in described in `references/jev-api.md`, because they send the anchor statement and the item text to TypeSafe.

## Concepts

| Concept | ID | What it is | Where it comes from |
| --- | --- | --- | --- |
| Intent | none | One-page "why" for the plan; frames every question but is not judged | Written during planning |
| Anchor | ANC-NNN | A fact the user stated while planning, stored in their exact words | What the user says |
| Requirement | REQ-* | A numbered technical requirement already in the requirement register | Existing register |
| ADR | ADR-* | A numbered architectural decision record | Existing register |

All three ID'd kinds become Jev questions and are judged the same way. Details: `references/anchor-document.md`.

## Layout

```
doc/plan/phase-current/
├── intent.md            # the overview
├── anchors.json         # record of truth: every anchor with provenance, status, beads, fixtures
├── anchors.md           # rendered from anchors.json; never hand-edited
└── anchor-runs/         # one JSON per gate run; versioned with the plan for diffs
```

Beads hold the questions so they live and version with the work: one anchor bead per fact, with a plan-questions child and a dev-questions child (`references/bead-layout.md`). The deterministic tooling is `scripts/jev_judge.py`; run `python3 .claude/skills/plan-anchoring/scripts/jev_judge.py --help` for its subcommands.

## Workflow

### A. Capture anchors while planning (main session, interactive)

Read `references/anchor-capture.md`. While planning, watch for directives the user states about how the work must be done. When you detect one, propose it as an anchor by quoting their exact words, and record it only when they confirm or when they say "lock this" or "anchor this". Never paraphrase the statement. One testable constraint per anchor.

### B. Lock and record

```bash
S=.claude/skills/plan-anchoring/scripts/jev_judge.py
A=doc/plan/phase-current/anchors.json
python3 $S add --anchors $A --statement "<verbatim words>" --stated-by "<name>" --context "planning session" \
  --summary "<short paraphrase for tables>" --scope "<where it applies>" --status locked
python3 $S validate --anchors $A && python3 $S render --anchors $A
```

Then create the bead tree and record the bead IDs with `set-beads` (`references/bead-layout.md`). Requirements and ADRs that govern this plan are added the same way with `--source-type REQ|ADR --source-ref <ID>`; they keep their register ID. If `intent.md` does not exist yet, create it from `assets/templates/intent.md`.

### C. Planning gate

For each planning bead, delegate to `anchor-plan-review` (see Agent Delegation). It prepares the context, resolves question overrides from the plan-questions beads, runs the judge once per anchor, and returns verdicts. Then compute coverage across beads in code, never by asking Jev:

```bash
python3 $S coverage --runs doc/plan/phase-current/anchor-runs --gate plan --format md
```

Act on verdicts per `references/report-format.md`, edit the plan, and re-run. Compare runs with `diff --prev <run> --next <run>`. The gate passes when every bead has no `contradicted`, `not_addressed`, or `underspecified` verdict and every locked anchor is `satisfied` by at least one bead. Question design: `references/plan-anchor-questions.md`. Verdict logic: `references/verdict-gating.md`.

### D. Development gate (sprint review)

When a sprint's work is delivered, the quality-manager side delegates to `anchor-sprint-review` with the sprint ID and the evidence to judge (sprint report, PR description, diff summary, test output). It runs the development question set, which adds an evidence question so "we followed it" is separated from "here is where". Pair every `satisfied` or `asserted_only` verdict with the anchor's `deterministic_check` when one is recorded; Jev judges text, and only a diff or git history proves the code did what the text says. Question design: `references/code-review-questions.md`.

### E. Report

Reports quote the user's own words back, in the format of `references/report-format.md`. Post the markdown from `report --format md` as a comment on the judged bead (`bd comment <id> ...`) or on the PR so the record travels with the work.

### F. Maintain

An anchor that proves durable is promoted: `promote --id ANC-012 --adr ADR-0007` keeps the ID and adds the reference. A statement is never reworded in place; a changed directive is a new anchor and the old one is retired (`status: retired` in `anchors.json`). Lifecycle rules: `references/anchor-document.md`.

## Agent Delegation

Capture (A) and locking (B) are interactive and stay in the main session. The gates are tool-heavy and run in isolated agents that return fenced JSON; the skill presents results to the user.

| Operation | Agent | Inputs | Returns |
| --- | --- | --- | --- |
| Planning gate, one bead | `anchor-plan-review` | `bead_id`, `anchor_ids` or `all`, `anchors_path`, optional `run_dir`, `threshold`, `dry_run`, `correlation_id` | fenced JSON: run path, pass flag, per-anchor verdicts, report markdown |
| Development gate, one sprint | `anchor-sprint-review` | `sprint_id`, `evidence` paths or `pr_number`, `anchor_ids` or `all`, `anchors_path`, optional `run_dir`, `threshold`, `dry_run`, `correlation_id` | fenced JSON: run path, pass flag, per-anchor verdicts, deterministic checks to pair, report markdown |

To invoke, instruct: "Use the Agent Runner to invoke `anchor-plan-review` as defined in `.claude/agents/registry.yaml` with parameters: bead_id bd-42, anchor_ids all, anchors_path doc/plan/phase-current/anchors.json." Run at most 3 beads in parallel, one `correlation_id` each, and aggregate in bead-ID order. Treat unfenced or malformed JSON from an agent as failure. Where no Task tool exists (Codex, Cursor), follow the agent file's Execution Steps inline.

## Positions taken on the PRD's open questions

- **Granularity**: one testable constraint per anchor. A compound statement becomes several anchors that each quote the sentence carrying their constraint.
- **Capture**: the orchestrator proposes candidates it detects; nothing is locked until the user confirms or says "lock this".
- **Fast-model cross-check**: not in this version. Jev's own per-question confidence drives the `underspecified` verdict instead.
- **Relationship to plan hardening**: standalone and composable. Run the planning gate as an extra step after hardening; neither skill depends on the other.
- **Data retention**: fail closed. The gates refuse to call TypeSafe unless `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` is set for the session, and `--dry-run` shows exactly what would leave the machine.
- **Fixture authorship**: the skill drafts one pass and one fail fixture per anchor at lock time; the user approves them. Fixtures are judged with `--answers-file` in CI, never sent to Jev as plan text.

## Hard stops

- A statement that is not the user's verbatim words is not an anchor. Stop and ask for the exact wording.
- Never send more than one bead or one work description per Jev request, and never the whole plan.
- Never compute coverage, counts, or "satisfied anywhere" by asking Jev. The script does it.
- Missing `bd`, `python3`, API key, or opt-in: surface and stop; do not degrade silently.
- Three consecutive gate runs on the same bead with the same failing set: escalate to the user rather than editing the plan again.

## References

- `references/anchor-capture.md` - detecting, proposing, confirming, and wording anchors
- `references/anchor-document.md` - intent.md, anchors.json schema, anchors.md, IDs, lifecycle, promotion
- `references/bead-layout.md` - the anchor bead tree, bd commands, labels, question overrides in beads
- `references/plan-anchor-questions.md` - the planning-gate question set and why it is orthogonal
- `references/code-review-questions.md` - the development-gate question set and what evidence to feed it
- `references/verdict-gating.md` - how independent Jev answers become one verdict, thresholds, coverage, diffs
- `references/report-format.md` - the provenance-quoting report and what to do with each verdict
- `references/jev-api.md` - endpoint, request and response shape, limits, privacy opt-in, environment variables
- `references/installation-and-troubleshooting.md` - installing python3, bd, and the API key; PATH issues
- `assets/questions/plan.json`, `assets/questions/dev.json` - the question wording of record
- `assets/templates/intent.md`, `assets/templates/anchor-questions-bead.md`, `assets/examples/` - starting points and a worked example
