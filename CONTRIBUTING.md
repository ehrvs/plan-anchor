# Contributing

plan-anchoring is a general-purpose skill. Anyone, human or agent, may propose an upgrade. These rules keep it auditable and keep it general.

## What a good change looks like

- **One aspect per pull request.** The skill is a table of contents (`SKILL.md`) with one reference per aspect. Change the reference that owns the aspect; add a new reference only for a new aspect, and list it in `SKILL.md`.
- **General wording.** No project names, people, issue numbers, crate names or team-specific process. Use neutral examples (the "legacy repo" example is the house one). `grep -rniE "<your repo>|<your team>" plugins/sc-plan-anchor/` must return nothing.
- **Concise.** One idea per sentence. State a rule once, where it is defined; elsewhere cite it. Justify numbers from `references/measured-behaviour.md`; a behaviour change that rests on how Jev judges comes with measurements (see `docs/experiments/` for the protocol).
- **Script and docs together.** A new flag, field, verdict, error code or exit code lands with its reference text, its agent text if an agent uses it, and a test. Existing names are never renamed or removed in a patch; add only.
- **Tests green.** `python3 -m unittest discover -s tests/sc-plan-anchor` and `python3 scripts/check_version_sync.py --base origin/main` both pass before you open the PR.
- **Never a secret.** No keys, no live run output containing private plan text. Fixture answers and dry runs are how tests touch Jev.

## Versioning

`VERSION` at the repo root is the release version. Every versioned artifact (`SKILL.md`, each `references/*.md`, each `agents/*.md`, mirrored in `registry.yaml`) shares its major.minor.

| You are | You do |
| --- | --- |
| Proposing a change | Bump the **patch** of every artifact you edit, from the version it has on the base branch: `0.3.0` becomes `0.3.1`. Edits to `scripts/`, `assets/` or the repository-level `tests/sc-plan-anchor/` suite count against `SKILL.md`. Mirror every agent and skill bump in `registry.yaml`. Add a line under `## Unreleased` in `CHANGELOG.md`. |
| Releasing (maintainers) | Bump the **minor** in `VERSION`, set every artifact and manifest to exactly that version in one commit, turn `## Unreleased` into `## X.Y.0 — date`. |

Never change major.minor in a non-release PR, never bump a file you did not edit, and never leave an edited artifact at its old version. `scripts/check_version_sync.py` enforces this: by default it checks that every artifact shares `VERSION`'s major.minor with a patch at or above it, that the registry mirrors the agents, that manifests equal `VERSION`, and that the changelog has the release entry; with `--base <ref>` (CI runs it on every pull request) it also checks that each artifact you touched advanced its patch and that `CHANGELOG.md` changed. A PR that changes `VERSION` is a release and must bring every artifact to the new version exactly.

## Proposing a change as an agent

1. Read `SKILL.md`, then only the reference you intend to change.
2. Make the change, bump the patch of what you edited, add the changelog line.
3. Run the tests, the version check with `--base`, and the general-wording grep.
4. Open the PR with: what changed, which aspect, the evidence (test names, measured cells), and the before and after version of each artifact.

## What not to propose

- Repo-specific anchors, question overrides, or examples: those live in the consuming repository's `anchors.json` and question beads, not in the skill.
- Raising a size cap, lowering a threshold, or changing default question wording without a measurement that shows the effect.
- A rename of a flag, field, verdict or error code. Deprecate by adding the new name and keeping the old.
