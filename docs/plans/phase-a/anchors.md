# Anchors - phase-a

Constraints captured during planning. Each anchor is a testable statement written by the orchestrator and approved by the user; the user's verbatim words are kept beneath it as provenance. Every anchor is judged at the planning gate and again at the development gate. Edit `anchors.json`, not this file; this file is rendered.

Intent: `docs/plans/phase-a/intent.md`

| ID | Status | Summary | Stated |
| --- | --- | --- | --- |
| ANC-001 | locked | Guideline baseline | 2026-10-10 |
| ANC-002 | locked | Agent tool only | 2026-10-10 |
| ANC-003 | retired | Resolve agent trust once | 2026-10-10 |
| ANC-004 | retired | Structured agent params | 2026-10-10 |
| ANC-005 | locked | Only API-key environment variable | 2026-10-10 |
| ANC-006 | retired | Offline modes never send | 2026-10-10 |
| ANC-007 | retired | Support bd and br | 2026-10-10 |
| ANC-008 | retired | No shell commands in params | 2026-10-10 |
| ANC-009 | locked | Harness-specific agents | 2026-10-10 |
| ANC-010 | locked | Independent question tuning | 2026-10-10 |
| ANC-011 | locked | Jev remains required | 2026-10-10 |
| ANC-012 | locked | Secrets stay redacted | 2026-10-10 |
| ANC-013 | locked | Realistic examples | 2026-10-10 |
| ANC-014 | locked | Exclude sc-lint agents | 2026-10-10 |
| ANC-015 | locked | Authoritative sprint documents | 2026-10-10 |
| ANC-016 | locked | Dual plan sources | 2026-10-10 |
| ANC-017 | locked | Beads only stores anchors | 2026-10-10 |
| ANC-018 | locked | Fast br anchor-store setup | 2026-10-10 |

## ANC-001

Anchor: claude-code-skills-agents-guidelines.md is the governing architecture baseline for plan-anchor.

> these guidelines are my expected baseline.  I feel like we need to apply plan-anchoring to the plan-anchor skill

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Guideline baseline

Scope: edits the skill, an agent definition, an agent registry, an invocation runner, or plugin orchestration

Deterministic check to pair with the development gate: Run the Phase A compliance validator against the guideline-derived rules and the documented override list.

Beads: anchor `pa-jvb`, plan questions `pa-jvb.1`, dev questions `pa-jvb.2`

Fixtures:
- pass: The Phase A change follows every applicable guideline rule and records the Agent-tool override in the locked anchors.
- fail: The change ignores the guideline because the current implementation already works.

## ANC-002

Anchor: Claude plan-anchor workflows must invoke subagents with the Agent tool.

> yes, the Task tool has been superceeded w/ Agent tool

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Agent tool only

Scope: edits Claude delegation instructions, invocation examples, agent manifests, or orchestration tests

Deterministic check to pair with the development gate: Repository validation finds Agent-tool invocation and no active instruction that invokes the Task tool.

Beads: anchor `pa-fwo`, plan questions `pa-fwo.1`, dev questions `pa-fwo.2`

Fixtures:
- pass: Claude invokes anchor-plan-review through the Agent tool.
- fail: Claude invokes anchor-plan-review through the Task tool.

## ANC-003

Anchor: The plan-anchor orchestration boundary must perform agent trust resolution once per invocation.

> why does every agent need to do this?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: retired. Version 4.

Summary: Resolve agent trust once

Scope: adds or changes agent resolution, registry validation, runtime attestation, or an agent preflight step

Deterministic check to pair with the development gate: Runner tests prove one resolution per invocation and agent definitions contain no install-path fallback search.

Beads: anchor `pa-rxx`, plan questions `pa-rxx.1`, dev questions `pa-rxx.2`

Fixtures:
- pass: The runner resolves the registered agent path, version, model, and hash once before launching it.
- fail: Each agent searches several installation paths and validates its own version before starting.

## ANC-004

Anchor: Each plan-anchor agent invocation must receive one fenced JSON input object.

> is the agent getting passed fenced json input?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: retired. Version 4.

Summary: Structured agent params

Scope: edits any Claude or Codex agent invocation example, runner payload, or agent Inputs contract

Deterministic check to pair with the development gate: A contract test parses exactly one fenced JSON input object for every registered agent and rejects missing required fields.

Beads: anchor `pa-0rb`, plan questions `pa-0rb.1`, dev questions `pa-0rb.2`

Fixtures:
- pass: The invocation contains one fenced JSON params object matching the registered agent input schema.
- fail: The invocation describes script, tracker, and item values as unstructured prose.

## ANC-005

Anchor: Plan-anchor must not read runtime configuration from environment variables other than TYPESAFE_API_KEY.

> My preference would be no environment variables are used outside of typesafe api key

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Only API-key environment variable

Scope: adds or changes configuration, command-line flags, defaults, installation instructions, or environment reads

Deterministic check to pair with the development gate: Static validation finds no plan-anchor-owned environment read other than TYPESAFE_API_KEY.

Beads: anchor `pa-j8m`, plan questions `pa-j8m.1`, dev questions `pa-j8m.2`

Fixtures:
- pass: The script reads TYPESAFE_API_KEY and receives model, endpoint, threshold, and limits through CLI arguments or defaults.
- fail: Users must export PLAN_ANCHOR_ALLOW_REMOTE_JUDGE and PLAN_ANCHOR_JEV_MODEL before running a gate.

## ANC-006

Anchor: Plan-anchor --dry-run execution must make zero network calls.

> yes, --dry-run is an arg that does the same thing and can be used in unit tests

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: retired. Version 4.

Summary: Offline modes never send

Scope: changes dry-run, fixture-answer, transport, rubric, tuning, or gate execution

Deterministic check to pair with the development gate: Unit tests fail if any transport is called during --dry-run or fixture-answer execution.

Beads: anchor `pa-dyx`, plan questions `pa-dyx.1`, dev questions `pa-dyx.2`

Fixtures:
- pass: The dry-run and fixture-answer tests use a transport spy that observes zero requests.
- fail: Dry-run validates the request and then sends it to Jev.

## ANC-007

Anchor: The plan-anchoring skill must support both bd and br.

> how large of a change would it be to make this skill work w/ bd and br ?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: retired. Version 4.

Summary: Support bd and br

Scope: reads, creates, updates, lists children of, or comments on tracker issues

Deterministic check to pair with the development gate: Contract tests run the same normalized show, children, create, update, and comment cases against bd and br fixtures.

Beads: anchor `pa-dyw`, plan questions `pa-dyw.1`, dev questions `pa-dyw.2`

Fixtures:
- pass: The tracker layer selects br and normalizes show, children, create, update, and comment results.
- fail: The planning agent calls bd children directly and fails in a br repository.

## ANC-008

Anchor: Plan-anchor agent inputs must carry tracker operation data rather than shell command strings.

> so the bd/br commands would be passed in the fenced json?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: retired. Version 4.

Summary: No shell commands in params

Scope: edits tracker selection, agent params, runner payloads, or tracker command construction

Deterministic check to pair with the development gate: Input-schema tests reject command-string fields and adapter tests construct argv from validated operation data.

Beads: anchor `pa-08k`, plan questions `pa-08k.1`, dev questions `pa-08k.2`

Fixtures:
- pass: Params identify tracker br and issue pa-123 while the trusted adapter constructs the argv list.
- fail: Params contain the interpolated command string br show pa-123 | jq .

## ANC-009

Anchor: Each plan-anchor agent definition must reside in its harness’s agent directory: .claude/agents or .codex/agents.

> I think we should have separate agents for codex and claude (in .codex/.claude folders so agent class sonnet/luna are specified per harness).

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 6.

Summary: Harness-specific agents

Scope: adds or changes an agent definition, registry entry, plugin manifest, or model assignment

Deterministic check to pair with the development gate: Repository validation proves every Claude agent definition resides under .claude/agents and every Codex agent definition resides under .codex/agents.

Beads: anchor `pa-nyp`, plan questions `pa-nyp.1`, dev questions `pa-nyp.2`

Fixtures:
- pass: Claude definitions live under .claude/agents while Codex definitions live under .codex/agents.
- fail: Both harnesses load one shared agent definition outside their harness agent directories.

## ANC-010

Anchor: Question tuning must be performed by an evaluator independent from the planner.

> My feeling is that tuning should be done w/ an agent independent from the planner.  this should probably be a higher level agent i.e. opus or sol which has the responsibility for tuning against the intent/anchors w/out regard for 'getting the plan to pass'.  i.e. the tuning agent should loop over jev calls while modifying the question text and verifying the answers align with intent/anchors.  the tuning agent must exercise judgement..

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Independent question tuning

Scope: changes question-tuning prompts, oracle construction, fixtures, override acceptance, or tuner model selection

Deterministic check to pair with the development gate: Tuner contract tests prove the oracle is fixed before Jev answers and current plan verdicts are absent from tuning inputs.

Beads: anchor `pa-waz`, plan questions `pa-waz.1`, dev questions `pa-waz.2`

Fixtures:
- pass: The tuner freezes its oracle from approved intent and fixtures before the first Jev answer and never receives the current plan verdict.
- fail: The planner rewrites questions until the currently failing bead passes.

## ANC-011

Anchor: The normal plan-anchoring workflow must require Jev.

> fix README and make sure documents are consistent (this skill requires jev)

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Jev remains required

Scope: edits README, SKILL.md, installation guidance, examples, or marketplace descriptions

Deterministic check to pair with the development gate: Documentation consistency validation finds the required-workflow statement and no claim that offline modes replace Jev.

Beads: anchor `pa-nwu`, plan questions `pa-nwu.1`, dev questions `pa-nwu.2`

Fixtures:
- pass: The README states that Jev is required for normal capture, tuning, and gate execution and labels offline modes as development aids.
- fail: The README presents dry-run as a complete replacement for Jev.

## ANC-012

Anchor: Plan-anchor script output must redact the TypeSafe API-key value.

> p2 - redact api key from script output

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Secrets stay redacted

Scope: changes transport errors, structured output, logging, reports, audit records, or run-file persistence

Deterministic check to pair with the development gate: Secret-canary tests scan stdout, stderr, errors, reports, audits, and run files for raw credential and authorization-header variants.

Beads: anchor `pa-buf`, plan questions `pa-buf.1`, dev questions `pa-buf.2`

Fixtures:
- pass: A transport failure returns a redacted credential marker and no run artifact contains the supplied secret.
- fail: A structured error echoes the supplied API key in its suggested action.

## ANC-013

Anchor: Plan-anchor examples must be executable using repository-valid paths, supported commands, and supported JSON schemas.

> p3 - update examples to be realistic

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 4.

Summary: Realistic examples

Scope: adds or changes README examples, reference snippets, fixtures, sample anchors, or agent invocation examples

Deterministic check to pair with the development gate: Example tests execute commands in a fixture repository and validate documented JSON against current schemas.

Beads: anchor `pa-2td`, plan questions `pa-2td.1`, dev questions `pa-2td.2`

Fixtures:
- pass: The br example uses docs/plans/phase-a, current flags, and the documented br JSON envelope.
- fail: The example uses an invented path, removed flag, and JSON shape no supported tracker emits.

## ANC-014

Anchor: The plan-anchor plugin must not define or invoke arch-qa or req-qa.

> where did arch-qa and req-qa come from?  these are agents on sc-lint, not part of this skill

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 5.

Summary: Exclude sc-lint agents

Scope: edits plan-anchor agent files, registries, manifests, skill delegation, or examples

Deterministic check to pair with the development gate: Repository search finds no arch-qa or req-qa reference under the plan-anchor plugin.

Beads: anchor `pa-9wl`, plan questions `pa-9wl.1`, dev questions `pa-9wl.2`

Fixtures:
- pass: The plan-anchor registries list only anchor-plan-review, anchor-sprint-review, and anchor-question-tune.
- fail: The plan-anchor skill delegates requirement review to the sc-lint req-qa agent.

## ANC-015

Anchor: The Phase A index must link separate authoritative sprint-plan documents.

> I always break a plan into sprints.  see. /Users/randlee/github/raptor/docs/plans/phase-a/* for raptor project.  there is also a plan-hardening skill in that repo which has sprint-plan-guidelines for building your sprint

Said by randlee, plan-anchor Phase A dogfood correction; live rubric pending explicit TypeSafe payload approval, 2026-10-10. Status: locked. Version 6.

Summary: Authoritative sprint documents

Scope: creates or reviews a phase plan, sprint plan, phase index, or planning source

Deterministic check to pair with the development gate: Validate the phase index links separate sprint Markdown files and each sprint has one authoritative deliverables, acceptance, validation, and non-closure section.

Beads: anchor `pa-2zo`, plan questions `pa-2zo.1`, dev questions `pa-2zo.2`

Fixtures:
- pass: The phase index links eight separate sprint documents, each with authoritative deliverables, acceptance criteria, validation, and non-closure.
- fail: The phase plan keeps all sprint work as subsections in one monolithic Markdown file.

## ANC-016

Anchor: The plan-anchoring gate must accept both a Markdown plan and its copy in a br database.

> You should be able to run the /plan-anchor skill both against the md plan and against a copy of the plan in br database

Said by randlee, plan-anchor Phase A dogfood correction; live rubric pending explicit TypeSafe payload approval, 2026-10-10. Status: locked. Version 6.

Summary: Dual plan sources

Scope: changes plan-source selection, sprint discovery, item composition, source digests, planning-gate invocation, or source parity tests

Deterministic check to pair with the development gate: Materialize the Phase A Markdown sprints and their br copies, assert identical ordered request digests, require both recorded-answer parity and independent live passing results, and classify differing live answers as model instability.

Beads: anchor `pa-bxu`, plan questions `pa-bxu.1`, dev questions `pa-bxu.2`

Fixtures:
- pass: The Markdown and br-copy adapters normalize Sprint A2 to the same request digest, pass independently, and reserve exact verdict equality for recorded-answer parity.
- fail: The skill can review only tracker issue bodies and rejects the equivalent Markdown sprint file.

## ANC-017

Anchor: Markdown plan review requires tracker records only for an anchor root and its plan-question and dev-question children.

> at that point the only beads dependency in the plan is for holding the anchoring info and questions which can be spun up in a br database quickly for any repo

Said by randlee, plan-anchor Phase A dogfood correction; live rubric pending explicit TypeSafe payload approval, 2026-10-10. Status: locked. Version 7.

Summary: Beads only stores anchors

Scope: changes tracker prerequisites, anchor storage, question storage, Markdown plan review, or required issue layout

Deterministic check to pair with the development gate: Complete Markdown-source dry-run review in a repository whose tracker contains only anchor roots with plan-question and dev-question children.

Beads: anchor `pa-885`, plan questions `pa-885.1`, dev questions `pa-885.2`

Fixtures:
- pass: Markdown review reads plan text from sprint files and uses br only for each anchor's question tree.
- fail: Markdown review requires the phase and every sprint to exist as br issues before it can run.

## ANC-018

Anchor: The skill must document br initialization with no prerequisite beyond a local Git repository.

> at that point the only beads dependency in the plan is for holding the anchoring info and questions which can be spun up in a br database quickly for any repo

Said by randlee, plan-anchor Phase A dogfood correction; live rubric pending explicit TypeSafe payload approval, 2026-10-10. Status: locked. Version 6.

Summary: Fast br anchor-store setup

Scope: changes br installation, local initialization prerequisites, command examples, or onboarding

Deterministic check to pair with the development gate: Run the documented br initialization sequence in a temporary local Git repository without a remote service or phase epic.

Beads: anchor `pa-c3t`, plan questions `pa-c3t.1`, dev questions `pa-c3t.2`

Fixtures:
- pass: In any local Git repository, the documented br initialization commands work without a remote tracker service or a phase epic.
- fail: Before br can initialize, every repository must connect to a shared tracker service and create a phase epic.
