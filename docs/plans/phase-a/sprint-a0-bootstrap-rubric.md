# Sprint A0 — Bootstrap rubric calibration

## Objective

Make the testability rubric a trustworthy prerequisite for anchor capture by
calibrating its questions and confidence handling against a frozen,
plan-independent oracle before it judges this Phase A plan.

## Scope boundary

This sprint owns the versioned testability questions, their deterministic lint
seam, confirmation semantics, the calibration corpus, and the tuner's
`testability` operation. It does not tune plan/development questions, review the
active Phase A plan, or change plan/development verdict semantics.

## Dependency relations

- Root sprint; follows the Phase A base on `main`.
- Sprint A1 is `must_follow` because every later contract and dogfood run relies
  on anchors admitted by this calibrated bootstrap gate.

## Authoritative deliverables

- A frozen, versioned calibration corpus whose cases and expected answers are
  written before any Jev response and are unrelated to the active Phase A plan.
- Corpus coverage for valid directives, prohibitions, structural and global
  scope, one atomic anchor extracted from a multi-directive quote, genuinely
  bundled statements, unsupported elaboration, vague outcomes, explicit
  testable conditions, and API-key-output redaction.
- Testability questions that judge separately actionable constraints,
  observable artifacts or behavior, quote-supported obligations, identifiable
  scope, and self-contained conditions without requiring literal token matches.
- Deterministic requirement-form lint rather than a stochastic grammar vote.
- Duplicate detection that compares the testable statements, not only their
  provenance quotes, so two distinct atomic anchors may cite the same
  multi-directive user statement without being mislabeled as duplicates.
- Confirmation that runs each semantic cell twice and a third time on
  disagreement; low-confidence agreement is `inconclusive`, disagreement is
  `unstable`, and neither is misreported as evidence that wording is wrong.
- A `testability` operation in the independent Opus/Sol question-tuner contract
  that receives approved intent and the frozen corpus but no active-plan
  verdict, and returns corpus/rubric digests, rationales, attempts, disagreement
  data, and an acceptance table.

## Authoritative acceptance criteria

- The frozen corpus and expected labels are hashed before the first Jev call;
  no case is added, removed, or relabeled after a response.
- Every accepted rubric cell has two confident agreeing answers matching the
  oracle, with a third call used only to resolve disagreement.
- Confirmed `no` or `unclear` yields `needs_work`; low confidence yields
  `inconclusive`; conflicting confirmations yield `unstable`.
- An atomic anchor drawn from a multi-directive quote may pass when every
  obligation in the statement is supported by the quote; it need not exhaust
  unrelated directives in that quote.
- Two anchors with the same immutable quote are not duplicates when their
  normalized testable statements express distinct obligations; genuinely
  overlapping statements remain a failing duplicate pair.
- Explicit prohibitions and testable conditions may pass the self-contained
  criterion without being rewritten into misleading positive prose.
- The redaction case distinguishes compliant from violating output through an
  input/action/outcome test and does not depend on literal statement tokens.

## Authoritative validation

- Offline state-machine tests for two-call agreement, third-call tie breaking,
  `testable`, `needs_work`, `inconclusive`, and `unstable`.
- Recorded-answer corpus tests for every required case and each semantic cell.
- Live independent Sol/Opus calibration with persisted corpus digest, rubric
  digest, expected answers, rationales, all run IDs, and final acceptance table.
- Mutation cases for a bundled statement, unsupported policy, vague outcome,
  private shorthand, unrecorded approval dependency, two atomic anchors sharing
  one quote, and two genuinely duplicate statements with different quotes.

## Traceability

- Phase requirement: PA-REQ-018.
- Anchors: none; this is the bootstrap instrument that determines whether an
  anchor is fit to enter later gates.
- Tracker: `pa-sza.8`.

## Risks and mitigations

- Calibration overfits Phase A: exclude active-plan text and use unrelated
  corpus cases with frozen rationales.
- Repeated calls hide uncertainty: preserve every answer and disagreement;
  confirmation classifies instability rather than averaging it away.
- Rubric work drifts into plan verdict changes: keep plan/development question
  IDs, roles, thresholds, and `decide()` semantics out of this sprint.

## Non-closure

- Tuning any Phase A plan or development question.
- Lowering a threshold to turn an inconclusive answer into a pass.
- Changing plan/development verdict meanings or coverage policy.
- Reviewing Markdown or tracker plan sources.

## Handoff to A1

A1 consumes only anchors accepted by the calibrated bootstrap gate and records
the rubric/corpus versions in the invocation attestation; it does not reopen
testability semantics.
