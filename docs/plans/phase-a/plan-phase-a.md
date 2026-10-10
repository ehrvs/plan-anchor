# Phase A — Self-anchor plan-anchor

## Status and authority

- Status: planning; implementation starts only after plan hardening and the
  plan-anchoring gate complete.
- Source of truth: this file defines Phase A scope, ordering, and closure. Each
  linked sprint document is authoritative for that sprint's deliverables,
  acceptance criteria, validation, and non-closure.
- Intent: [intent.md](intent.md).
- Anchors: [anchors.json](anchors.json), rendered as [anchors.md](anchors.md).
- Tracker epic: `pa-sza`. Tracker records carry identity, dependencies, status,
  question overrides, and review evidence; they do not replace sprint plans.
- Architectural baseline:
  `/Users/randlee/Documents/github/synaptic-canvas/docs/claude-code-skills-agents-guidelines.md`
  v0.7, subject to the locked Agent-tool override.

## Outcome

Phase A makes plan-anchor conform to the architecture it expects other skills
to follow and makes Markdown phase/sprint plans first-class gate inputs.

```text
phase plan/directory OR tracker epic
  -> discover sprint documents OR materialize the tracker copy
  -> normalize one complete sprint item per source entry
  -> resolve trusted harness agent once
  -> select bd or br once for workflow metadata
  -> invoke the harness Agent with one fenced JSON params object
  -> judge one complete sprint document per agent run
  -> persist redacted run evidence and compute phase coverage
```

The resulting workflow can dogfood this Phase A plan twice: once from the
Markdown sprint documents and once from a copy stored under the Phase A `br`
epic. Both routes produce the same normalized sprint items and must produce the
same gate decisions. A small `bd` or `br` database remains required only for
anchor records and their plan/dev question records; the Markdown route does not
require plan work to be modeled as tracker issues.

## Phase requirements

| ID | Requirement |
| --- | --- |
| PA-REQ-001 | Treat the skills/agents guideline as the architectural baseline except where a locked anchor records an approved override. |
| PA-REQ-002 | Invoke Claude and Codex subagents with the Agent tool; active instructions must not direct use of the superseded Task tool. |
| PA-REQ-003 | Resolve the registered agent path, version, model, plugin confinement, and SHA-256 once at the orchestration boundary. |
| PA-REQ-004 | Pass exactly one fenced JSON params object matching the selected agent's documented input contract and reject malformed input or output. |
| PA-REQ-005 | Accept either a Markdown phase plan/directory or a `bd`/`br` epic containing a copy of the sprint plan and judge each discovered sprint as one planning item. |
| PA-REQ-006 | Normalize Markdown and tracker-copy sources to the same item contract; equivalent copies must yield identical item text, source digests, and gate decisions. |
| PA-REQ-007 | Keep Markdown sprint documents authoritative when both representations exist and fail visibly when the tracker copy has drifted. |
| PA-REQ-008 | Limit the mandatory Beads dependency to storing anchor records and their plan/dev question records; a new repository can initialize that store quickly without first modeling its plan as issues. |
| PA-REQ-009 | Support either `bd` or `br` for the anchor/question store and optional tracker plan source through one normalized interface selected once at the orchestration boundary. |
| PA-REQ-010 | Build tracker argv from typed operation data; never accept interpolated shell commands in agent params. |
| PA-REQ-011 | Read no plan-anchor application environment variable except `TYPESAFE_API_KEY`; expose other choices through flags or checked-in defaults. |
| PA-REQ-012 | Make `--dry-run` and fixture-answer execution zero-network paths proven with transport-spy tests. |
| PA-REQ-013 | Keep separate Claude and Codex agent definitions with Sonnet/Opus and Luna/Sol role assignments respectively. |
| PA-REQ-014 | Keep question tuning independent from the planner and driven by a frozen oracle derived from approved intent, anchors, fixtures, and boundary probes. |
| PA-REQ-015 | Keep Jev required for the normal workflow and preserve recursive credential/bearer-token redaction in every observable or persisted output. |
| PA-REQ-016 | Keep examples executable against current harness and tracker output shapes and repository-valid paths. |
| PA-REQ-017 | Do not define or invoke the sc-lint agents `arch-qa` or `req-qa` from this plugin. |

## Quality requirements

| ID | Requirement |
| --- | --- |
| PA-NFR-001 | Every sprint is independently reviewable and production-ready for its stated boundary. |
| PA-NFR-002 | Each sprint has one authoritative list each for deliverables, acceptance criteria, paths to delete when applicable, and required validation. |
| PA-NFR-003 | Every dependency is identified as `must_follow` or `parallel_safe` with a rationale; no later sprint silently absorbs unfinished closure. |
| PA-NFR-004 | Boundary failures are typed and actionable; malformed data never becomes executable shell text. |
| PA-NFR-005 | Offline tests are deterministic and require neither a TypeSafe credential nor network access. |
| PA-NFR-006 | Plan review evidence identifies source kind, stable source identity, and normalized content digest for every run. |
| PA-NFR-007 | Markdown and tracker-copy review remain parity-testable without sending both representations in one Jev request. |

## Architectural boundaries

### Plan source adapters

The user-facing invocation accepts a Markdown phase index, its directory, or a
tracker epic. The Markdown adapter locates one unambiguous phase index, reads
only repository-local links from its sprint table, and rejects duplicate or
escaping paths. The tracker adapter enumerates the epic's sprint children and
composes their title, description, and acceptance criteria without using design
or notes. Both return the same ordered descriptor and normalized item contract:

```json
{
  "phase": "phase-a",
  "source": "docs/plans/phase-a/plan-phase-a.md",
  "sprints": [
    {
      "id": "A1",
      "path": "docs/plans/phase-a/sprint-a1-runner-contract.md",
      "sha256": "<64 lowercase hex characters>",
      "source_kind": "markdown",
      "source_ref": "docs/plans/phase-a/sprint-a1-runner-contract.md",
      "tracker_id": "pa-sza.1",
      "normalized_sha256": "<64 lowercase hex characters>"
    }
  ]
}
```

For Markdown, the complete sprint file is the planning item. For a tracker copy,
the normalized title, description, and acceptance criteria are the item. The
phase index, epic, and intent frame discovery and tuning but are not concatenated
into every Jev request. Each run records both a source-specific revision and the
normalized item digest. The dogfood copy must match that digest before its
verdicts are compared; drift is a source error, not a Jev disagreement.

### Runtime trust and invocation

The skill is the harness runner because only the harness can invoke Agent. A
deterministic resolver reads the harness registry under the selected plugin
root, confines its relative path, verifies frontmatter name/version/model, and
computes SHA-256. It returns an immutable runtime descriptor; gate and tuner
agents do not search installation paths or re-attest registered artifacts.

Every Agent invocation carries one fenced JSON object containing the runtime
descriptor, plan-source descriptor, tracker descriptor, operation fields, and
correlation ID. The runner rejects missing, unknown, wrongly typed, duplicated,
or unfenced fields and validates the single fenced JSON result before using it.

### Anchor/question store and tracker boundary

The mandatory tracker use is a lightweight anchor/question store: one anchor
record plus plan-question and dev-question children for each locked fact. It can
be initialized quickly with `bd` or `br` in a repository whose plan exists only
as Markdown. The same adapter may optionally read a tracker epic as the plan
source and post review evidence, but Markdown review does not require plan issues.

The adapter owns only `show`, `children`, `create`, `update`, and `comment`. An
explicit `bd` or `br` selection wins; otherwise capability probes must find
exactly one valid repository workspace. Operations use fixed argv arrays,
normalize JSON envelopes, and never migrate storage.

### Configuration and network behavior

`TYPESAFE_API_KEY` is the only plan-anchor-owned environment variable. Endpoint,
model, threshold, size, confirmation, author, tracker, and source choices use
explicit flags or checked-in defaults. A normal live command plus a valid key
is sufficient. `--dry-run` and fixture-answer execution instantiate no network
transport and work without the key.

## Sprint stack

| Sprint | Authoritative plan | Tracker | Relation | Closure |
| --- | --- | --- | --- | --- |
| A1 | [Runner contract and trust resolution](sprint-a1-runner-contract.md) | `pa-sza.1` | root | Establish the trusted runtime descriptor, fenced invocation envelope, and redacted attestation. |
| A2 | [Markdown and tracker plan sources](sprint-a2-markdown-plan-source.md) | `pa-sza.2` | `must_follow` A1 | Normalize linked Markdown sprints and a tracker epic copy to one gate input contract. |
| A3 | [Tracker-neutral anchor/question store](sprint-a3-tracker-neutrality.md) | `pa-sza.3` | `must_follow` A2 | Support quickly initialized `bd` or `br` anchoring state without requiring plan issues. |
| A4 | [Configuration and offline behavior](sprint-a4-configuration-and-offline.md) | `pa-sza.4` | `must_follow` A3 | Reduce environment configuration and prove offline execution never sends. |
| A5 | [Harness-specific agent simplification](sprint-a5-harness-agents.md) | `pa-sza.5` | `must_follow` A4 | Move resolved source/runtime/tracker contracts into focused Claude and Codex agents. |
| A6 | [Mechanical compliance gates](sprint-a6-compliance-gates.md) | `pa-sza.6` | `must_follow` A5 | Turn every locked invariant into executable regression checks. |
| A7 | [Documentation, examples, and dogfood](sprint-a7-documentation-and-dogfood.md) | `pa-sza.7` | `must_follow` A6 | Align public docs and pass independent tuning, sprint review, and phase coverage on this plan. |

All relations are `must_follow` because each sprint changes a public contract
consumed by the next. Parent development is merged forward before each child
development or fix round, and parent PRs merge before child PRs. One `gh-stack`
PR represents each implementation sprint.

## Traceability

| Concern | Phase requirements | Locked anchors | Owning sprints |
| --- | --- | --- | --- |
| Guideline and Agent invocation | PA-REQ-001–004 | ANC-001–004, ANC-008 | A1, A5, A6 |
| Dual plan sources and Markdown authority | PA-REQ-005–007 | ANC-015–016 | A2, A7 |
| Lightweight `bd`/`br` anchor store | PA-REQ-008–010 | ANC-007–008, ANC-017–018 | A3, A5, A6 |
| Environment and offline execution | PA-REQ-011–012 | ANC-005–006 | A4, A6 |
| Harness roles and independent tuning | PA-REQ-013–014 | ANC-009–010 | A5, A6, A7 |
| Jev, redaction, examples, plugin boundary | PA-REQ-015–017 | ANC-011–014 | A4, A6, A7 |

## Phase acceptance

- `/plan-anchoring` against the phase file, its directory, and the `pa-sza`
  tracker copy discovers the same seven ordered sprint items.
- Markdown and tracker-copy materialization have identical normalized digests;
  separate Jev runs produce identical per-anchor verdicts for each sprint.
- Each run records source kind, source identity/revision, and normalized digest;
  tracker-copy drift fails before judging.
- A repository with only Markdown plans can initialize `bd` or `br` solely for
  anchor/question records and complete capture, tuning, and review.
- Both `bd` and `br` fixture and installed-binary integration contracts pass.
- `TYPESAFE_API_KEY` is the only application-specific environment read; dry-run
  and fixture modes make zero transport calls.
- Claude and Codex registries, agent roles, schemas, manifests, and version
  declarations pass mechanical consistency validation.
- Credential canaries remain absent from stdout, stderr, errors, reports,
  attestations, and run files.
- The independently tuned planning gate passes every sprint document and phase
  coverage contains no uncovered locked anchor.
- The existing offline test suite, new Phase A tests, documentation examples,
  version checks, and `git diff --check` all pass.

## Phase-wide non-closure

- Replacing Jev or changing verdict semantics and confidence policy.
- Building a general-purpose runner or tracker migration framework for other
  plugins.
- Making `bd` and `br` share a database format.
- Adding sc-lint agents to plan-anchor.
- Reopening marketplace packaging completed before Phase A except where a
  manifest must change for an implemented Phase A contract.
- Treating free-form Markdown or an unstructured tracker epic as a hardened plan.

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Markdown discovery becomes convention-heavy | Parse one explicit sprint table and fail on ambiguity; cover valid and invalid repositories with fixtures. |
| A large sprint document exceeds reliable Jev context | Run `shape`, harden or split the sprint on production-ready boundaries, and never silently trim prose. |
| Tracker copies drift from source documents | Compare normalized digests before parity review and identify Markdown as authority for this phase. |
| Supporting two trackers doubles agent branching | Select and normalize once in the adapter; agents consume one typed contract. |
| Central trust resolution weakens repository-input safety | Keep workspace confinement for plan, anchor, run, and evidence paths inside agent preflight. |
| Dogfood is biased toward passing | Independent Sol tuning freezes its oracle before gate results; every Jev failure is preserved and triaged. |

## Handoff after Phase A

Phase B may extend source profiles or development evidence only after Phase A's
Markdown source, tracker, invocation, and attestation contracts are stable and
the self-hosted planning gate has passed. Remaining findings become explicit
dependent tracker work; they are never carried silently in this phase plan.
