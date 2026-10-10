# Sprint A2 — Markdown and tracker plan sources

## Objective

Let `/plan-anchoring` review either a phase index plus linked Markdown sprint
documents or a copy of the same plan under a `bd`/`br` epic, using one normalized
item contract and explicit source parity checks.

## Scope boundary

This sprint owns Markdown and tracker plan-source discovery, sprint ordering,
repository path confinement, structural checks, source revisions, normalized
digests, parity comparison, and item composition. It does not mutate tracker
state, tune questions, or change verdict semantics.

## Dependency relations

- `must_follow` Sprint A1 because the plan-source descriptor is validated as an
  operation-specific extension of the runner payload.
- Sprint A3 is `must_follow` because tracker records attach workflow metadata to
  the source descriptors established here.

## Invocation and source contract

Supported user-facing targets:

```text
/plan-anchoring docs/plans/phase-a/plan-phase-a.md
/plan-anchoring docs/plans/phase-a/
/plan-anchoring --tracker br --epic pa-sza
```

The directory form must resolve exactly one phase index. The phase index must
contain one sprint table whose plan links identify ordered repository-local
Markdown files. The tracker form must resolve one epic and its ordered planning
children; each child description is an exact copy of one complete sprint
Markdown file, while tracker title, acceptance, design, and notes remain workflow
metadata. Both forms produce the copied sprint Markdown plus source metadata as
the normalized item. Each Markdown sprint file must contain one
authoritative section each for deliverables, acceptance criteria, and validation,
plus explicit scope and non-closure. Paths to delete are required only when
deletion is in scope.

## Authoritative deliverables

- Plan-source adapters for a phase-index file/directory and a selected tracker
  epic, returning ordered sprint descriptors with source kind, phase/sprint ID,
  source reference/revision, normalized SHA-256, and dependency relation.
- Deterministic parsing of the phase sprint table without executing Markdown,
  HTML, links, code blocks, or repository content.
- Repository confinement and rejection of absolute, escaping, duplicate,
  missing, non-regular, or symlink-escaped sprint paths.
- Structural checks for exactly one authoritative deliverables, acceptance, and
  validation section in every sprint and for unique phase/sprint identifiers.
- Planning-item composition from the complete sprint file or tracker copy with
  a shared normalization function and no source-specific semantic rewriting.
- A copy/parity command that writes or verifies each complete sprint document in
  the tracker description, records the source path/digest, and refuses
  destructive overwrite when the target changed independently.
- Run metadata binding every verdict to the phase path, sprint path, Git commit
  when available, and SHA-256 reviewed.
- A `shape` path for sprint files that reports section sizes and detects plans
  too large for reliable review without silently trimming prose.

## Authoritative acceptance criteria

- File, directory, and `pa-sza` tracker invocations discover the same ordered
  sprint set for this Phase A plan.
- A fresh tracker copy has the same normalized item digest as its Markdown
  source; independent drift fails parity before Jev is called.
- Every Jev request contains one normalized sprint item and one anchor, never
  the phase index/epic, intent, or another sprint.
- Invalid or ambiguous phase structures return typed errors before delegation.
- A sprint exceeding the reliable limit produces `PLAN.TOO_LARGE` plus shape
  evidence; no implementation truncates prose or raises the cap to pass.

## Authoritative validation

- Parser fixtures: valid phase file/directory and tracker epic; missing or duplicate index;
  malformed sprint table; duplicate ID/path; broken link; absolute/traversing
  path; symlink escape; missing authoritative section; duplicate checklist.
- Golden composition tests proving equivalent Markdown and tracker copies
  normalize identically, including headings, prose, and fenced examples.
- Digest tests proving stable output, changed-content detection, and drift refusal.
- Dogfood discovery over `docs/plans/phase-a/plan-phase-a.md` returning A1–A7
  in table order.

## Traceability

- Phase requirements: PA-REQ-005–007.
- Anchors: ANC-015–016.
- Tracker: `pa-sza.2`.

## Risks and mitigations

- Markdown parsing grows into a general parser: support the explicit phase
  table and authoritative headings only; fail on ambiguity.
- Detailed contracts make a sprint too large: harden or split on a real
  production-ready boundary rather than hiding content from Jev.

## Non-closure

- Arbitrary Markdown plans without a phase index and sprint documents.
- Automatic rewriting or splitting of sprint documents.
- General tracker mutation beyond safe copy creation/parity verification.
- Development-gate evidence composition.

## Handoff to A3

A3 associates optional tracker identities, dependencies, question records, and
review comments with these immutable source descriptors while leaving their
Markdown content authoritative.
