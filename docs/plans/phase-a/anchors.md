# Anchors - phase-a

Constraints captured during planning. Each anchor is a testable statement written by the orchestrator and approved by the user; the user's verbatim words are kept beneath it as provenance. Every anchor is judged at the planning gate and again at the development gate. Edit `anchors.json`, not this file; this file is rendered.

Intent: `docs/plans/phase-a/intent.md`

| ID | Status | Summary | Stated |
| --- | --- | --- | --- |
| ANC-001 | locked | Guideline baseline | 2026-10-10 |
| ANC-002 | locked | Agent tool only | 2026-10-10 |
| ANC-003 | locked | Resolve agent trust once | 2026-10-10 |
| ANC-004 | locked | Structured agent params | 2026-10-10 |
| ANC-005 | locked | Only API-key environment variable | 2026-10-10 |
| ANC-006 | locked | Offline modes never send | 2026-10-10 |
| ANC-007 | locked | Support bd and br | 2026-10-10 |
| ANC-008 | locked | No shell commands in params | 2026-10-10 |
| ANC-009 | locked | Harness-specific agents | 2026-10-10 |
| ANC-010 | locked | Independent question tuning | 2026-10-10 |
| ANC-011 | locked | Jev remains required | 2026-10-10 |
| ANC-012 | locked | Secrets stay redacted | 2026-10-10 |
| ANC-013 | locked | Realistic examples | 2026-10-10 |
| ANC-014 | locked | Exclude sc-lint agents | 2026-10-10 |

## ANC-001

Anchor: The plan-anchoring skill and its harness-specific agents must conform to claude-code-skills-agents-guidelines.md except where a locked anchor records a user-approved override.

> these guidelines are my expected baseline.

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Guideline baseline

Scope: edits the skill, an agent definition, an agent registry, an invocation runner, or plugin orchestration

Deterministic check to pair with the development gate: Run the Phase A compliance validator against the guideline-derived rules and the documented override list.

Beads: anchor `pa-jvb`, plan questions `pa-jvb.1`, dev questions `pa-jvb.2`

Fixtures:
- pass: The Phase A change follows every applicable guideline rule and records the Agent-tool override in the locked anchors.
- fail: The change ignores the guideline because the current implementation already works.

## ANC-002

Anchor: Claude plan-anchor workflows must invoke subagents with the Agent tool and contain no instruction to invoke the superseded Task tool.

> yes, the Task tool has been superceeded w/ Agent tool

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Agent tool only

Scope: edits Claude delegation instructions, invocation examples, agent manifests, or orchestration tests

Deterministic check to pair with the development gate: Repository validation finds Agent-tool invocation and no active instruction that invokes the Task tool.

Beads: anchor `pa-fwo`, plan questions `pa-fwo.1`, dev questions `pa-fwo.2`

Fixtures:
- pass: Claude invokes anchor-plan-review through the Agent tool.
- fail: Claude invokes anchor-plan-review through the Task tool.

## ANC-003

Anchor: The orchestration boundary must resolve each agent's registry entry, canonical path, version, model, and SHA-256 once and pass an immutable runtime descriptor to the agent.

> why does every agent need to do this?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Resolve agent trust once

Scope: adds or changes agent resolution, registry validation, runtime attestation, or an agent preflight step

Deterministic check to pair with the development gate: Runner tests prove one resolution per invocation and agent definitions contain no install-path fallback search.

Beads: anchor `pa-rxx`, plan questions `pa-rxx.1`, dev questions `pa-rxx.2`

Fixtures:
- pass: The runner resolves the registered agent path, version, model, and hash once before launching it.
- fail: Each agent searches several installation paths and validates its own version before starting.

## ANC-004

Anchor: Each agent invocation must supply exactly one fenced JSON params object whose fields match the agent's documented Inputs contract.

> is the agent getting passed fenced json input?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Structured agent params

Scope: edits any Claude or Codex agent invocation example, runner payload, or agent Inputs contract

Deterministic check to pair with the development gate: A contract test parses exactly one fenced JSON input object for every registered agent and rejects missing required fields.

Beads: anchor `pa-0rb`, plan questions `pa-0rb.1`, dev questions `pa-0rb.2`

Fixtures:
- pass: The invocation contains one fenced JSON params object matching the registered agent input schema.
- fail: The invocation describes script, tracker, and item values as unstructured prose.

## ANC-005

Anchor: Plan-anchor must read no application-specific environment variable except TYPESAFE_API_KEY.

> My preference would be no environment variables are used outside of typesafe api key

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Only API-key environment variable

Scope: adds or changes configuration, command-line flags, defaults, installation instructions, or environment reads

Deterministic check to pair with the development gate: Static validation finds no plan-anchor-owned environment read other than TYPESAFE_API_KEY.

Beads: anchor `pa-j8m`, plan questions `pa-j8m.1`, dev questions `pa-j8m.2`

Fixtures:
- pass: The script reads TYPESAFE_API_KEY and receives model, endpoint, threshold, and limits through CLI arguments or defaults.
- fail: Users must export PLAN_ANCHOR_ALLOW_REMOTE_JUDGE and PLAN_ANCHOR_JEV_MODEL before running a gate.

## ANC-006

Anchor: --dry-run and fixture-answer execution must make zero network calls, proven by transport-spy unit tests.

> yes, --dry-run is an arg that does the same thing and can be used in unit tests

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Offline modes never send

Scope: changes dry-run, fixture-answer, transport, rubric, tuning, or gate execution

Deterministic check to pair with the development gate: Unit tests fail if any transport is called during --dry-run or fixture-answer execution.

Beads: anchor `pa-dyx`, plan questions `pa-dyx.1`, dev questions `pa-dyx.2`

Fixtures:
- pass: The dry-run and fixture-answer tests use a transport spy that observes zero requests.
- fail: Dry-run validates the request and then sends it to Jev.

## ANC-007

Anchor: The skill must support both bd and br through tracker-neutral operations after selecting one installed tracker at the orchestration boundary.

> how large of a change would it be to make this skill work w/ bd and br ?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Support bd and br

Scope: reads, creates, updates, lists children of, or comments on tracker issues

Deterministic check to pair with the development gate: Contract tests run the same normalized show, children, create, update, and comment cases against bd and br fixtures.

Beads: anchor `pa-dyw`, plan questions `pa-dyw.1`, dev questions `pa-dyw.2`

Fixtures:
- pass: The tracker layer selects br and normalizes show, children, create, update, and comment results.
- fail: The planning agent calls bd children directly and fails in a br repository.

## ANC-008

Anchor: Agent params must omit interpolated shell command strings, carrying a tracker descriptor and operation data instead.

> so the bd/br commands would be passed in the fenced json?

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: No shell commands in params

Scope: edits tracker selection, agent params, runner payloads, or tracker command construction

Deterministic check to pair with the development gate: Input-schema tests reject command-string fields and adapter tests construct argv from validated operation data.

Beads: anchor `pa-08k`, plan questions `pa-08k.1`, dev questions `pa-08k.2`

Fixtures:
- pass: Params identify tracker br and issue pa-123 while the trusted adapter constructs the argv list.
- fail: Params contain the interpolated command string br show pa-123 | jq .

## ANC-009

Anchor: Harness-specific agent definitions are separate under .claude/agents and .codex/agents, declaring Sonnet/Opus for Claude and Luna/Sol for Codex.

> I think we should have separate agents for codex and claude (in .codex/.claude folders so agent class sonnet/luna are specified per harness).

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Harness-specific agents

Scope: adds or changes an agent definition, registry entry, plugin manifest, or model assignment

Deterministic check to pair with the development gate: Version-sync validation proves registry parity and the expected Sonnet/Opus and Luna/Sol role assignments.

Beads: anchor `pa-nyp`, plan questions `pa-nyp.1`, dev questions `pa-nyp.2`

Fixtures:
- pass: Claude definitions live under .claude/agents with Sonnet and Opus roles while Codex definitions live under .codex/agents with Luna and Sol roles.
- fail: Both harnesses load one shared agent file with an unspecified model.

## ANC-010

Anchor: Question tuning must run in an evaluator independent from the planner, freeze an oracle from approved intent and anchors, and ignore whether the current plan passes.

> tuning should be done w/ an agent independent from the planner.

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Independent question tuning

Scope: changes question-tuning prompts, oracle construction, fixtures, override acceptance, or tuner model selection

Deterministic check to pair with the development gate: Tuner contract tests prove the oracle is fixed before Jev answers and current plan verdicts are absent from tuning inputs.

Beads: anchor `pa-waz`, plan questions `pa-waz.1`, dev questions `pa-waz.2`

Fixtures:
- pass: The tuner freezes its oracle from approved intent and fixtures before the first Jev answer and never receives the current plan verdict.
- fail: The planner rewrites questions until the currently failing bead passes.

## ANC-011

Anchor: Documentation must identify Jev as required for the normal workflow and describe dry-run and fixture modes as development and CI aids.

> fix README and make sure documents are consistent (this skill requires jev)

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Jev remains required

Scope: edits README, SKILL.md, installation guidance, examples, or marketplace descriptions

Deterministic check to pair with the development gate: Documentation consistency validation finds the required-workflow statement and no claim that offline modes replace Jev.

Beads: anchor `pa-nwu`, plan questions `pa-nwu.1`, dev questions `pa-nwu.2`

Fixtures:
- pass: The README states that Jev is required for normal capture, tuning, and gate execution and labels offline modes as development aids.
- fail: The README presents dry-run as a complete replacement for Jev.

## ANC-012

Anchor: All script outputs and persisted run data must redact the TypeSafe API key and bearer-token forms before emission.

> the code-redaction change is a real issue flint fixed.

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Secrets stay redacted

Scope: changes transport errors, structured output, logging, reports, audit records, or run-file persistence

Deterministic check to pair with the development gate: Secret-canary tests scan stdout, stderr, errors, reports, audits, and run files for raw credential and authorization-header variants.

Beads: anchor `pa-buf`, plan questions `pa-buf.1`, dev questions `pa-buf.2`

Fixtures:
- pass: A transport failure returns a redacted credential marker and no run artifact contains the supplied secret.
- fail: A structured error echoes the supplied API key in its suggested action.

## ANC-013

Anchor: Examples must use repository-valid paths, current command syntax, and JSON shapes emitted by supported tracker and harness versions.

> p3 - update examples to be realistic

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Realistic examples

Scope: adds or changes README examples, reference snippets, fixtures, sample anchors, or agent invocation examples

Deterministic check to pair with the development gate: Example tests execute commands in a fixture repository and validate documented JSON against current schemas.

Beads: anchor `pa-2td`, plan questions `pa-2td.1`, dev questions `pa-2td.2`

Fixtures:
- pass: The br example uses docs/plans/phase-a, current flags, and the documented br JSON envelope.
- fail: The example uses an invented path, removed flag, and JSON shape no supported tracker emits.

## ANC-014

Anchor: The plan-anchor plugin must not define or invoke the sc-lint agents arch-qa or req-qa.

> where did arch-qa and req-qa come from?  these are agents on sc-lint, not part of this skill

Said by randlee, plan-anchor self-anchoring review, 2026-10-10. Status: locked. Version 2.

Summary: Exclude sc-lint agents

Scope: edits plan-anchor agent files, registries, manifests, skill delegation, or examples

Deterministic check to pair with the development gate: Repository search finds no arch-qa or req-qa reference under the plan-anchor plugin.

Beads: anchor `pa-9wl`, plan questions `pa-9wl.1`, dev questions `pa-9wl.2`

Fixtures:
- pass: The plan-anchor registries list only anchor-plan-review, anchor-sprint-review, and anchor-question-tune.
- fail: The plan-anchor skill delegates requirement review to the sc-lint req-qa agent.
