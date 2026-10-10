# Sprint A4 — Configuration and explicit offline behavior

## Objective

Make installation portable and network behavior evident from the command:
`TYPESAFE_API_KEY` is the only application environment input, live execution
needs no second opt-in, and offline paths provably never create transport.

## Scope boundary

This sprint owns CLI configuration, environment reads, transport construction,
and offline-network tests. It does not change Jev question wording, verdict
semantics, retry policy, or plan/tracker discovery.

## Dependency relations

- `must_follow` Sprint A3 so source and tracker choices have stable explicit
  argument contracts before legacy environment paths are removed.
- Sprint A5 is `must_follow` because agent params use the final CLI behavior.

## Authoritative deliverables

- Remove reads of `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE`, `PLAN_ANCHOR_JEV_URL`,
  `PLAN_ANCHOR_JEV_MODEL`, `PLAN_ANCHOR_CONFIDENCE_THRESHOLD`,
  `PLAN_ANCHOR_MAX_ITEM_CHARS`, `PLAN_ANCHOR_MAX_CODE_LINES`,
  `PLAN_ANCHOR_CONFIRM_NEAR`, and `USER` as an author default.
- Remove `--allow-remote`; a live command plus a valid `TYPESAFE_API_KEY` is
  sufficient authorization, while `--dry-run` is the explicit no-send mode.
- Retain or add explicit endpoint, model, threshold, size, confirmation, author,
  source, and tracker flags with checked-in defaults and stable help text.
- Centralize API-key validation at live transport construction and preserve
  recursive redaction of the raw key and bearer forms.
- Separate command preparation from transport creation so dry-run and
  fixture-answer execution require no key and instantiate no client.
- Migrate tests and examples away from ordinary configuration environment vars.

## Authoritative acceptance criteria

- A static test finds exactly one plan-anchor-owned environment read:
  `TYPESAFE_API_KEY`.
- Live execution without the key fails with `AUTH.CREDENTIALS` before any
  transport call; live execution with the key needs no other opt-in.
- `--dry-run` and fixture-answer execution pass without a key and record zero
  transport constructions and calls.
- Help, errors, README, SKILL.md, agents, examples, and Jev references contain no
  active instruction for a removed variable or `--allow-remote`.
- Credential and bearer-token canaries are absent from stdout, stderr, nested
  exceptions, run files, reports, and attestations.

## Authoritative validation

- Transport-spy tests for live missing-key, live successful, dry-run,
  fixture-answer, retry, error, and report paths.
- Repository static scan of application environment reads with an allowlist
  containing only `TYPESAFE_API_KEY`.
- CLI snapshot tests for defaults and each explicit override.
- Existing judge, coverage, diff, shape, and redaction suites remain green.

## Traceability

- Phase requirements: PA-REQ-011–012, PA-REQ-015.
- Locked anchors: ANC-005, ANC-011–012.
- Tracker: `pa-sza.4`.

## Risks and mitigations

- Removing environment overrides breaks hidden tests: enumerate every current
  read first and add flag/default parity before deletion.
- Dry-run accidentally validates or constructs transport: keep offline dispatch
  above credential lookup and prove it with constructor and call spies.

## Non-closure

- Changing Jev endpoint semantics, answer schema, pricing, or retry thresholds.
- Adding credential stores or global shell configuration.
- Agent-body refactoring beyond parameter changes required by removed flags.

## Handoff to A5

A5 consumes the final explicit configuration schema and removes duplicated
bootstrap and tracker logic from each harness-specific agent.
