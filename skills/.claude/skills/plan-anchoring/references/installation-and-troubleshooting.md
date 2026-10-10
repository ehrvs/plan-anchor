---
name: installation-and-troubleshooting
version: 0.1.0
description: Installing and locating the CLIs and credentials plan-anchoring depends on (python3, beads bd, TypeSafe API key), minimum versions, PATH issues in Claude Code, validation, and known issues.
---

# Installation and troubleshooting

## Check first

```bash
which python3 && python3 --version
which bd && bd --version
test -n "$TYPESAFE_API_KEY" && echo "key set" || echo "key missing"
```

If all three succeed, skip to Validation.

## Find an existing install

Claude Code's bash inherits a minimal PATH that can miss Homebrew, Go, pyenv, and `~/.local/bin`:

```bash
for p in /opt/homebrew/bin/bd "$HOME/go/bin/bd" "$HOME/.local/bin/bd" /usr/local/bin/bd; do [ -x "$p" ] && echo "bd at $p"; done
for p in /opt/homebrew/bin/python3 /usr/local/bin/python3 /usr/bin/python3 "$HOME/.pyenv/shims/python3"; do [ -x "$p" ] && echo "python3 at $p"; done
```

Use the full path, or `export PATH="/opt/homebrew/bin:$PATH"` for the session.

## Install

**python3** (3.9 or newer; the script is standard-library only)

- macOS: `brew install python` or the Xcode command line tools' `/usr/bin/python3`
- Linux: `apt install python3` / `dnf install python3`
- Windows: `winget install Python.Python.3.12`; use forward slashes in paths

**beads (`bd`)**

- macOS: `brew install steveyegge/beads/bd` (or the tap your team uses)
- Any platform with Go: `go install github.com/steveyegge/beads/cmd/bd@latest`, then add `$HOME/go/bin` to PATH
- Initialise in the repo once: `bd init`

**TypeSafe API key**

- Create a key at typesafe.ai and export it: `export TYPESAFE_API_KEY=...` in the shell that launches Claude Code, or in the project's `.envrc`. Never commit it and never echo it.
- For live gate runs also `export PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` for that session only (see `jev-api.md`).

## Minimum versions

| Tool | Minimum | Why |
| --- | --- | --- |
| python3 | 3.9 | `from __future__ import annotations`, `str.removeprefix` not used; 3.9 is the floor tested |
| bd | 1.x | `--parent`, `--labels`, `--silent`, `show --json`, `children --json` |
| Jev | `jev-latest` | pin a version once thresholds are tuned |

## PATH troubleshooting

- A tool that works in your terminal but not in the skill: your shell init added it to PATH and Claude Code's bash did not source that file. Export the directory in the session or put the tool's full path in your commands.
- `bd` found but `bd show --json` errors with "no database": run commands from the repo root that has `.beads/`, or pass `--repo`.

## Validation

```bash
python3 .claude/skills/plan-anchoring/scripts/jev_judge.py --help
python3 .claude/skills/plan-anchoring/scripts/jev_judge.py validate --anchors .claude/skills/plan-anchoring/assets/examples/anchors.example.json
python3 .claude/skills/plan-anchoring/scripts/jev_judge.py judge --anchors .claude/skills/plan-anchoring/assets/examples/anchors.example.json \
  --gate plan --all --item-id smoke --item-file .claude/skills/plan-anchoring/SKILL.md \
  --answers-file .claude/skills/plan-anchoring/assets/examples/answers.fixture.json --out /tmp/anchor-smoke.json
```

The last command exercises the full gating path with fixture answers and no network; expect `not_addressed` for ANC-012 and `not_applicable` for REQ-014.

## Known issues

- `POLICY.REMOTE_JUDGE_DISABLED` on a live run: the opt-in is deliberate. Set `PLAN_ANCHOR_ALLOW_REMOTE_JUDGE=1` only once sending this plan's text to TypeSafe is acceptable.
- `QUESTIONS.ROLES`: a question override renamed a question ID without updating `roles`. Keep the default IDs.
- `VALIDATION.ANCHORS` from `judge`: run `validate` and fix the listed problems; the usual cause is a hand edit that set an invalid `status`.
- `JEV.RATE_LIMITED` under parallel gates: cap concurrency at 3 beads; the agents retry once with backoff.
- Dates in reports show as "undated": `stated_at` is not an ISO date. Use `YYYY-MM-DD`.
- Windows: the report's short-date formatting falls back gracefully, but run `bd` and the script from Git Bash or PowerShell with forward slashes.
