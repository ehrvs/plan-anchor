# Sprint A5 — Harness-specific agent simplification

## Objective

Reduce each Claude and Codex agent to one gate or tuning responsibility after
runtime trust, Markdown source, tracker, and configuration decisions move to
their owning boundaries.

## Scope boundary

This sprint owns the six harness-specific agent definitions and their registry
contracts. It preserves separate files and model roles and does not merge agents
or introduce sc-lint reviewers.

## Dependency relations

- `must_follow` Sprint A4 because agents consume the complete runtime, source,
  tracker, and configuration descriptors established in A1–A4.
- Sprint A6 is `must_follow` because it mechanizes the final agent contracts.

## Agent matrix

| Role | Claude model | Codex model | Responsibility |
| --- | --- | --- | --- |
| `anchor-plan-review` | Sonnet | Luna | Judge one authoritative sprint Markdown document against selected anchors. |
| `anchor-sprint-review` | Sonnet | Luna | Judge one delivered sprint evidence package and return deterministic checks. |
| `anchor-question-tune` | Opus | Sol | Freeze an independent oracle and tune one anchor/gate question set. |

## Authoritative deliverables

- Update all six definitions to accept exactly one fenced params object using
  immutable runtime, plan-source/evidence, tracker, and operation descriptors.
- Replace `script` path hints, installation searches, and repeated registry /
  frontmatter checks with the pre-resolved runtime descriptor.
- Replace direct `bd`/`br` commands with normalized adapter operations and read
  planning item text from the bound sprint file, not a tracker description.
- Retain repository confinement for anchor, sprint, run, question, override, and
  evidence paths; keep one-operation responsibility and typed errors.
- Keep the tuner isolated from planner objectives and active plan verdicts; it
  freezes its oracle before the first Jev answer and returns auditable evidence.
- Measure final file sizes and split only if a definition still owns multiple
  responsibilities, not solely to satisfy a byte target.

## Authoritative acceptance criteria

- Every registered definition has valid frontmatter plus Inputs, Output Format,
  Error Handling, and Constraints sections matching its schema.
- Plan and sprint gate agents contain no installation fallback, direct tracker
  branching, or second artifact-attestation implementation.
- Plan review takes one sprint path/digest and never substitutes tracker prose;
  result metadata echoes the reviewed source.
- Claude and Codex registries remain version/model consistent with Sonnet/Opus
  and Luna/Sol assignments.
- No active instruction uses Task, and no file defines or invokes `arch-qa` or
  `req-qa`.

## Authoritative validation

- Schema fixtures for valid params/results; missing/unknown/wrongly typed fields;
  duplicate/unfenced JSON; timeout redispatch with an existing run.
- Static scans for path search, direct tracker commands, Task-tool wording, and
  forbidden sc-lint agent names.
- Contract tests proving identical normalized operations across Claude/Codex
  definitions and role-specific model assertions.
- Independent-tuner fixtures proving current plan pass/fail is never an input.

## Traceability

- Phase requirements: PA-REQ-002–010, PA-REQ-013–014, PA-REQ-017.
- Anchors: ANC-001–004, ANC-007–010, ANC-014, ANC-016–018.
- Tracker: `pa-sza.5`.

## Risks and mitigations

- Removing safety prose removes real controls: map every deleted instruction to
  the runner, source adapter, tracker adapter, or retained agent preflight test.
- Shared contracts erase harness differences: share schemas, not files or model
  declarations.

## Non-closure

- Adding agents beyond the three plan-anchor roles per harness.
- Changing question or verdict semantics.
- Refactoring unrelated marketplace or sc-lint agents.

## Handoff to A6

A6 converts these final contracts and every locked deterministic check into CI
assertions before documentation claims the behavior is shipped.
