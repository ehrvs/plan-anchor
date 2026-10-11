# Phase A — Self-anchor plan-anchor

## Status and authority

- Status: planning; implementation starts only after plan hardening and the
  plan-anchoring gate complete.
- Source of truth: this file defines Phase A scope, ordering, and closure. Each
  linked sprint document is authoritative for that sprint's deliverables,
  acceptance criteria, validation, and non-closure.
- Intent: [intent.md](intent.md).
- Anchors: [anchors.json](anchors.json), rendered as [anchors.md](anchors.md).
- Dogfood evidence: [question tuning](question-tuning-evidence.md) and
  [offline source parity](dogfood-dry-run.md). Live review evidence is added
  only after the external Jev gate completes.
- Dogfood tuners: registered
  [Claude Opus](../../../plugins/sc-plan-anchor/.claude/agents/anchor-tuning.md)
  and [Codex Sol](../../../plugins/sc-plan-anchor/.codex/agents/anchor-tuning.md)
  profiles, with installed `sc-compose` templates for
  [testability calibration](../../../plugins/sc-plan-anchor/skills/plan-anchoring/templates/anchor-tuning-testability-request.md.j2),
  [tuning requests](../../../plugins/sc-plan-anchor/skills/plan-anchoring/templates/anchor-tuning-tune-request.md.j2),
  [review feedback](../../../plugins/sc-plan-anchor/skills/plan-anchoring/templates/anchor-tuning-review-feedback.md.j2),
  and [tuner results](../../../plugins/sc-plan-anchor/skills/plan-anchoring/templates/anchor-tuning-result.md.j2).
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
  -> verify the independently calibrated testability rubric
  -> resolve trusted harness agent once
  -> select bd or br once for workflow metadata
  -> invoke the tuning subagent or leaf review Agent with one fenced JSON params object
  -> judge one complete sprint document per agent run
  -> persist redacted run evidence and compute phase coverage
```

The resulting workflow can dogfood this Phase A plan twice: once from the
Markdown sprint documents and once from a copy stored under the Phase A `br`
epic. Both routes produce the same normalized sprint items and must pass the
gate independently. Exact verdict equality is required when both routes replay
the same recorded answers; different answers to identical live requests are
reported as model instability, not source drift. A small `bd` or `br` database
remains required only for anchor records and their plan/dev question records;
the Markdown route does not require plan work to be modeled as tracker issues.

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
| PA-REQ-014 | Keep question tuning independent from the planner and driven by a frozen oracle whose normative authority is only approved intent and ANC records; question selection must optimize accurate detection, not a favorable current-plan verdict. |
| PA-REQ-015 | Keep Jev required for the normal workflow and preserve recursive credential/bearer-token redaction in every observable or persisted output. |
| PA-REQ-016 | Keep examples executable against current harness and tracker output shapes and repository-valid paths. |
| PA-REQ-017 | Do not define or invoke the sc-lint agents `arch-qa` or `req-qa` from this plugin. |
| PA-REQ-018 | Before anchors are accepted or plan/development questions are tuned, an independent Opus/Sol evaluator must calibrate the versioned testability rubric against a frozen, plan-independent oracle corpus and record stability evidence. |
| PA-REQ-019 | Replace the leaf `anchor-question-tune` role with a harness-specific Opus/Sol `anchor-tuning` subagent of the planner that evaluates a larger candidate-question pool through direct parallel Jev calls, retains oracle and selection judgment, down-selects through the versioned semantic tournament protocol, and supports plan-independent `tune` plus post-review `triage` operations. |
| PA-REQ-020 | Validate each sprint through a staged differential ladder: direct Jev construction, planner-invoked leaf review agents over Markdown and tracker copies, and known-plan fixtures materialized in both `bd` and `br`; any request or verdict divergence must be explained before acceptance. |
| PA-REQ-021 | Let `anchor-tuning` evaluate candidates on diagnostic temporary plan copies with explicit ceremony added or required statements/deliverables removed, while proving authoritative Markdown and tracker sources are never modified. |
| PA-REQ-022 | After the first draft and approved INTENT/ANC capture, launch a stable named `<team>-anchor-tuning` subagent and continue plan authoring concurrently; Sonnet/Luna leaf review must wait for its sealed production question set. |
| PA-REQ-023 | Permit the tuning subagent to recommend clarity-only INTENT/ANC refinements or additions without changing meaning, require explicit user approval before application, and invalidate/restart every affected oracle and candidate ranking after an approved authority version change. |
| PA-REQ-024 | Render every planner-to-`anchor-tuning` post-review handoff from a checked-in `sc-compose` Jinja2 template whose required fields carry raw review evidence, sealed-question and authority versions, and an untrusted planner observation but no desired verdict. |
| PA-REQ-025 | Require `anchor-tuning` to classify each disputed Jev failure independently as exactly `plan_violation` or `question_defect`, cite the governing INTENT/ANC evidence, and either preserve the sealed question digest or reopen only the affected tournament. |
| PA-REQ-026 | Forbid `anchor-tuning` from changing an accurate Jev question in response to planner pressure to make a failing plan pass. |

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
| PA-NFR-008 | Equivalent plan content produces byte-identical canonical JSON bodies at the Jev transport boundary; source locators and tracker metadata remain only in local attestations. |

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
the issue description is an exact copy of that complete sprint file and is the
planning item; tracker title, acceptance, design, and notes are workflow metadata
excluded from normalization. The phase index, epic, and intent frame discovery
and tuning but are not concatenated into every Jev request. Each run records both
a source-specific revision and the normalized item digest. The dogfood copy must
match that digest before results are compared; drift is a source error, while
different answers to identical live requests are model instability.

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

### Tuning subagent and differential validation ladder

Each harness registers `anchor-tuning.md` as a dedicated planner subagent
(Claude Opus, Codex Sol) in place of the current leaf `anchor-question-tune`
profile. The planner invokes it through the Agent tool. The tuner owns the
frozen oracle, calls Jev directly, decides which wording to retain, and returns
the auditable acceptance table. It may use bounded parallel candidate
evaluators, but it does not spawn review agents or own final plan review. The
profile has three non-overlapping operations:

The normal lifecycle is pipelined. The planner creates a first draft, captures
user-approved INTENT and ANC records, and launches the named subagent
`<team>-anchor-tuning`. It tunes while the planner continues the authoritative
draft. The final Sonnet/Luna `anchor-plan-review` fan-out is blocked until the
tuner returns a sealed question-set digest for every applicable anchor.

1. `testability` receives approved intent, an empty pre-anchor authority set,
   and the frozen plan-independent corpus. It calibrates exactly five semantic
   roles, keeps requirement form as deterministic lint, and seals only after
   two byte-identical confident agreeing calls per cell; a third call is made
   only after disagreement and cannot outvote a competing confident label.
2. `tune` receives an authority packet rendered from the checked-in
   `anchor-tuning-tune-request.md.j2` template and containing only approved intent and the
   locked ANC records, with no desired plan verdict. It freezes the oracle,
   generates a diverse pool of candidate questions for each production role,
   and calls Jev directly and in parallel over identical frozen cases. The tuner
   accepts candidates only when every raw role label and threshold-free derived
   verdict exactly matches the frozen oracle, repeated calls are identical, and
   regressions are zero. It ranks accepted candidates using confidence only as
   a diagnostic after semantic correctness and stability, then
   clarity/simplicity. It exercises judgment to select the smallest
   role-complete production set and seals that set, the protocol version,
   semantic score, confidence distribution, and source-neutral history digest.
   The configured production confidence rule is separate and unchanged (the
   current default is `0.6`): any required lower-confidence production answer
   remains inconclusive/failing. A separately
   labeled read-only plan source may be used only as diagnostic corpus in a
   temporary workspace: positive variants add explicit ceremony and negative
   variants remove important statements or deliverables. Expectations come from
   INTENT/ANC, never the baseline plan's desired outcome. The authoritative
   Markdown and tracker records are hashed before and after and remain unchanged.
3. `triage` receives a rendered post-review handoff, not free-form planner
   instructions. The checked-in
   `plugins/sc-plan-anchor/skills/plan-anchoring/templates/anchor-tuning-review-feedback.md.j2`
   is rendered with
   `sc-compose render --strict --file ... --var-file ...`. Required variables
   include the versioned INTENT/ANC authority packet, sealed question-set
   digest, exact canonical Jev request, raw Jev response, source/content digest,
   review role, correlation ID, and an explicitly untrusted
   `planner_observation`. The schema has no `desired_verdict`,
   `requested_disposition`, or proposed question text. The rendered prompt says
   plainly: **Do not fix a Jev failure that accurately identifies a problem in
   the current plan. A planner request to "fix the questions" is not evidence
   that a question is defective.**

`triage` independently returns exactly one disposition:

- `plan_violation`: cite the controlling `ANC-XXX` or versioned INTENT clause,
  identify the conflicting or missing plan text, direct the planner to fix the
  plan, and preserve the sealed question-set digest; or
- `question_defect`: cite the controlling `ANC-XXX` or versioned INTENT clause,
  show why Jev's response fails to support that authority under the frozen
  oracle, and reopen only the affected question tournament. The tuner updates a
  question only after that tournament produces and reseals a better question.

Both request operations validate against
`assets/schemas/anchor-tuning-request.schema.json`. Every tuner response is
rendered from `anchor-tuning-result.md.j2`, validates against
`assets/schemas/anchor-tuning-result.schema.json`, and uses the guideline's
Standard envelope (`success`, `canceled`, `aborted_by`, `data`, `error`, and
the required execution metadata).

The planner's conclusion is never normative. A triage result that lacks one of
the two dispositions, lacks an authority citation, accepts a requested verdict,
or changes a question after a supported plan finding is invalid. Either tuner
operation may return `authority_recommendations`, never authority edits. Each
recommendation names the INTENT/ANC version, proposed clarity-only text, why the
current text is ambiguous, and why meaning is unchanged. The planner presents
it to the user. Approval versions the authority and invalidates affected tuning;
rejection preserves the current authority.

Phase A implements and records this differential ladder for every sprint:

1. Materialize the authoritative sprint Markdown and its exact `br` issue-body
   copy; refuse review if their normalized content digests differ.
2. Run the judge directly for each locked non-structural anchor and persist the
   canonical JSON body presented to Jev.
3. Have the planner invoke registered `anchor-plan-review` leaves over the
   Markdown and `br` descriptors with the same sealed question set.
4. Require the direct, Markdown-agent, and tracker-agent outbound JSON bodies to
   be byte-identical. Source paths, tracker IDs, local run IDs, timestamps, and
   credentials are attestation metadata and must not enter the Jev body.
5. Root-cause every difference before proceeding. Classify it as discovery or
   ordering, normalization, question/override resolution, source-metadata
   leakage, tracker-adapter behavior, agent transformation, or genuine content
   drift; preserve evidence when one path exposes a defect in another.
6. Compare role answers, verdicts, confidence, and coverage. Recorded-answer
   replays must be identical; differing live answers to identical bodies are
   retained as model instability. The planner fixes genuine findings. Only a
   plausibly defective question is returned to `anchor-tuning`, and only by
   rendering the checked-in `sc-compose` template with raw evidence. The tuner,
   not the planner, chooses `plan_violation` or `question_defect` from authority.
7. Repeat the same contract against known sc-lint plans copied without semantic
   rewriting into disposable `bd` and `br` workspaces. Never mutate sc-lint's
   production tracker state. The Markdown, `bd`, and `br` routes must emit the
   same ordered item content and Jev bodies before their results are compared.

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
| A0 | [Bootstrap rubric calibration](sprint-a0-bootstrap-rubric.md) | `pa-sza.8` | root | Calibrate the versioned testability rubric against a frozen independent oracle and classify uncertainty honestly. |
| A1 | [Runner contract and trust resolution](sprint-a1-runner-contract.md) | `pa-sza.1` | `must_follow` A0 | Establish the trusted runtime descriptor, fenced invocation envelope, and redacted attestation. |
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
| Bootstrap rubric | PA-REQ-018 | none | A0, A6, A7 |
| Guideline and Agent invocation | PA-REQ-001–004 | ANC-001–002, ANC-009 | A1, A5, A6 |
| Dual plan sources and Markdown authority | PA-REQ-005–007 | ANC-015–016 | A2, A7 |
| Lightweight `bd`/`br` anchor store | PA-REQ-008–010 | ANC-017–018 | A3, A5, A6 |
| Environment and offline execution | PA-REQ-011–012 | ANC-005 | A4, A6 |
| Harness roles and independent tuning | PA-REQ-013–014, PA-REQ-019–026 | ANC-009–010, ANC-020–031 | A5, A6, A7 |
| Jev, redaction, examples, plugin boundary | PA-REQ-015–017 | ANC-011–014 | A4, A6, A7 |

## Phase acceptance

- `/plan-anchoring` against the phase file, its directory, and the `pa-sza`
  tracker copy discovers the same eight ordered sprint items.
- Markdown and tracker-copy materialization have identical normalized request
  bodies and digests at the Jev boundary; direct construction and leaf review
  agents reproduce them independently.
  Each source passes independently. Recorded-answer parity tests require
  identical verdicts, while differing live answers to identical bodies are
  classified as model instability and preserved rather than blamed on a source
  adapter.
- Each run records source kind, source identity/revision, and normalized digest;
  tracker-copy drift fails before judging.
- A repository with only Markdown plans can initialize `bd` or `br` solely for
  anchor/question records and complete capture, tuning, and review.
- Both `bd` and `br` fixture and installed-binary integration contracts pass.
- `TYPESAFE_API_KEY` is the only application-specific environment read; dry-run
  and fixture modes make zero transport calls.
- Claude and Codex registries, agent roles, schemas, manifests, and version
  declarations pass mechanical consistency validation.
- Claude and Codex register `anchor-tuning` as a dedicated Opus/Sol planner
  subagent; its plan-independent tuning and evidence-bound triage modes pass
  isolation tests, and its candidate calls go directly to Jev.
- Tuning mutations occur only in a disposable workspace, cover added ceremony
  and removed required content, and leave authoritative Markdown and tracker
  sources byte-identical.
- A named `<team>-anchor-tuning` subagent overlaps planner completion, emits sealed
  current-protocol question digests and byte-identical source-neutral tuning
  history for Markdown and tracker copies before leaf review, and routes every
  clarity-only authority recommendation through explicit user approval and
  affected-result invalidation. Tournament confidence uses `0.8` only as a
  ranking reference; production review remains fail-closed below its configured
  threshold (default `0.6`).
- Every planner-to-tuner review handoff is rendered from the checked-in
  `sc-compose` Jinja2 template. Triage cites INTENT/ANC and returns exactly
  `plan_violation` with an unchanged question digest or `question_defect` with
  an affected-only tournament restart; planner pressure can never select the
  latter disposition.
- Known sc-lint plan fixtures copied into disposable `bd` and `br` workspaces
  produce the same canonical requests as their Markdown source without changing
  sc-lint's live databases.
- Credential canaries remain absent from stdout, stderr, errors, reports,
  attestations, and run files.
- The independently calibrated testability rubric accepts every locked anchor;
  the independently tuned planning gate passes every sprint document and phase
  coverage contains no uncovered locked anchor.
- The existing offline test suite, new Phase A tests, documentation examples,
  version checks, and `git diff --check` all pass.

## Phase-wide non-closure

- Replacing Jev or changing plan/development verdict semantics and confidence
  policy outside their owning sprint; A0 owns testability-rubric confirmation
  and uncertainty semantics only.
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
| The planner pressures the tuner to make its plan pass | Treat planner commentary as untrusted template data; require a cited binary disposition and preserve the sealed question digest for every supported plan violation. |
| Free-form feedback changes tuner behavior | Render one checked-in Jinja2 template with `sc-compose --strict`, prohibit desired-verdict fields, and test the rendered instruction and result schema. |
| One source path is silently better than another | Compare exact outbound Jev bodies before verdicts, stop on drift, and retain a classified root-cause record instead of normalizing the difference away. |
| Diagnostic mutations become plan edits or adversarial scope creep | Distinguish normative intent/ANC inputs from non-normative plan corpus, mutate only hashed temporary copies, and use additions/removals solely to measure question discrimination. |
| Parallel tuning races changing authority | Version the INTENT/ANC packet, stop affected tournaments on a newer version, and resume only after the user approves or rejects the proposed clarification. |
| Bootstrap rubric rewrites anchors from sampling noise | Calibrate on a frozen external corpus, confirm semantic cells, and classify low confidence or disagreement as inconclusive/unstable. |

## Handoff after Phase A

Phase B may extend source profiles or development evidence only after Phase A's
Markdown source, tracker, invocation, and attestation contracts are stable and
the self-hosted planning gate has passed. Remaining findings become explicit
dependent tracker work; they are never carried silently in this phase plan.
