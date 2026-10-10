#!/usr/bin/env python3
"""Version discipline for the plan-anchoring skill. Two modes.

Default (release consistency):
  VERSION holds the release version X.Y.Z. Every artifact (SKILL.md, each
  reference, each agent) must share X.Y and have patch >= Z: contributors may
  advance the patch of what they edit, a minor or major change happens only in
  unison through VERSION. registry.yaml mirrors each agent's own version.
  Plugin and marketplace manifests equal VERSION exactly. CHANGELOG.md has a
  "## X.Y.Z" entry.

--base <ref> (pull-request rule):
  Every artifact changed since <ref> must have bumped its version by at least
  one patch over the version at <ref>, within the same X.Y, and CHANGELOG.md
  must have changed. If VERSION itself changed since <ref> this is a release:
  every artifact must equal the new VERSION exactly.

Ownership of unversioned files: a change anywhere under the skill directory
other than references/*.md counts against SKILL.md; a change to
references/<name>.md counts against that reference; a change to
agents/<name>.md counts against that agent. registry.yaml is a mirror and
needs no bump of its own.

Exit 0 in sync, 1 drift (each on its own line), 2 missing files or bad input.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PLUGIN = ROOT / "plugins" / "sc-plan-anchor"
SKILL = PLUGIN / "skills" / "plan-anchoring"
AGENT_DIRS = {
    "claude": PLUGIN / ".claude" / "agents",
    "codex": PLUGIN / ".codex" / "agents",
}
FRONT_RE = re.compile(r"^---\n(.*?)\n---", re.S)
VER_RE = re.compile(r'^\s*version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)["\']?\s*$', re.M)
MODEL_RE = re.compile(r"^model:\s*(\S+)\s*$", re.M)


def parse(v: str):
    return tuple(int(x) for x in v.split("."))


def frontmatter_version(text: str):
    m = FRONT_RE.match(text)
    if not m:
        return None
    v = VER_RE.search(m.group(1))
    return v.group(1) if v else None


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, check=False).stdout


def show(ref: str, rel: str):
    out = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=ROOT, capture_output=True, text=True, check=False)
    return out.stdout if out.returncode == 0 else None


def artifacts() -> list:
    files = [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]
    for agent_dir in AGENT_DIRS.values():
        files.extend(sorted(agent_dir.glob("*.md")))
    return [f for f in files if f.name != "registry.yaml"]


def owner_of(rel: str):
    """Which versioned artifact a changed path counts against."""
    p = pathlib.PurePosixPath(rel)
    skill_rel = SKILL.relative_to(ROOT).as_posix()
    if rel.startswith(skill_rel + "/references/") and rel.endswith(".md"):
        return rel
    if rel.startswith(skill_rel + "/"):
        return skill_rel + "/SKILL.md"
    for agent_dir in AGENT_DIRS.values():
        agents_rel = agent_dir.relative_to(ROOT).as_posix()
        if rel.startswith(agents_rel + "/") and rel.endswith(".md"):
            return rel
    return None


def release_checks(want: str, drift: list) -> int:
    checked = 0
    wmaj, wmin, wpatch = parse(want)
    for f in artifacts():
        if not f.exists():
            print(f"check-version-sync: missing {f.relative_to(ROOT)}", file=sys.stderr)
            sys.exit(2)
        got = frontmatter_version(f.read_text(encoding="utf-8"))
        checked += 1
        rel = f.relative_to(ROOT)
        if got is None:
            drift.append(f"{rel}: no version in frontmatter")
            continue
        gmaj, gmin, gpatch = parse(got)
        if (gmaj, gmin) != (wmaj, wmin):
            drift.append(f"{rel}: {got} changes major.minor; minor bumps happen in unison through VERSION ({want})")
        elif gpatch < wpatch:
            drift.append(f"{rel}: {got} is below VERSION {want}")
        for harness, agent_dir in AGENT_DIRS.items():
            if f.parent == agent_dir:
                front = FRONT_RE.match(f.read_text(encoding="utf-8"))
                model_match = MODEL_RE.search(front.group(1)) if front else None
                if f.name == "anchor-question-tune.md":
                    expected = "opus" if harness == "claude" else "sol"
                else:
                    expected = "sonnet" if harness == "claude" else "luna"
                if not model_match or model_match.group(1) != expected:
                    drift.append(f"{rel}: model must be {expected} for the {harness} harness")
    expected_agents = {f.stem for f in AGENT_DIRS["claude"].glob("*.md")}
    for harness, agent_dir in AGENT_DIRS.items():
        actual_agents = {f.stem for f in agent_dir.glob("*.md")}
        if actual_agents != expected_agents:
            drift.append(f"{agent_dir.relative_to(ROOT)}: agent files {sorted(actual_agents)} != {sorted(expected_agents)}")
        reg = agent_dir / "registry.yaml"
        if not reg.exists():
            drift.append(f"{reg.relative_to(ROOT)}: missing")
            continue
        text = reg.read_text(encoding="utf-8")
        registered = set()
        for m in re.finditer(r"^  ([a-z0-9-]+):\n    version:\s*([0-9.]+)\n    path:\s*(\S+)", text, re.M):
            checked += 1
            name, rv, path = m.groups()
            if name.startswith("anchor-"):
                registered.add(name)
            target = PLUGIN / path.lstrip("/")
            if target.exists():
                fv = frontmatter_version(target.read_text(encoding="utf-8"))
                if fv != rv:
                    drift.append(f"registry.yaml {name}: {rv} != {fv} in {path}")
            else:
                drift.append(f"registry.yaml {name}: path {path} not found")
        if registered != expected_agents:
            drift.append(f"{reg.relative_to(ROOT)}: agents {sorted(registered)} != {sorted(expected_agents)}")
        dependencies = set()
        for m in re.finditer(r'(anchor-[a-z-]+):\s*"([^"]+)"', text):
            dependencies.add(m.group(1))
            if m.group(2) not in (want, f"{wmaj}.x"):
                drift.append(f"{reg.relative_to(ROOT)} depends_on {m.group(1)}: {m.group(2)} does not cover {want}")
        if dependencies != expected_agents:
            drift.append(f"{reg.relative_to(ROOT)}: depends_on {sorted(dependencies)} != {sorted(expected_agents)}")
    manifests = [PLUGIN / "plugin.json", *ROOT.glob("**/.claude-plugin/plugin.json"), *ROOT.glob("**/.codex-plugin/plugin.json"),
                     *ROOT.glob("**/.cursor-plugin/plugin.json"), *ROOT.glob("**/.claude-plugin/marketplace.json"),
                     *ROOT.glob("**/.agents/plugins/marketplace.json"), *ROOT.glob("**/manifest.yaml")]
    for manifest in manifests:
        if "/.git/" in str(manifest) or "node_modules" in str(manifest):
            continue
        checked += 1
        rel = manifest.relative_to(ROOT)
        if manifest.suffix == ".json":
            try:
                data = json.loads(manifest.read_text())
            except json.JSONDecodeError:
                drift.append(f"{rel}: not valid JSON")
                continue
            versions = [data.get("version")] + [p.get("version") for p in data.get("plugins", []) if isinstance(p, dict)]
            for v in versions:
                if v is not None and v != want:
                    drift.append(f"{rel}: {v} != VERSION {want} (manifests carry the release version)")
        else:
            m = re.search(r"^version:\s*([0-9.]+)", manifest.read_text(), re.M)
            if m and m.group(1) != want:
                drift.append(f"{rel}: {m.group(1)} != VERSION {want}")
    plugin_manifests = [
        PLUGIN / "plugin.json",
        PLUGIN / ".claude-plugin" / "plugin.json",
        PLUGIN / ".codex-plugin" / "plugin.json",
    ]
    for manifest in plugin_manifests:
        if not manifest.exists():
            drift.append(f"{manifest.relative_to(ROOT)}: missing")
            continue
        data = json.loads(manifest.read_text())
        if data.get("name") != "sc-plan-anchor":
            drift.append(f"{manifest.relative_to(ROOT)}: name must be sc-plan-anchor")
    claude_manifest = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    expected_claude_agents = {f"./.claude/agents/{name}.md" for name in expected_agents}
    if set(claude_manifest.get("agents", [])) != expected_claude_agents:
        drift.append("Claude manifest agents do not match .claude/agents")
    catalogs = [
        ROOT / ".claude-plugin" / "marketplace.json",
        ROOT / ".agents" / "plugins" / "marketplace.json",
    ]
    for catalog in catalogs:
        if not catalog.exists():
            drift.append(f"{catalog.relative_to(ROOT)}: missing")
            continue
        data = json.loads(catalog.read_text())
        entries = [p for p in data.get("plugins", []) if p.get("name") == "sc-plan-anchor"]
        if len(entries) != 1:
            drift.append(f"{catalog.relative_to(ROOT)}: expected one sc-plan-anchor entry")
            continue
        source = entries[0].get("source")
        source_path = source.get("path") if isinstance(source, dict) else source
        if source_path != "./plugins/sc-plan-anchor":
            drift.append(f"{catalog.relative_to(ROOT)}: source must be ./plugins/sc-plan-anchor")
        elif not (ROOT / source_path[2:]).is_dir():
            drift.append(f"{catalog.relative_to(ROOT)}: source path does not exist")
    changelog = ROOT / "CHANGELOG.md"
    if not changelog.exists() or f"## {want}" not in changelog.read_text():
        drift.append(f"CHANGELOG.md has no '## {want}' entry")
    return checked


def pr_checks(base: str, want: str, drift: list) -> str:
    changed = set(l for l in git("diff", "--name-only", f"{base}...HEAD").splitlines() if l.strip())
    changed |= set(l for l in git("diff", "--name-only", base).splitlines() if l.strip())          # working tree edits
    changed |= set(l for l in git("ls-files", "--others", "--exclude-standard").splitlines() if l.strip())  # new, uncommitted files
    changed = sorted(changed)
    base_version = (show(base, "VERSION") or "").strip()
    release = base_version != want
    if release:
        for f in artifacts():
            got = frontmatter_version(f.read_text(encoding="utf-8"))
            if got != want:
                drift.append(f"release PR: {f.relative_to(ROOT)} is {got}, must equal VERSION {want}")
        if "CHANGELOG.md" not in changed:
            drift.append("release PR: CHANGELOG.md did not change")
        return f"release mode (VERSION {base_version or 'absent'} -> {want})"
    owners = {}
    for rel in changed:
        o = owner_of(rel)
        if o:
            owners.setdefault(o, []).append(rel)
    for owner, paths in sorted(owners.items()):
        cur = frontmatter_version((ROOT / owner).read_text(encoding="utf-8")) if (ROOT / owner).exists() else None
        old_text = show(base, owner)
        old = frontmatter_version(old_text) if old_text else None
        if old is None:
            continue  # new artifact: the release check already requires it to sit at VERSION's X.Y
        if cur is None:
            drift.append(f"{owner}: no version (edited: {', '.join(paths)})")
            continue
        omaj, omin, opatch = parse(old)
        cmaj, cmin, cpatch = parse(cur)
        if (cmaj, cmin) != (omaj, omin):
            drift.append(f"{owner}: {old} -> {cur} changes major.minor in a non-release PR; bump the patch only")
        elif cpatch <= opatch:
            drift.append(f"{owner}: still {cur} but edited ({', '.join(paths)}); bump to {omaj}.{omin}.{opatch + 1}")
    if owners and "CHANGELOG.md" not in changed:
        drift.append("CHANGELOG.md did not change; add a line under '## Unreleased'")
    return f"patch mode against {base} ({len(owners)} artifact(s) edited)"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="", help="git ref of the PR base; enables the pull-request rule")
    args = ap.parse_args()
    vfile = ROOT / "VERSION"
    if not vfile.exists():
        print("check-version-sync: VERSION file missing", file=sys.stderr)
        return 2
    want = vfile.read_text().strip()
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", want):
        print(f"check-version-sync: VERSION is not X.Y.Z: {want!r}", file=sys.stderr)
        return 2
    drift: list = []
    checked = release_checks(want, drift)
    mode = pr_checks(args.base, want, drift) if args.base else "release consistency"
    if drift:
        print(f"check-version-sync [{mode}]: {len(drift)} drift(s) from VERSION {want}:")
        for d in drift:
            print(f"  {d}")
        return 1
    print(f"check-version-sync [{mode}]: {checked} artifacts consistent with {want}, CHANGELOG entry present")
    return 0


if __name__ == "__main__":
    sys.exit(main())
