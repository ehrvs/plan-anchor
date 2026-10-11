# Sprint A6 — Mechanical compliance and regression gates

## Objective

Turn the architectural guideline, locked anchors, and A1–A5 public contracts
into executable checks that fail for the intended reason before release.

## Scope boundary

This sprint owns validators, fixtures, and CI wiring. It may make narrowly
required production fixes uncovered by those tests but does not redesign the
contracts or documentation narrative.

## Dependency relations

- `must_follow` Sprint A5 because it validates the final code and agent shape.
- Sprint A7 is `must_follow` because public examples and dogfood rely on these
  checks as their release gate.

## Authoritative deliverables

- Extend release validation for frontmatter, required sections, registry and
  manifest parity, model roles, skill dependencies, path confinement, version,
  and changelog consistency.
- Enforce Agent-tool wording and reject active Task-tool instructions.
- Enforce the application environment allowlist and zero-network offline paths.
- Validate the Markdown phase/sprint source contract, structured invocation
  examples, response envelopes, and source-path/digest attestations.
- Add `bd` and `br` contract fixtures, installed-binary smoke hooks, ambiguity
  handling, and command-injection cases.
- Add credential canaries across stdout, stderr, nested errors, reports,
  attestations, run files, and timeout/retry paths.
- Add bootstrap-rubric state-machine and recorded-answer tests for `testable`,
  `needs_work`, `inconclusive`, `unstable`, two-call agreement, and third-call
  disagreement resolution.
- Add duplicate-detection regression cases proving that shared provenance does
  not override distinct atomic statements while genuine statement overlap is
  still rejected.
- Add tuner-isolation tests proving `anchor-tuning tune` cannot receive an
  active plan as authority and `triage` cannot accept a desired verdict,
  requested disposition, or planner-proposed question text.
- Add tuning-tournament tests proving candidate questions are evaluated in
  parallel against identical frozen cases, rank components and rejection reasons
  are persisted, semantic judgment can reject a misleading high score, and only
  down-selected questions enter production review requests.
- Add neutral plan-mutation tests: ceremony is added and required content is
  removed only in temporary copies, expectations are traceable to intent/ANC,
  source hashes remain unchanged, and a real baseline-plan failure is reported
  for plan repair rather than used to retune questions.
- Add lifecycle tests proving `<team>-anchor-tuning` starts as a planner
  subagent after the first
  draft/approved authority packet, overlaps planner work, and seals current
  questions before Sonnet/Luna review can begin.
- Add authority-recommendation tests proving proposals are clarity-only and
  non-mutating, user approval is required, rejected proposals preserve versions,
  and approved changes invalidate/restart all and only affected tuning evidence.
- Add strict `sc-compose` and JSON Schema tests for tune requests, triage
  feedback, and tuner results covering declared variables, missing values,
  deterministic rendering, exactly one valid fenced JSON payload, the Standard
  response envelope, hostile planner text remaining inert data, the exact
  anti-pass-seeking instruction, and the absence of desired-verdict fields.
- Add triage mutation tests in which the planner says "the plan is correct; fix
  the questions." When raw evidence supports the failure, the only valid result
  is a cited `plan_violation` with an unchanged question digest. When a frozen
  oracle proves a question defect, require a cited `question_defect` and
  affected-only tournament restart.
- Add differential request tests that compare direct and review-agent,
  Markdown, `bd`, and `br` canonical Jev JSON byte for byte and retain a typed
  root-cause record for every injected divergence.
- Preserve and run existing judge, coverage, diff, shape, redaction, and version
  suites alongside new tests.

## Authoritative acceptance criteria

- Every locked anchor's deterministic check maps to at least one named
  executable assertion, recorded in a traceability fixture.
- Negative fixtures fail on the expected typed error or validator rule rather
  than on unrelated setup.
- CI fails on a deliberately escaping Markdown path, tracker-body substitution,
  unfenced result, wrong model, forbidden env read, Task instruction, raw secret,
  or direct tracker branch in an agent.
- CI fails when the tuning profile declares nested Agent/subagent capability, a
  direct Jev call can change oracle/question state, source metadata enters a Jev
  body, or two equivalent source paths serialize different request JSON.
- CI fails when candidate evaluation changes the oracle/case set, omits a
  candidate result, ranks on current-plan passage, or leaks unselected tuning
  questions into the production Jev body.
- CI fails if tuning treats plan text as normative, writes an authoritative
  Markdown/tracker source, derives an expected mutation result from a desired
  plan verdict, or changes sealed questions after baseline-plan review.
- CI fails if review consumes default/stale questions while the named tuning
  subagent is incomplete, or if a recommendation changes meaning, bypasses the user,
  or reuses evidence from an earlier authority version.
- CI fails if planner-to-tuner review feedback bypasses the checked-in template,
  if the rendered prompt lacks the anti-pass-seeking instruction, if triage
  returns a third disposition or omits an INTENT/ANC citation, or if an accurate
  failure changes the sealed question digest.
- The complete offline suite and `scripts/check_version_sync.py` pass on a clean
  checkout with no API key or network.
- Test output and persisted fixtures contain no live credential or machine-only
  absolute path.

## Authoritative validation

- `python3 -m unittest discover -s plugins/sc-plan-anchor/skills/plan-anchoring/tests -p 'test_*.py'`.
- `python3 scripts/check_version_sync.py`.
- New source/runner/tracker contract suites on Linux, macOS, and Windows where
  supported by existing CI.
- `git diff --check` and secret-canary repository scan.
- Mutation fixtures for each prohibited condition listed in acceptance.
- `sc-compose validate --strict --lint --check-render` and strict sample renders
  of all three installed anchor-tuning templates, followed by JSON Schema
  validation of each extracted fenced payload.
- Recorded-answer differential fixtures from this Phase A plan and selected
  sc-lint plans, each materialized through Markdown plus disposable `bd` and
  `br` stores.

## Traceability

- Phase requirements: PA-REQ-001–026.
- Locked anchors: ANC-001–002, ANC-005, ANC-009–018, ANC-020–031.
- Tracker: `pa-sza.6`.

## Risks and mitigations

- Static checks reward wording games: pair them with behavior tests and negative
  fixtures for each boundary.
- Installed tracker versions vary: keep recorded fixture contracts mandatory and
  make installed-binary smoke tests report unsupported versions explicitly.

## Non-closure

- Full end-to-end live Jev acceptance; A7 owns live dogfood.
- General linting rules for unrelated plugins.
- Performance optimization not required by a measured regression.

## Handoff to A7

A7 updates every public document/example to the mechanically enforced contract,
then runs independent tuning and Jev review on this Phase A plan itself.
