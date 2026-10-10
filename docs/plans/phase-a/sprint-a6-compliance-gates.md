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

## Traceability

- Phase requirements: PA-REQ-001–017.
- Anchors: ANC-001–018.
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
