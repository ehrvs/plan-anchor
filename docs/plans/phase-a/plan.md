# Phase A plan: self-anchor the plan-anchor skill

Status: initial plan, ready for independent review

Intent: `docs/plans/phase-a/intent.md`

Anchors: `docs/plans/phase-a/anchors.json` and rendered `anchors.md`

Tracker epic: `pa-sza`

Architectural baseline: `/Users/randlee/Documents/github/synaptic-canvas/docs/claude-code-skills-agents-guidelines.md` v0.7

## 1. Objective

Phase A makes plan-anchor conform to the architecture it expects other skills
to follow. The result should be simpler than the current implementation at the
agent boundary: the skill resolves trusted artifacts and tracker capabilities
once, invokes a harness-specific agent with one structured parameter object,
and treats malformed inputs or outputs as boundary failures. Agents retain the
repository-input checks that protect evidence and run paths, but stop repeating
installation discovery and artifact attestation.

The phase also removes machine configuration that currently leaks into normal
operation. `TYPESAFE_API_KEY` remains the sole application-specific environment
variable. Everything else uses explicit command arguments or checked-in
defaults. A live command is explicit by the absence of `--dry-run`; it does not
require a second environment-variable opt-in.

Finally, the skill becomes tracker-neutral for the small operation set it uses.
It supports both Go/Dolt `bd` and Rust/SQLite `br` without pretending their
database formats are interchangeable.

## 2. Constraints carried from the anchors

The implementation must preserve all 14 locked anchors. The most important
cross-cutting constraints are:

- the guideline is the baseline, with the Agent-tool correction recorded as an
  explicit override;
- trust resolution occurs once at the orchestration boundary;
- every agent receives exactly one fenced JSON params object;
- params carry typed data and a tracker descriptor, not shell command strings;
- only `TYPESAFE_API_KEY` is read as plan-anchor application configuration;
- `--dry-run` and fixture-answer paths never call the network;
- `bd` and `br` expose the same normalized operations to the workflow;
- Claude and Codex keep separate definitions and model classes;
- tuning stays independent from the planner;
- Jev remains required for the normal workflow;
- secret redaction remains comprehensive;
- examples must be executable and current; and
- sc-lint's `arch-qa` and `req-qa` never enter this plugin.

## 3. Baseline audit against the guideline

### 3.1 Already conforming; preserve with regression checks

| Area | Evidence on merged `main` | Phase A treatment |
| --- | --- | --- |
| Harness separation | Three definitions exist in both `.claude/agents/` and `.codex/agents/` | Preserve and validate parity, not merge them |
| Model classes | Claude uses Sonnet for gates and Opus for tuning; Codex uses Luna and Sol | Add a mechanical model-role assertion |
| Frontmatter versions | All six agent files declare version `0.4.0` | Continue validating against each harness registry |
| Required sections | Every agent has Inputs, Output Format, Error Handling, and Constraints | Make the validator fail on omissions |
| Fenced responses | Agents specify fenced JSON responses and structured errors | Add parser tests at the runner boundary |
| External registries | Both harnesses have `registry.yaml` with skill dependencies | Make runtime resolution consume them |
| Version consistency | `scripts/check_version_sync.py` validates 35 release artifacts | Extend rather than replace it |
| Independent tuning | Opus/Sol tuner definitions already freeze an oracle independently | Preserve and add focused contract tests |
| Secret redaction | The script recursively redacts exact credentials and bearer forms | Keep canary tests over every output channel |
| Jev requirement | README and skill describe Jev as normal-workflow infrastructure | Retain while removing the redundant remote opt-in |

### 3.2 Gaps to correct

| Finding | Current behavior | Required outcome | Anchors |
| --- | --- | --- | --- |
| No orchestration runner contract | Registries exist, but the skill passes a script path in prose and agents establish artifact trust themselves | Resolve registry path, version, model, and SHA-256 once; launch through Agent with an immutable descriptor | ANC-001, ANC-003 |
| Repeated trust boilerplate | Every gate agent searches install locations and validates the script before doing work | Remove installation-path branching from agents; retain only repository-input validation | ANC-003 |
| Unstructured invocation | The skill's example is a natural-language sentence with named values | Supply one fenced JSON params object matching the agent Inputs contract | ANC-004 |
| Tracker coupling | Agents and references call `bd show`, `bd children`, and `bd comment` directly | Normalize the five needed operations for either `bd` or `br` | ANC-007, ANC-008 |
| Environment configuration | Script reads URL, model, threshold, size limits, confirmation behavior, remote opt-in, and user identity from environment | Keep only `TYPESAFE_API_KEY`; move all other choices to flags/defaults | ANC-005, ANC-006 |
| Redundant live opt-in | Live calls require both a key and `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE` or `--allow-remote` | A live command plus a valid key is sufficient; `--dry-run` is the explicit no-send mode | ANC-005, ANC-006 |
| Agent size and branching | Two gate agents exceed the guideline's 10 KB split-review threshold, largely from duplicated safety and shell instructions | Remove duplicated trust and tracker branches; split only if a definition remains multi-responsibility afterward | ANC-001, ANC-003 |
| Runtime attestation absent | CI validates versions, but invocation does not bind a resolved file hash | Emit a redacted attestation containing registry identity, version, model, hash, correlation ID, and outcome | ANC-001, ANC-003, ANC-012 |
| Examples drift with implementation | Examples assume `bd`, the old opt-in environment variable, and prose agent invocation | Test current `bd` and `br` examples plus fenced params examples | ANC-011, ANC-013 |

### 3.3 Explicit override to the guideline

The guideline still describes Task-tool launching. For this repository that text
is stale: Claude invokes agents using the Agent tool. Phase A must not copy Task
tool instructions into the skill, agents, examples, or validator. References to
the historical guideline wording may appear only in this documented override or
in a test proving active instructions do not use it.

## 4. Target architecture

```text
main session
  -> plan-anchoring skill
     -> resolve harness registry entry once
        {agent, path, version, model, sha256, harness}
     -> select active tracker once
        {kind: bd|br, binary, workspace}
     -> invoke harness Agent with one fenced params object
        {runtime, tracker, operation inputs, correlation_id}
     -> agent validates typed fields and repository-local inputs
     -> tracker adapter executes fixed argv for normalized operations
     -> jev_judge.py performs composition, judging, gating, and redaction
     -> runner validates one fenced JSON response and records attestation
```

### 4.1 Trust boundary

The skill is the runner for harness purposes because only the harness can invoke
the Agent tool. A small deterministic resolver may be implemented as a Python
helper, but it does not launch agents. It receives the plugin root, harness, and
registered agent name; it returns a descriptor only after:

1. locating the harness registry under that plugin root;
2. resolving a registry-relative path without traversal;
3. requiring a regular file inside the plugin root;
4. comparing registry and frontmatter name/version;
5. reading the declared model and comparing it with the role policy;
6. computing SHA-256; and
7. returning fenced JSON suitable for inclusion in params.

There is no PATH search for agent files and no fallback after a supplied plugin
root or registry entry fails. This logic runs once per invocation, not once in
each agent.

### 4.2 Structured invocation contract

Every invocation uses one JSON object with operation-specific fields. A planning
gate invocation has this conceptual shape:

```json
{
  "runtime": {
    "agent": "anchor-plan-review",
    "harness": "codex",
    "path": ".codex/agents/anchor-plan-review.md",
    "version": "0.5.0",
    "model": "luna",
    "sha256": "<64 lowercase hex characters>",
    "script": "skills/plan-anchoring/scripts/jev_judge.py"
  },
  "tracker": {
    "kind": "br",
    "binary": "/opt/homebrew/bin/br",
    "workspace": ".beads"
  },
  "operation": "plan_review",
  "bead_id": "pa-phase-a-runner-abc123",
  "anchor_ids": "all",
  "anchors_path": "docs/plans/phase-a/anchors.json",
  "run_dir": "docs/plans/phase-a/anchor-runs",
  "threshold": 0.6,
  "dry_run": false,
  "correlation_id": "pa-phase-a-runner-abc123"
}
```

The JSON contains data, not executable snippets. The runner and adapter create
argv arrays from allowlisted operations. Unknown fields, missing required fields,
wrong types, duplicate JSON blocks, unfenced input, unfenced output, or output
that violates the response envelope fail closed before another operation starts.

### 4.3 Repository-input safety

Central artifact trust does not remove input safety. `agent-preflight` continues
to canonicalize anchors, run directories, evidence, identifiers, and correlation
IDs against the Git workspace. Its responsibility narrows: it validates data
paths and identifiers, not how the installed agent or script was discovered.

Temporary directories come from a fixed platform API or `mktemp -d` without
constructing names from unvalidated input. No agent needs to inspect HOME,
CLAUDE_PLUGIN_ROOT, TMPDIR, or installation fallback directories.

### 4.4 Tracker interface

The adapter supports only operations the skill actually needs:

| Normalized operation | `bd` | `br` | Normalized output |
| --- | --- | --- | --- |
| `show(id)` | `bd show ID --json` | `br show ID --json` | one issue object |
| `children(id)` | `bd children ID --json` | `br dep list ID --direction up --type parent-child --format json`, then `br show` for the returned IDs | ordered issue array |
| `create(fields)` | `bd create ...` | `br create ...` | created issue ID |
| `update(id, fields)` | `bd update ...` | `br update ...` | updated issue identity/status |
| `comment(id, file)` | `bd comment ID --file FILE` | `br comments add ID --file FILE` | comment receipt |

Selection occurs once. An explicit tracker choice wins. Otherwise the skill
probes repository-local workspaces with read-only `where`/capability calls and
selects the single valid implementation. If both or neither are valid, it
returns a typed ambiguity or prerequisite error instead of guessing. The binary
path is canonicalized once and passed in the tracker descriptor.

The adapter accepts typed fields and uses `subprocess` argv lists with no shell.
It normalizes JSON envelopes but does not translate or migrate storage. Fixture
contracts cover both tools, and optional integration tests run when the relevant
binary is installed.

### 4.5 Configuration and network behavior

The script removes reads of:

- `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE`
- `PLAN_ANCHOR_JEV_URL`
- `PLAN_ANCHOR_JEV_MODEL`
- `PLAN_ANCHOR_CONFIDENCE_THRESHOLD`
- `PLAN_ANCHOR_MAX_ITEM_CHARS`
- `PLAN_ANCHOR_MAX_CODE_LINES`
- `PLAN_ANCHOR_CONFIRM_NEAR`
- `USER` as an author default

Equivalent explicit flags and current checked-in defaults remain. The endpoint
gets a clearly named CLI flag intended for testing and controlled proxies. A
normal live invocation requires `TYPESAFE_API_KEY`; a dry run and fixture-answer
execution require no key and instantiate no network transport. `--allow-remote`
is removed because it duplicates the live-versus-dry-run choice.

## 5. Sprint plan

### Sprint A1 — Runner contract and single trust resolution (`pa-sza.1`)

Purpose: establish the orchestration boundary every later sprint consumes.

Deliverables:

- a deterministic resolver for Claude and Codex registries;
- validation of relative paths, regular files, names, versions, role models,
  plugin-root confinement, and SHA-256;
- one runtime descriptor schema shared by the three operations;
- runner instructions that invoke Claude/Codex through Agent with one fenced
  params object;
- response parsing that rejects unfenced, duplicated, or malformed JSON;
- a redacted invocation attestation schema and atomic writer; and
- unit tests for traversal, symlink escape, mismatched version/model, modified
  file hash, malformed params, timeout, and malformed result.

Acceptance:

- registry/path/version/model/hash resolution occurs once per invocation;
- no agent definition performs installation-path fallback or frontmatter
  version validation;
- the Agent-tool override is explicit and no active Task-tool instruction
  remains; and
- resolver output and audit data contain no credentials or arbitrary command
  strings.

Anchors: ANC-001, ANC-002, ANC-003, ANC-004, ANC-008, ANC-012.

### Sprint A2 — Tracker-neutral `bd` and `br` operations (`pa-sza.2`)

Purpose: remove direct tracker branching from agents and documentation.

Deliverables:

- a small tracker adapter with `show`, `children`, `create`, `update`, and
  `comment` operations;
- selection and ambiguity rules at the orchestration boundary;
- normalization for `bd` arrays and `br` object/envelope shapes;
- capability/version checks and typed errors for unsupported releases;
- fixture suites for both trackers and integration tests guarded by binary
  availability; and
- Phase A's own `br` workflow as the first real repository fixture.

Acceptance:

- the same normalized contract passes for both tracker fixtures;
- no agent contains `bd children` or `br list --parent` branching;
- shell command strings supplied through params are rejected; and
- `br ready --exclude-label anchor --json` exposes only executable Phase A
  sprint work, not anchor-question records.

Anchors: ANC-004, ANC-007, ANC-008, ANC-013.

Dependencies: Sprint A1.

### Sprint A3 — Environment-variable reduction and explicit offline mode (`pa-sza.3`)

Purpose: make installation portable and live behavior obvious from the command.

Deliverables:

- remove every plan-anchor environment read except `TYPESAFE_API_KEY`;
- remove the remote-judge opt-in environment variable and `--allow-remote`;
- retain or add explicit endpoint, model, threshold, size, confirmation, and
  author flags with documented defaults;
- centralize API-key validation at live transport creation;
- prove dry-run and fixture-answer execution never constructs or calls the
  network transport; and
- migrate tests without using application environment variables for ordinary
  configuration.

Acceptance:

- a static test finds exactly one application-specific environment read;
- live execution without a key fails with `AUTH.CREDENTIALS` before transport;
- live execution with a key needs no second opt-in;
- dry-run and fixtures work with no key and zero transport calls; and
- help, errors, README, skill, and Jev reference contain no removed variable.

Anchors: ANC-005, ANC-006, ANC-011, ANC-012.

Dependencies: Sprint A1.

### Sprint A4 — Simplify harness-specific agents (`pa-sza.4`)

Purpose: reduce agent branching after runner and tracker responsibilities move
to their correct boundary.

Deliverables:

- update all six agent definitions to accept the fenced params contract;
- replace `script` and installation-search inputs with the immutable runtime
  descriptor;
- replace direct tracker commands with normalized adapter calls;
- retain focused workspace preflight, one-operation responsibility, typed
  errors, timeout semantics, and fenced JSON responses;
- keep separate Claude/Codex files and role models; and
- assess final file sizes, splitting an agent only if it still has multiple
  responsibilities rather than splitting solely to meet a byte target.

Acceptance:

- every registered agent passes the required-section and schema checks;
- the plan and sprint gate definitions contain no duplicated trust bootstrap;
- the tuner remains isolated from planner objectives and current verdicts;
- harness registries and plugin manifests remain in parity; and
- no sc-lint agent appears in this plugin.

Anchors: ANC-001, ANC-003, ANC-004, ANC-009, ANC-010, ANC-014.

Dependencies: Sprints A1 and A2.

### Sprint A5 — Mechanical compliance and regression gates (`pa-sza.5`)

Purpose: turn the guideline and locked invariants into executable checks.

Deliverables:

- extend release validation to check frontmatter, required sections, registry
  parity, model roles, skill dependencies, and manifest registration;
- enforce Agent-tool wording and reject active Task-tool instructions;
- enforce the environment-variable allowlist;
- validate structured invocation examples and response envelopes;
- add credential canaries covering stdout, stderr, nested errors, reports,
  attestation, and run files;
- add tracker fixture and command-injection tests; and
- keep existing judge, coverage, diff, shape, and redaction suites green.

Acceptance:

- each locked deterministic check has a corresponding executable assertion;
- negative fixtures fail for the intended reason;
- `scripts/check_version_sync.py` and the offline test suite pass on a clean
  checkout; and
- CI fails on a deliberately unfenced output, wrong model, forbidden env read,
  Task-tool instruction, raw secret, or direct tracker branch in an agent.

Anchors: all, with emphasis on ANC-001, ANC-002, ANC-004, ANC-005, ANC-006,
ANC-009, ANC-012, and ANC-014.

Dependencies: Sprints A2, A3, and A4.

### Sprint A6 — Documentation, examples, and self-gate (`pa-sza.6`)

Purpose: make the public contract match the shipped behavior and demonstrate
that plan-anchor can gate its own plan.

Deliverables:

- update README, SKILL.md, installation/troubleshooting, Jev API, bead layout,
  planning/development gate references, PRD, and architecture diagrams;
- document both trackers without implying database compatibility;
- replace environment-variable and prose-invocation examples;
- provide executable `bd` and `br` examples using repository-valid paths and
  current JSON shapes;
- render `anchors.md` from the record and keep issue IDs linked;
- run independent question tuning after explicit authorization for the scoped
  Jev payload; and
- run the planning gate, triage real failures, and record coverage and diffs.

Acceptance:

- documentation consistency and example tests pass;
- Jev is clearly required for the normal workflow;
- offline modes are described accurately as development/CI aids;
- latest planning runs pass every locked anchor and coverage has no uncovered
  anchor; and
- any plan growth that fixed a failure cites a pre-existing locked anchor.

Anchors: ANC-001, ANC-004, ANC-007, ANC-009, ANC-010, ANC-011, ANC-013,
ANC-014.

Dependencies: Sprint A5.

## 6. Dependency graph

```text
A1 runner contract
├── A2 tracker neutrality
├── A3 environment reduction
└── A4 agent simplification (also depends on A2)

A2 + A3 + A4
└── A5 mechanical compliance
    └── A6 documentation and self-gate
```

Executable dependency edges in `br` are the source of truth. Parent-child edges
place every sprint under the Phase A epic; blocking edges enforce the graph
above.

## 7. Verification strategy

### Offline, required on every sprint

- Python unit tests for judge and new resolver/adapter modules;
- static validation for environment reads, Task-tool instructions, required
  sections, registries, models, and manifests;
- `br` and `bd` JSON fixture contract tests;
- example execution in temporary repositories;
- secret-canary scan of all observable and persisted outputs;
- `jev_judge.py lint`, `validate`, `render`, and dry-run; and
- `git diff --check` plus release-version consistency.

### Live, required before Phase A implementation acceptance

Live Jev work is deliberately separate from ordinary tests. After the user
authorizes sending the scoped intent, anchor, fixtures, and individual sprint
text to TypeSafe:

1. the independent Opus/Sol tuner freezes an oracle for each non-structural
   anchor and gate;
2. the tuner records accepted question overrides and evidence;
3. each sprint is judged separately at the planning gate;
4. failures are triaged to plan, anchor, question, or Jev error;
5. only the owning defect is changed, with cuts preferred over additions;
6. affected sprints are re-run and diffed; and
7. coverage is recomputed from run files.

No live Jev request is part of creating this initial plan or database.

## 8. Rollout and compatibility

- Treat removal of legacy environment configuration and direct `bd` contracts
  as a minor-version feature with a clear changelog entry.
- Keep anchor-record `beads` field names for schema compatibility in Phase A;
  documentation may describe them as tracker issue references. A schema rename
  requires a separate migration decision.
- Preserve existing run-file schema unless the attestation reference needs an
  additive optional field.
- Reject ambiguous tracker selection rather than silently changing storage.
- Do not migrate a repository between `bd` and `br` inside plan-anchor.

## 9. Review rounds

This is the initial grounded plan. Independent review should proceed until the
diff reaches steady state:

1. architecture and trust-boundary review;
2. security, secret, and command-injection review;
3. tracker-contract and migration-risk review;
4. documentation and operator-experience review; and
5. final anchor coverage review.

Each review finding becomes an update to an existing sprint or a new dependent
sprint in `br`; it does not become an untracked markdown TODO.
