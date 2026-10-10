# Sprint A3 — Tracker-neutral anchor and question store

## Objective

Support a quickly initialized Go/Dolt `bd` or Rust/SQLite `br` store for anchors
and their plan/dev question records. Plan issues are optional and exist only when
the tracker-copy source from A2 is requested.

## Scope boundary

This sprint owns initialization guidance, tracker selection, the five normalized
operations used by the anchor/question workflow, JSON normalization, and typed
tracker failures. It does not require plan work to be represented as issues.

## Dependency relations

- `must_follow` Sprint A2 so tracker objects reference established source
  descriptors rather than becoming a competing plan source.
- Sprint A4 is `must_follow` because its CLI/configuration cleanup exposes the
  explicit tracker-selection behavior implemented here.

## Normalized operation contract

| Operation | `bd` implementation | `br` implementation | Result |
| --- | --- | --- | --- |
| `show(id)` | `bd show ID --json` | `br show ID --json` | one issue object |
| `children(id)` | `bd children ID --json` | `br dep list ID --direction up --type parent-child --format json`, then `br show` | ordered issue array |
| `create(fields)` | fixed `bd create` argv | fixed `br create` argv | created issue identity |
| `update(id, fields)` | fixed `bd update` argv | fixed `br update` argv | updated issue identity/status |
| `comment(id, file)` | `bd comment ID --file FILE` | `br comments add ID --file FILE` | comment receipt |

## Authoritative deliverables

- A tracker descriptor and adapter exposing only `show`, `children`, `create`,
  `update`, and `comment` with typed fields and normalized JSON results.
- Explicit selection rules: a requested tracker wins after capability checks;
  otherwise exactly one valid repository workspace must be discovered.
- Canonical binary/workspace resolution once at the orchestration boundary and
  typed ambiguity, missing, unsupported-version, not-found, conflict, and
  malformed-output errors.
- Fixed subprocess argv construction with no shell and no command text accepted
  from agent params.
- `bd` and `br` fixture suites plus installed-binary integration tests guarded
  by binary availability.
- Fast, documented initialization for a repository that needs only anchor and
  question records, without unrelated agent/hook installation side effects.
- Optional tracker plan-copy records carrying the source path and digest defined
  by A2; they are not created for ordinary Markdown-only review.

## Authoritative acceptance criteria

- The same normalized contract tests pass for current supported `bd` and `br`
  fixture outputs.
- The registered plan-review agent can read question records through either
  adapter regardless of whether plan input is Markdown or a tracker copy.
- If both or neither valid tracker workspaces are available without an explicit
  selection, the adapter returns a typed error instead of guessing.
- Params containing shell command strings or unsupported operation names are
  rejected before process creation.
- A new repository can initialize a `br` anchor/question store, create one anchor
  tree, and validate it without first creating a phase epic or sprint issues.

## Authoritative validation

- Contract fixtures for array/object/envelope output, empty children, missing
  issue, version mismatch, ambiguity, malformed JSON, and nonzero exit.
- Command-injection tests over IDs, paths, comments, and unknown fields proving
  argv remains data and no shell is invoked.
- Installed-binary smoke tests for `show`, `children`, and a disposable create /
  update / comment lifecycle when the corresponding tracker is available.
- Regression proving the current `br` Phase A workspace no longer fails through
  a hard-coded `bd show` path.

## Traceability

- Phase requirements: PA-REQ-008–010.
- Locked anchors: ANC-013, ANC-016–018.
- Tracker: `pa-sza.3`.

## Risks and mitigations

- Similar command names conceal semantic differences: normalize explicit
  operations and test real emitted shapes; never interpolate command templates.
- Auto-selection chooses a stray installation: require a valid repository-local
  workspace and fail on ambiguity.

## Non-closure

- Database migration or shared on-disk format.
- General tracker operations unrelated to plan-anchor.
- Markdown parsing or mandatory plan-content projection into issue bodies.

## Handoff to A4

A4 exposes tracker choice through explicit arguments/defaults and removes the
remaining environment configuration without changing adapter semantics.
