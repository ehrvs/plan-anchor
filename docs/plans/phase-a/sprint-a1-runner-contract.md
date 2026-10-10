# Sprint A1 — Runner contract and single trust resolution

## Objective

Establish the orchestration boundary every later sprint consumes: resolve one
trusted harness agent, invoke it with one typed fenced payload, validate its
single fenced response, and write a credential-safe attestation.

## Scope boundary

This sprint owns registry resolution, runtime descriptors, invocation-envelope
validation, result-envelope validation, and attestation. It does not parse phase
plans, execute tracker commands, change Jev networking, or rewrite agent bodies.

## Dependency relations

- Root sprint; follows the Phase A base on `main`.
- Sprint A2 is `must_follow` because its plan-source descriptor becomes an
  operation field in this runner contract.

## Public contract

```json
{
  "runtime": {
    "agent": "anchor-plan-review",
    "harness": "codex",
    "path": ".codex/agents/anchor-plan-review.md",
    "version": "0.5.0",
    "model": "luna",
    "sha256": "<64 lowercase hex characters>"
  },
  "operation": "plan_review",
  "correlation_id": "phase-a:A1"
}
```

The runtime path is registry-relative and confined to the selected plugin root.
The descriptor is immutable after resolution and contains no credential or
executable command string.

## Authoritative deliverables

- A deterministic resolver for Claude and Codex registries that validates
  plugin confinement, regular-file status, frontmatter identity/version,
  registry version, allowed role model, and SHA-256.
- A versioned JSON schema for the common runtime and operation envelope.
- Harness instructions that invoke the registered agent through Agent with
  exactly one fenced JSON params object.
- A response parser that accepts exactly one fenced JSON result and validates
  success and error envelopes before any follow-on action.
- A redacted attestation schema and atomic writer containing registry identity,
  version, model, file digest, source digest when supplied, correlation ID,
  timing, and outcome.
- Focused error codes for untrusted path, identity/version/model mismatch,
  changed hash, malformed params/result, timeout, and atomic-write failure.

## Authoritative acceptance criteria

- Resolution and attestation occur once per agent invocation; no gate or tuner
  agent searches installation paths or repeats frontmatter trust validation.
- A supplied plugin root or registry entry that fails validation never falls
  back to another location.
- Unknown, missing, wrongly typed, duplicated, or unfenced params/results fail
  closed before another operation begins.
- Claude and Codex invocation instructions use Agent and contain no active Task
  tool instruction.
- Resolver output, error text, and attestations contain neither credentials nor
  interpolated shell command strings.

## Authoritative validation

- Unit fixtures: valid Claude/Codex registry; traversal; symlink escape;
  non-regular file; wrong name/version/model; modified file hash; duplicate JSON
  fences; malformed response; timeout; failed atomic replace.
- Static assertion: gate and tuner definitions contain no installation search
  or independent registry/frontmatter validation after Sprint A5 lands.
- Secret canaries through successful, error, and timeout attestation paths.
- Existing `scripts/check_version_sync.py` and offline unit tests remain green.

## Traceability

- Phase requirements: PA-REQ-001–004, PA-REQ-013.
- Anchors: ANC-001–004, ANC-008, ANC-012.
- Tracker: `pa-sza.1`.

## Risks and mitigations

- Harnesses expose different launch mechanisms: keep the shared descriptor
  identical and isolate only the thin Agent invocation wording.
- Attestation may leak inputs: record digests and typed metadata, not raw params
  or environment values.

## Non-closure

- Markdown phase/sprint discovery.
- `bd`/`br` execution.
- Agent-body simplification.
- General-purpose plugin execution outside plan-anchor.

## Handoff to A2

A2 consumes the envelope schema and adds a validated plan-source descriptor;
it does not reopen runtime trust rules.
