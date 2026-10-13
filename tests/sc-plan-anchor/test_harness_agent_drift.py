"""Fail when Claude, Codex, and Cursor copies diverge after harness frontmatter.

Agent bodies must match once YAML frontmatter is removed. Registries must
match once each ``.{harness}/`` path prefix is normalized.
"""

from pathlib import Path
import difflib
import re
import unittest


ROOT = Path(__file__).resolve().parents[2]
PLUGIN = ROOT / "plugins" / "sc-plan-anchor"
HARNESSES = ("claude", "codex", "cursor")
AGENTS = ("anchor-plan-review.md", "anchor-sprint-review.md", "anchor-tuning.md")
HARNESS_PATH = re.compile(r"\.(claude|codex|cursor)/")


def body_after_frontmatter(text: str, path: Path) -> str:
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} has no YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise AssertionError(f"{path} has unterminated YAML frontmatter")
    return text[end + 5 :]


def explain(label: str, left_name: str, left: str, right_name: str, right: str) -> str:
    diff = "".join(
        difflib.unified_diff(
            left.splitlines(keepends=True),
            right.splitlines(keepends=True),
            fromfile=left_name,
            tofile=right_name,
        )
    )
    return f"{label} drifted:\n{diff}"


class HarnessAgentDriftTests(unittest.TestCase):
    def test_agent_bodies_match_after_frontmatter(self):
        for name in AGENTS:
            bodies = {}
            for harness in HARNESSES:
                path = PLUGIN / f".{harness}" / "agents" / name
                self.assertTrue(path.is_file(), f"missing {path}")
                bodies[harness] = body_after_frontmatter(path.read_text(encoding="utf-8"), path)
            baseline = bodies["claude"]
            for harness in HARNESSES[1:]:
                self.assertEqual(
                    baseline,
                    bodies[harness],
                    explain(name, "claude", baseline, harness, bodies[harness]),
                )

    def test_registries_match_after_harness_path(self):
        normalized = {}
        for harness in HARNESSES:
            path = PLUGIN / f".{harness}" / "agents" / "registry.yaml"
            self.assertTrue(path.is_file(), f"missing {path}")
            normalized[harness] = HARNESS_PATH.sub(".HARNESS/", path.read_text(encoding="utf-8"))
        baseline = normalized["claude"]
        for harness in HARNESSES[1:]:
            self.assertEqual(
                baseline,
                normalized[harness],
                explain("registry.yaml", "claude", baseline, harness, normalized[harness]),
            )


if __name__ == "__main__":
    unittest.main()
