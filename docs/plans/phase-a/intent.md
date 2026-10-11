# Phase A intent: make plan-anchor conform to its own standard

## Purpose

Plan-anchor should apply the same pressure to its own design that it applies to
other plans. Phase A brings the skill and its harness-specific agents into
conformance with the Claude Code Skills and Agents Architecture Guidelines,
using the user's explicit corrections where the guideline is stale. The work
should make invocation simpler, safer, and easier to install: resolve trusted
artifacts once, pass one structured parameter object, support either `bd` or
`br`, and avoid machine-specific configuration.

## Sources of truth

- `/Users/randlee/Documents/github/synaptic-canvas/docs/claude-code-skills-agents-guidelines.md`
  is the architectural baseline.
- The locked anchors in `anchors.json` are the user-approved overrides and
  constraints for this phase.
- Claude uses the Agent tool, not the superseded Task tool.
- Existing behavior that already satisfies an anchor is preserved and covered
  by regression tests rather than redesigned.

## Success

Phase A succeeds when:

- a skill-level runner resolves the harness-specific agent path, registry
  version, declared model, and file hash once before invocation;
- a Markdown phase plan/directory and a tracker epic copy normalize to the same
  ordered sprint items and byte-identical outbound Jev request JSON, then pass
  independent live reviews; differing answers to identical requests are
  preserved as model instability rather than source-adapter drift;
- Markdown remains authoritative when both forms exist, while a quickly
  initialized `bd` or `br` database is required only for anchor and question
  records unless the user also chooses the tracker-copy plan source;
- each invocation supplies one fenced JSON params object and rejects malformed
  input or output at the boundary;
- individual agents contain no installation-path search or duplicated registry
  trust logic;
- tracker operations work with both `bd` and `br` through a small normalized
  interface selected once by the orchestrator;
- `TYPESAFE_API_KEY` is the only plan-anchor-owned environment variable, with
  ordinary behavior controlled by explicit CLI arguments and checked-in
  defaults;
- `--dry-run` and fixture-answer modes are proven to make no network calls;
- harness-specific agents, independent question tuning, Jev requirements,
  secret redaction, and realistic examples remain consistent across the skill,
  README, design documents, tests, and plugin manifests;
- harness-specific `anchor-tuning` is a dedicated Opus/Sol subagent of the
  planner: it freezes and owns tuning judgment, calls Jev directly and in
  parallel over a larger candidate-question pool than production review will
  use, ranks and down-selects that pool, and never tunes toward an active plan
  result;
- `anchor-tuning` treats approved INTENT and ANC records as its only normative
  authority. It is neutral rather than adversarial or plan-serving: temporary
  plan copies may gain explicit ceremony or lose required statements solely to
  measure whether candidate questions detect presence and absence accurately;
  authoritative Markdown and tracker copies remain byte-for-byte read-only;
- the direct runner and ordinary review agents reproduce the same sealed
  question set and outbound request JSON for the Markdown and tracker copies,
  then the review agents are proven against dogfood `br` and known external
  `bd` and `br` plan fixtures;
- after a first plan draft and approved INTENT/ANC packet exist, the planner
  launches a named `<team>-anchor-tuning` subagent and continues completing the plan
  concurrently, so calibrated questions are sealed before Sonnet/Luna leaf
  review begins;
- the tuning subagent may return clarity-only INTENT/ANC recommendations with a
  semantic-equivalence rationale, but cannot apply them; the user approves each
  authority change, after which affected oracles and rankings are invalidated
  and rerun;
- the testability rubric is independently calibrated against a frozen,
  plan-independent oracle and reports uncertainty or disagreement without
  mislabeling either as an anchor defect; and
- the Phase A planning gate passes every locked anchor before implementation is
  accepted.

## Out of scope

- Replacing Jev or changing plan/development verdict semantics, confidence
  thresholds, or the anchor data model; Phase A may correct the bootstrap
  testability rubric's questions, confirmation, and uncertainty states.
- Adding `arch-qa`, `req-qa`, or any other sc-lint agent to this plugin.
- Building a general-purpose agent runner for unrelated plugins.
- Accepting an unstructured monolithic Markdown document as a hardened phase
  plan; the supported form is a phase index plus authoritative sprint docs.
- Making `bd` and `br` share a database format; Phase A normalizes their CLI
  operations while each tracker retains its own storage.
- Redesigning the marketplace packaging completed before Phase A.

## Review policy

Question tuning is performed by an evaluator independent from the planner's
desired result. The evaluator freezes an oracle from this intent and the locked
anchors before seeing Jev's answers, and it optimizes for agreement with that
oracle rather than for making the current plan pass. The evaluator is the
harness-specific Opus/Sol `anchor-tuning` subagent. In `tune` mode it cannot
receive the active plan as authority or receive a desired plan verdict. It
generates multiple candidate questions per role, calls Jev directly and in
parallel against the same frozen oracle, and uses judgment plus recorded
accuracy, confidence, stability, regression, and simplicity evidence to select
the smaller production question set. It may use a read-only proposed plan only
as diagnostic material copied into its temporary workspace: add explicit
ceremony to a copy to test recognition and remove important statements or
deliverables from another copy to test missing-content detection. These are
neutral calibration cases, never edits to the original.

The planner does not wait until the plan is finished to begin this work. Once a
first draft exists and the user-approved INTENT/ANC authority packet is stable
enough to evaluate, it launches the named subagent
`<team>-anchor-tuning` and continues authoring in parallel. Sonnet/Luna plan
review waits for the subagent's sealed question-set digest. If the tuner finds
an ambiguity in INTENT or ANC, it returns a clarity-only recommendation rather
than silently guessing. The user decides whether to apply it; approval versions
the authority record and restarts every affected oracle/candidate result.

After the planner runs `anchor-plan-review`, any disputed failure is sent back
to `anchor-tuning` only through a checked-in `sc-compose` Jinja2 template. The
template carries the raw review request and response, the sealed question-set
digest, and the applicable versioned INTENT/ANC authority. It treats every
planner claim—including "the plan is fine; fix the questions"—as untrusted
context and explicitly forbids changing an accurate question merely to obtain a
pass. The tuner must independently return exactly one evidence-backed
disposition: `plan_violation`, citing the INTENT/ANC obligation the plan fails
and leaving the sealed question digest unchanged; or `question_defect`, citing
why Jev's response does not support the INTENT/ANC oracle and reopening only the
affected question tournament. No desired verdict is a template input.
