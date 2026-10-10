# Sprint A7 — Documentation, examples, and dogfood

## Objective

Make the public contract match shipped behavior and prove plan-anchor can review
this authoritative Phase A Markdown plan through its own independent tuner and
Jev-backed planning gate.

## Scope boundary

This sprint owns public documentation, executable examples, migration notes,
question-tuning evidence, planning runs, triage diffs, and final coverage. It
does not weaken anchors, questions, size limits, or verdicts to obtain a pass.

## Dependency relations

- `must_follow` Sprint A6 because documentation and dogfood describe and execute
  the final mechanically enforced behavior.
- Final sprint; Phase A closes only after its acceptance criteria pass.

## Authoritative deliverables

- Update README, SKILL.md, installation/troubleshooting, Jev API, anchor and
  tracker layout, planning/development gate references, PRD, architecture
  diagrams, manifests, and changelog to the final contracts.
- Document phase-index, directory, and tracker-epic invocation; source parity;
  authoritative sprint sections; the anchor/question-only store; explicit
  flags; and offline behavior.
- Replace stale environment-variable, prose-invocation, tracker-body, and
  hard-coded `bd` examples with executable current examples for both harnesses
  and trackers.
- Render `anchors.md`, keep tracker question/evidence references linked, and
  include the Markdown-authority anchors added during dogfood.
- Verify A0's frozen bootstrap corpus and acceptance evidence, then run the
  calibrated rubric against every locked anchor before plan-question tuning.
- Run the independent Sol question tuner for every non-structural anchor/gate,
  record the frozen oracle digest, accepted override, acceptance table, and run
  IDs in `question-tuning-evidence.md`, and apply only independently justified
  overrides.
- Run one `anchor-plan-review` Agent per sprint first from Markdown and then from
  the `br` copy, preserve Jev verdicts unchanged, require matching normalized
  request digests and independently passing results, classify differing live
  answers as model instability, and rerun only affected inputs.
- Compute phase coverage from the latest run per sprint and publish the final
  source paths/digests, failures corrected, size deltas, and any allowed growth
  with pre-existing authority. Keep offline source-construction evidence in
  `dogfood-dry-run.md` and live verdict evidence in a separate record so a dry
  run can never be mistaken for gate acceptance.

## Authoritative acceptance criteria

- Documentation consistency, link, manifest, version, and executable-example
  tests pass for Claude/Codex and `bd`/`br`.
- Jev is identified as required for the normal workflow; dry-run and fixture
  modes are accurately described as offline development/CI aids.
- Every tuning result was produced independently from the active plan verdicts
  and meets its frozen oracle at the required confidence.
- Every sprint's latest Markdown and tracker-copy runs pass and record matching
  normalized request digests; recorded-answer parity runs have identical
  verdicts, and phase coverage has no uncovered anchor.
- Every failing-to-passing edit that grew cites a locked ANC/REQ/ADR that
  predates the failed run; otherwise the fix cuts or replaces text.
- The full offline suite, live dogfood evidence, and `gh stack view --json`
  report a clean, mergeable Phase A implementation stack.

## Authoritative validation

- Execute all README and reference command examples in temporary repositories
  against recorded and installed supported tracker versions.
- Run `validate`, `lint`, `dedupe`, `render`, source discovery, independent
  `check-fixtures`, per-sprint planning review, `diff`, and `coverage`.
- Run the A6 offline suite and version validator after the final documentation
  edits.
- Verify no secret appears in Git diff, logs, reports, run files, comments, or
  attestations.
- Verify the final PR stack with `gh stack view --json` and GitHub checks.

## Traceability

- Phase requirements: PA-REQ-001–018.
- Locked anchors: ANC-001–002, ANC-005, ANC-009–018.
- Tracker: `pa-sza.7`.

## Risks and mitigations

- Dogfood tunes toward passing: the Sol tuner freezes its oracle before seeing
  Jev results and never receives current plan verdicts.
- Documentation repeats scope inconsistently: sprint plans remain authoritative;
  examples demonstrate contracts without restating deliverable checklists.
- Live requests expose secrets or excessive context: send only one anchor and
  one sprint per request and exercise recursive redaction canaries first.

## Non-closure

- Waiving a Jev failure, lowering confidence to pass, or rewriting an anchor from
  a live failure alone.
- Adding unrelated marketplace work or sc-lint agents.
- Starting Phase B implementation.

## Phase handoff

Close Phase A only when every acceptance criterion in the phase index and this
sprint is satisfied. File explicit dependent work for any remaining finding;
do not carry it silently into implementation or Phase B.
