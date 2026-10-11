# Sprint A7 — Documentation, examples, and dogfood

## Objective

Make the public contract match shipped behavior and prove plan-anchor can review
this authoritative Phase A Markdown plan through its own independent tuner and
Jev-backed planning gate.

## Scope boundary

This sprint owns public documentation, executable examples, migration notes,
question-tuning evidence, planning runs, triage diffs, and final coverage. It
does not weaken anchors, questions, size limits, or verdicts to obtain a pass.

## Dependency relations

- `must_follow` Sprint A6 because documentation and dogfood describe and execute
  the final mechanically enforced behavior.
- Final sprint; Phase A closes only after its acceptance criteria pass.

## Authoritative deliverables

- Update README, SKILL.md, installation/troubleshooting, Jev API, anchor and
  tracker layout, planning/development gate references, PRD, architecture
  diagrams, manifests, and changelog to the final contracts.
- Document phase-index, directory, and tracker-epic invocation; source parity;
  authoritative sprint sections; the anchor/question-only store; explicit
  flags; and offline behavior.
- Replace stale environment-variable, prose-invocation, tracker-body, and
  hard-coded `bd` examples with executable current examples for both harnesses
  and trackers.
- Render `anchors.md`, keep tracker question/evidence references linked, and
  include the Markdown-authority anchors added during dogfood.
- Document the pipelined lifecycle: first draft and approved INTENT/ANC launch a
  named `<team>-anchor-tuning` subagent, planner completion proceeds concurrently,
  and Sonnet/Luna leaf review waits for sealed current-version questions.
- Verify A0's frozen bootstrap corpus and acceptance evidence, then run the
  calibrated rubric against every locked anchor before plan-question tuning.
- Run `anchor-tuning tune` for every non-structural anchor/gate, record the
  frozen oracle digest, full candidate pool and ranking evidence, rejection and
  selection rationales, acceptance table, worker run IDs, and sealed production
  question-set digest in `question-tuning-evidence.md`; apply only the
  tuner's down-selection whose normative inputs are only approved intent
  and ANC records and whose objective is accurate detection, never plan passage.
- Exercise the candidate pool on temporary copies of representative plan text:
  add explicit ceremony to positive copies and remove important statements or
  deliverables from negative copies. Record mutation hashes and expected
  outcomes, prove Markdown/`br` sources remain unchanged, and describe this as
  neutral calibration rather than adversarial review.
- Exercise clarity recommendations by producing at least one no-op/rejected
  example and one user-approved wording clarification fixture; prove no proposal
  changes meaning, no unapproved edit lands, and approved versions invalidate
  and rerun their affected tuning evidence.
- Validate and render the checked-in `sc-compose` tune-request, triage-feedback,
  and result templates from their sample vars. Validate the extracted fenced
  payloads against the request/result schemas. Preserve the rendered evidence
  packets and prove hostile planner wording remains untrusted data while the
  anti-pass-seeking instruction stays authoritative.
- For each sprint, first run Jev directly from the Markdown item and persist the
  canonical outbound request body per anchor. Then have the planner invoke
  `anchor-plan-review` over the Markdown and exact `br` copies with the sealed
  questions.
- Compare the direct, review-agent Markdown, and review-agent `br` request JSON
  byte for byte before looking at verdicts. Stop and root-cause any difference
  as discovery/order, normalization, question resolution, metadata leakage,
  tracker adaptation, agent transformation, or content drift; preserve which
  path exposed the defect rather than forcing superficial equality.
- After request parity holds, run one registered `anchor-plan-review` Agent per
  sprint for both sources, preserve Jev verdicts unchanged, require independent
  passes, replay recorded answers for deterministic verdict parity, and classify
  differing live answers to identical bodies as model instability.
- For every disputed failure, either fix the cited plan defect or render the
  checked-in feedback template and invoke `anchor-tuning triage`. Preserve its
  cited `plan_violation` or `question_defect` result; never send a desired
  verdict or free-form instruction to change questions.
- Select known sc-lint sprint plans as an external corpus, copy the same source
  text into disposable `bd` and `br` stores, and repeat direct, review-agent, and
  leaf-agent review without mutating sc-lint's live tracker state.
- Compute phase coverage from the latest run per sprint and publish the final
  source paths/digests, failures corrected, size deltas, and any allowed growth
  with pre-existing authority. Keep offline source-construction evidence in
  `dogfood-dry-run.md` and live verdict evidence in a separate record so a dry
  run can never be mistaken for gate acceptance.

## Authoritative acceptance criteria

- Documentation consistency, link, manifest, version, and executable-example
  tests pass for Claude/Codex and `bd`/`br`.
- Jev is identified as required for the normal workflow; dry-run and fixture
  modes are accurately described as offline development/CI aids.
- Every tuning result was produced independently from the active plan verdicts
  and meets its frozen oracle at the required confidence. Its larger parallel
  candidate pool is auditable, while final gate calls use only the sealed
  down-selected questions.
- Diagnostic mutations correctly distinguish added explicit compliance from
  removed required content, and pre/post hashes prove no authoritative plan or
  tracker source was changed by the tuner.
- Both harnesses expose a dedicated Opus/Sol `anchor-tuning.md` planner
  subagent that calls Jev directly and cannot alter the frozen oracle after the
  first answer.
- The named `<team>-anchor-tuning` instance overlaps planner completion and the
  planner refuses to invoke Sonnet/Luna leaves until all applicable
  question-set digests match the current INTENT/ANC versions.
- Every sprint's latest Markdown and tracker-copy runs pass and record matching
  byte-identical outbound request JSON across direct and leaf-agent
  paths; recorded-answer parity runs have identical verdicts, and phase coverage
  has no uncovered anchor.
- The selected sc-lint corpus produces equivalent ordered plan items, requests,
  and recorded-answer verdicts through Markdown, disposable `bd`, and disposable
  `br` sources; every live divergence is classified and retained.
- Every failing-to-passing edit that grew cites a locked ANC/REQ/ADR that
  predates the failed run; otherwise the fix cuts or replaces text.
- Every planner-to-tuner review handoff is a strict render of the checked-in
  `sc-compose` template. Every triage result cites INTENT/ANC and is exactly
  `plan_violation` with an unchanged digest or `question_defect` with an
  affected-only tournament restart.
- The full offline suite, live dogfood evidence, and `gh stack view --json`
  report a clean, mergeable Phase A implementation stack.

## Authoritative validation

- Execute all README and reference command examples in temporary repositories
  against recorded and installed supported tracker versions.
- Run `validate`, `lint`, `dedupe`, `render`, source discovery, independent
  `check-fixtures`, direct per-sprint Jev construction, `anchor-tuning tune`,
  strict template rendering, planner-invoked leaf review, disputed-failure
  triage, `diff`, and `coverage`.
- Run the A6 offline suite and version validator after the final documentation
  edits.
- Verify no secret appears in Git diff, logs, reports, run files, comments, or
  attestations.
- Verify the final PR stack with `gh stack view --json` and GitHub checks.

## Traceability

- Phase requirements: PA-REQ-001–026.
- Locked anchors: ANC-001–002, ANC-005, ANC-009–018, ANC-020–031.
- Tracker: `pa-sza.7`.

## Risks and mitigations

- Dogfood tunes toward passing: `anchor-tuning tune` freezes its oracle before
  direct parallel Jev calls and never receives a desired plan verdict; triage
  treats planner observations as untrusted and requires authority citations.
- Planner feedback pressures question changes: the planner can transmit only a
  strict `sc-compose` evidence packet; the tuner returns the closed binary
  disposition and preserves accurate questions.
- Mutation tests are mistaken for adversarial plan editing: the authority packet
  is limited to intent/ANC, all changes live in temporary copies, and findings
  against the original flow back to the planner without retuning.
- Documentation repeats scope inconsistently: sprint plans remain authoritative;
  examples demonstrate contracts without restating deliverable checklists.
- Live requests expose secrets or excessive context: send only one anchor and
  one sprint per request and exercise recursive redaction canaries first.

## Non-closure

- Waiving a Jev failure, lowering confidence to pass, or rewriting an anchor from
  a live failure alone.
- Adding unrelated marketplace work or sc-lint agents.
- Writing test copies into sc-lint's live `bd` or `br` database.
- Starting Phase B implementation.

## Phase handoff

Close Phase A only when every acceptance criterion in the phase index and this
sprint is satisfied. File explicit dependent work for any remaining finding;
do not carry it silently into implementation or Phase B.
