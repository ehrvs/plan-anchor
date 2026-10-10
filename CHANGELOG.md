# Changelog

`VERSION` holds the release version. Contributors bump the patch of each artifact they edit and add a line under Unreleased; a release bumps the minor in unison and turns Unreleased into a dated section. `scripts/check_version_sync.py` enforces both (see CONTRIBUTING.md).

## Unreleased

- Planning gate sends a bead whole when it fits one Jev request (`--max-item-chars`, and `--max-request-bytes` for every anchor). Otherwise blocks longer than `--max-code-lines` are reduced to signatures one at a time, longest first, until it fits. `PLAN.TOO_LARGE` is unchanged. Measured on a 13-bead plan with 6 anchors: underspecified cells went from 15 to 8, and passing beads from 1 to 6 (`docs/experiments/2026-10-10-redact-only-when-oversize.md`). SKILL.md, plan-size-and-shape, jev-api, measured-behaviour and anchor-plan-review are now 0.3.1.

## 0.3.0 — 2026-10-10

Shaped by first use on a real multi-sprint plan and 245 live Jev requests against it (`docs/experiments/2026-10-10-phase-h-jev-experiments.md`).

- Anchors: `statement` is a testable requirement; the user's exact words are a separate immutable `quote`. `add` refuses a statement equal to its quote and near-duplicates (`ANCHOR.DUPLICATE_CANDIDATE`); `update --statement` rewords with history; `retire` replaces hand edits.
- Anchor `kind`: `directive`, `prohibition` (judged on contradiction only), `structural` (deterministic check only, verdict `deterministic_only`).
- New subcommands: `lint` (testability rules), `rubric` (Jev-judged testability, six criteria), `dedupe` (lexical, optionally Jev), `shape` (per-bead size, code/prose, references, repeated paragraphs), `compose-item --for plan|dev`, `diff --expected`.
- Planning gate judges title, description and acceptance criteria; never shortens prose; long code goes to Jev as signatures; an oversized bead is `PLAN.TOO_LARGE` and triaged as a symptom (unapproved work, prose and ceremony, split last).
- Gate caps: plan 24,000 bytes (what Jev reads reliably), dev 64,000. Near-threshold cells are re-asked once; every result carries `leaning`.
- New agent `anchor-question-tune` (background): proves and refines per-anchor question wording against fixtures and known beads.
- New references: `planning-gate`, `development-gate`, `question-tuning`, `triage-and-iteration`, `plan-size-and-shape`, `measured-behaviour`.
- 134 offline tests; CI on Linux, macOS, Windows.

## 0.2.0 — 2026-10-10

- Script hardened from QA review: three attempts per anchor with backoff, context-window shortening at the development gate, response validation, exit codes 0/1/2, dry runs written to the run directory, `compose-item`, `update`, `check-fixtures`.
- Agents gain `script` input, Invocation sections and the Codex/Cursor inline fallback; `bd comment --file` fixed; per-gate references added.
- First live verification against `jev-1.13.0` on both gates. Installed in sc-lint (PR #207).

## 0.1.0 — 2026-10-09

- Initial skill: SKILL.md, nine references, `jev_judge.py`, question sets, templates, `anchor-plan-review` and `anchor-sprint-review` agents, registry.
