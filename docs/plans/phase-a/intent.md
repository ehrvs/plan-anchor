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
  ordered sprint items and matching request digests, then pass independent live
  reviews; differing answers are preserved as model instability rather than
  source-adapter drift;
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

Question tuning is performed by an evaluator independent from the planner. The
evaluator freezes an oracle from this intent and the locked anchor before seeing
Jev's answers, and it optimizes for agreement with that oracle rather than for
making the current plan pass.
