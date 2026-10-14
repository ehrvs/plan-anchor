#!/usr/bin/env python3
"""Bounded, JSON-first mechanical setup. Never judges remotely or executes plan text."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

DEFAULTS = {"jobs": 3, "request_budget": 100, "calibration_budget": 1000, "threshold": 0.6}
KINDS = ("anchors", "intent", "items", "seal")


def digest(path):
    try:
        return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    except (OSError, TypeError):
        return None


def json_file(path):
    try:
        return json.loads(pathlib.Path(path).read_text(encoding="utf-8")), None
    except (OSError, UnicodeError, ValueError, TypeError) as exc:
        return None, type(exc).__name__


def settings_for(args):
    path = pathlib.Path(args.settings).expanduser() if args.settings else pathlib.Path.home() / ".claude/plan-review/jev.json"
    data, _ = json_file(path)
    return path, data if isinstance(data, dict) else {}


def registered(name):
    data, _ = json_file(pathlib.Path.home() / ".claude/plugins/installed_plugins.json")
    entries = (data or {}).get("plugins", {}) if isinstance(data, dict) else {}
    paths = []
    for key, installs in entries.items():
        if key.split("@")[0] != name or not isinstance(installs, list):
            continue
        for entry in installs:
            if isinstance(entry, dict) and isinstance(entry.get("installPath"), str):
                paths.append(pathlib.Path(entry["installPath"]).expanduser())
    return list(dict.fromkeys(paths))


def skill_at(root):
    if not root:
        return None
    root = pathlib.Path(root).expanduser().resolve()
    for plugin in (root, root / "plugins/sc-plan-anchor"):
        skill = plugin / "skills/plan-anchoring"
        if (plugin / "plugin.json").is_file() and (skill / "scripts/jev_judge.py").is_file():
            return skill
    return None


def find_install(explicit=None, settings=None):
    settings = settings or {}
    preferred = explicit or os.environ.get("PLAN_ANCHOR_ROOT") or os.environ.get("PLAN_REVIEW_PLAN_ANCHOR_ROOT") or settings.get("plan_anchor_root")
    if preferred:
        return pathlib.Path(preferred).expanduser().resolve() if skill_at(preferred) else None
    options = registered("sc-plan-anchor")
    options.append(pathlib.Path.home() / ".claude/plugins/marketplaces/sc-plan-anchor")
    matches = [p.resolve() for p in options if skill_at(p)]
    matches = list(dict.fromkeys(matches))
    return matches[0] if len(matches) == 1 else None


def adapter_path():
    for root in registered("plan-review"):
        path = root / "skills/adversarial-plan-review/scripts/jev-check.py"
        if path.is_file():
            return path
    return None


def plan_candidates(plan):
    """Only explicit local Markdown links and immediate conventional sidecars."""
    stem = plan.with_suffix("")
    outputs = pathlib.Path(str(stem) + ".jev")
    found = []
    def add(kind, path, provenance):
        if path.is_file() and not path.is_symlink():
            value = {"kind": kind, "path": str(path.resolve()), "sha256": digest(path), "provenance": provenance}
            existing = next((x for x in found if x["kind"] == kind and x["path"] == value["path"]), None)
            if existing is None:
                found.append(value)
            elif provenance == "explicit_markdown_reference":
                existing["provenance"] = provenance
    for kind in KINDS:
        ext = "md" if kind == "intent" else "json"
        for path in (pathlib.Path(str(stem) + f".{kind}.{ext}"), plan.parent / f"{kind}.{ext}",
                     outputs / ("authority.json" if kind == "anchors" else f"{kind}.{ext}")):
            add(kind, path, "conventional_sidecar")
    try:
        text = plan.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return found
    for raw in re.findall(r"\[[^\]\n]*\]\(([^)\n]+)\)", text):
        raw = raw.strip().strip("<>").split("#", 1)[0]
        if not raw or re.match(r"^[A-Za-z][A-Za-z0-9+.-]*:", raw) or pathlib.Path(raw).is_absolute():
            continue
        path = plan.parent / raw
        # References cannot authorize scanning outside the plan directory.
        if not path.resolve().is_relative_to(plan.parent.resolve()):
            continue
        name = path.name.lower()
        kind = next((k for k in KINDS if k in name), "anchors" if name == "authority.json" else None)
        if kind and path.suffix.lower() in (".json", ".md"):
            add(kind, path, "explicit_markdown_reference")
    return found


def safe_relative(raw, base):
    if not isinstance(raw, str) or not raw:
        raise ValueError("file reference must be a nonempty relative path")
    rel = pathlib.Path(raw)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError("file references cannot be absolute or traverse parents")
    path = base / rel
    if any((base / pathlib.Path(*rel.parts[:n])).is_symlink() for n in range(1, len(rel.parts) + 1)):
        raise ValueError("file references cannot contain symlinks")
    if not path.is_file():
        raise ValueError("referenced file missing")
    return path


def run_python(python, argv, **kwargs):
    env = dict(os.environ)
    env.pop("TYPESAFE_API_KEY", None)
    env.pop("PLAN_ANCHOR_ALLOW_REMOTE_JUDGE", None)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return subprocess.run([str(python), *map(str, argv)], capture_output=True, text=True,
                          timeout=30, env=env, **kwargs)


def validate_authority(authority, skill=None, python=None):
    if not isinstance(authority, dict) or not isinstance(authority.get("anchors"), list) or not authority["anchors"]:
        return ["authority must contain a nonempty anchors array"]
    skill = skill or pathlib.Path(__file__).resolve().parent.parent
    with tempfile.TemporaryDirectory() as td:
        source = pathlib.Path(td) / "anchors.json"
        source.write_text(json.dumps(authority), encoding="utf-8")
        run = run_python(python or sys.executable, [skill / "scripts/jev_judge.py", "validate", "--anchors", source])
    try:
        result = json.loads(run.stdout)
    except ValueError:
        return ["evaluator could not validate authority"]
    issues = (result.get("data") or {}).get("problems", [])
    if not result.get("success") and not issues:
        issues = ["evaluator rejected authority"]
    if not any(a.get("status") in ("locked", "promoted") for a in authority["anchors"] if isinstance(a, dict)):
        issues.append("authority needs at least one locked or promoted anchor")
    return issues


def validate_manifest(value, base, plan):
    if not isinstance(value, dict) or value.get("schema") != "plan-review/jev-items/1" or not value.get("items"):
        raise ValueError("nonempty plan-review/jev-items/1 manifest required")
    if set(value) - {"schema", "items", "shared_constraints"}:
        raise ValueError("unsupported manifest fields")
    seen, sources, texts = set(), [], []
    for entry in value["items"]:
        if not isinstance(entry, dict) or set(entry) - {"id", "path", "sha256", "title"}:
            raise ValueError("invalid item fields")
        ident = entry.get("id")
        if not isinstance(ident, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]{0,127}", ident) or ident in seen:
            raise ValueError("item IDs must be unique safe identifiers")
        seen.add(ident)
        source = safe_relative(entry.get("path"), base)
        if digest(source) != entry.get("sha256"):
            raise ValueError("item content hash missing or stale")
        text = source.read_text(encoding="utf-8")
        if not text.strip():
            raise ValueError("complete item cannot be empty")
        texts.append(text)
        sources.append(source.resolve())
    if plan.resolve() not in sources:
        raise ValueError("manifest must include original reviewed plan")
    for entry in value.get("shared_constraints", []):
        if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
            raise ValueError("invalid shared constraint")
        source = safe_relative(entry["path"], base)
        if digest(source) != entry["sha256"] or any(source.read_text(encoding="utf-8") not in text for text in texts):
            raise ValueError("shared constraint missing from complete items or stale")


def credential(settings):
    key = os.environ.get("TYPESAFE_API_KEY")
    source = "environment" if key is not None else None
    if key is None and isinstance(settings.get("credential_file"), str):
        try:
            path = pathlib.Path(settings["credential_file"]).expanduser()
            if path.stat().st_size > 65536:
                raise ValueError("credential provider too large")
            text = path.read_text(encoding="utf-8")
            values = {}
            for line in text.splitlines():
                match = re.fullmatch(r"\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*?)\s*", line)
                if match:
                    parts = shlex.split(match[2], comments=True)
                    if len(parts) == 1:
                        values[match[1]] = parts[0]
            name = values.get("API_KEY_ENV")
            key = values.get("TYPESAFE_API_KEY")
            if key is None and name is not None:
                key = values.get(name, name)
            source = "credential_file"
        except (OSError, UnicodeError, ValueError):
            pass
    valid = bool(key and key.isascii() and not any(ord(c) < 33 or ord(c) == 127 for c in key) and
                 not any(x in key for x in ("$", "`")))
    return {"credential_present": bool(key), "credential_format_valid": valid, "credential_source": source,
            "consent_for_this_process": os.environ.get("PLAN_ANCHOR_ALLOW_REMOTE_JUDGE") == "1"}


def bootstrap_capable(skill, python):
    if not skill:
        return False
    for name in ("request", "result"):
        schema, _ = json_file(skill / f"assets/schemas/anchor-tuning-{name}.schema.json")
        try:
            spec = schema["$defs"]["tuning_event"]["properties"]["supersedes"]
        except (KeyError, TypeError):
            # Find the named event definition without assuming its spelling.
            spec = next((v.get("properties", {}).get("supersedes") for v in (schema or {}).get("$defs", {}).values()
                         if isinstance(v, dict) and "supersedes" in v.get("properties", {})), None)
        if not spec:
            return False
        probe = run_python(python, ["-c", "import json,jsonschema,sys; jsonschema.Draft202012Validator(json.loads(sys.argv[1])).validate(None)", json.dumps(spec)])
        if probe.returncode:
            return False
    contract = skill / "scripts/anchor_tuning_contract.py"
    if not contract.is_file():
        return False
    probe = run_python(python, ["-c", "import runpy,sys; c=runpy.run_path(sys.argv[1]); c['validate_history']({'events':[{'event_index':1,'previous_event_sha256':None,'supersedes':None,'protocol_version':'plan-anchor/question-tournament/2.0.0'}]})", contract])
    return probe.returncode == 0


def selected_inputs(args, plan, candidates):
    saved, _ = json_file(pathlib.Path(str(plan.with_suffix("")) + ".jev") / "choices.json")
    saved = saved if isinstance(saved, dict) else {}
    resolved, questions = {}, []
    for kind in KINDS:
        raw = getattr(args, kind, None) or saved.get(kind)
        if raw:
            resolved[kind] = str(pathlib.Path(raw).expanduser().resolve())
            continue
        choices = [x for x in candidates if x["kind"] == kind]
        explicit = [x for x in choices if x["provenance"] == "explicit_markdown_reference"]
        choices = explicit or choices
        if len(choices) == 1:
            resolved[kind] = choices[0]["path"]
        elif len(choices) > 1:
            questions.append({"id": kind, "reason": "ambiguous candidates", "candidates": [x["path"] for x in choices]})
    resolved["model"] = args.model or saved.get("model")
    return resolved, questions


def inspect(args):
    plan = pathlib.Path(args.plan).expanduser().resolve()
    settings_path, settings = settings_for(args)
    root = find_install(args.plan_anchor_root, settings)
    skill = skill_at(root)
    python = pathlib.Path(args.python or settings.get("python") or sys.executable).expanduser().absolute()
    py_ok = python.is_file() and os.access(python, os.X_OK)
    deps, capabilities = {}, {}
    if py_ok:
        probe = run_python(python, ["-c", "import jsonschema; import importlib.metadata; print(importlib.metadata.version('jsonschema'))"])
        deps["jsonschema"] = {"available": probe.returncode == 0, "version": probe.stdout.strip() if probe.returncode == 0 else None}
    evaluator = skill / "scripts/jev_judge.py" if skill else None
    if evaluator and py_ok:
        help_run = run_python(python, [evaluator, "--help"])
        capabilities = {"help": help_run.returncode == 0, "judge": help_run.returncode == 0 and "judge" in help_run.stdout,
                        "tuning_contract": (skill / "scripts/anchor_tuning_contract.py").is_file(),
                        "bootstrap": bootstrap_capable(skill, python)}
    compose = settings.get("compose") or shutil.which("sc-compose")
    compose_ok, compose_version = False, None
    if compose and pathlib.Path(compose).is_file() and os.access(compose, os.X_OK):
        probe = subprocess.run([compose, "--version"], capture_output=True, text=True, timeout=10)
        match = re.search(r"\b(\d+)\.(\d+)\.(\d+)\b", probe.stdout)
        if probe.returncode == 0 and match:
            compose_version = match[0]
            compose_ok = tuple(map(int, match.groups())) >= (1, 6, 0)
    capabilities["native_templates"] = bool(skill and all((skill / "templates" / name).is_file() for name in
        ("anchor-tuning-tune-request.md.j2", "anchor-tuning-result.md.j2")))
    setup_ready = bool(plan.is_file() and skill and py_ok and compose_ok and deps.get("jsonschema", {}).get("available") and
                       all(capabilities.get(k) for k in ("help", "judge", "tuning_contract", "bootstrap", "native_templates")))
    candidates = plan_candidates(plan)
    resolved, questions = selected_inputs(args, plan, candidates)
    blockers, missing = [], []
    repairs = []
    if not compose_ok:
        blockers.append("sc-compose missing or older than 1.6.0")
        repairs.append({"id": "install-sc-compose", "kind": "dependency", "reason": "native calibration needs sc-compose >=1.6.0"})
    if skill and not capabilities["native_templates"]:
        blockers.append("native calibration templates missing")
    if not plan.is_file(): blockers.append("plan missing")
    if not root:
        blockers.append("installation missing or ambiguous")
        repairs.append({"id": "install-plan-anchor", "kind": "dependency", "reason": "select a trusted evaluator installation"})
        questions.append({"id": "plan_anchor_root", "reason": "select trusted installation"})
    if not py_ok: blockers.append("Python runtime unavailable")
    if not deps.get("jsonschema", {}).get("available"):
        blockers.append("jsonschema unavailable")
        repairs.append({"id": "install-jsonschema", "kind": "dependency", "reason": "selected interpreter cannot import jsonschema"})
    if skill and not capabilities.get("bootstrap"): blockers.append("native bootstrap unsupported")
    if skill and py_ok and not all(capabilities.get(k) for k in ("help", "judge", "tuning_contract")):
        blockers.append("evaluator capabilities incomplete")
    authority, authority_issues = None, []
    for kind in KINDS:
        if not resolved.get(kind):
            missing.append(kind)
            blockers.append(f"{kind} missing or ambiguous")
    if resolved.get("anchors"):
        authority, _ = json_file(resolved["anchors"])
        authority_issues = validate_authority(authority, skill, python) if setup_ready else ["authority validation unavailable"]
        if authority_issues: blockers.append("authority invalid")
    if resolved.get("intent"):
        try:
            if not pathlib.Path(resolved["intent"]).read_text(encoding="utf-8").strip(): blockers.append("intent empty")
        except (OSError, UnicodeError): blockers.append("intent unreadable")
    if resolved.get("items"):
        manifest, _ = json_file(resolved["items"])
        try: validate_manifest(manifest, pathlib.Path(resolved["items"]).parent, plan)
        except (ValueError, OSError, UnicodeError, TypeError): blockers.append("items invalid or stale")
    approval, _ = json_file(pathlib.Path(str(plan.with_suffix("")) + ".jev") / "authority-approval.json")
    current = bool(isinstance(approval, dict) and approval.get("approved") is True and digest(plan) and
                   resolved.get("anchors") and resolved.get("intent") and
                   approval.get("authority_sha256") == digest(resolved["anchors"]) and
                   approval.get("intent_sha256") == digest(resolved["intent"]))
    if not current: blockers.append("authority approval missing or stale")
    seal, _ = json_file(resolved.get("seal"))
    if isinstance(seal, dict) and seal.get("schema") == "plan-review/jev-seal/1" and seal.get("anchors_sha256") == digest(resolved.get("anchors")) and seal.get("intent_sha256") == digest(resolved.get("intent")):
        resolved["model"] = resolved.get("model") or seal.get("model")
    if not resolved.get("model") or resolved.get("model") == "jev-latest":
        missing.append("model")
        blockers.append("concrete model pin missing")
    defaults = {k: getattr(args, k, None) if getattr(args, k, None) is not None else settings.get(k, v) for k, v in DEFAULTS.items()}
    if (args.threshold is None and isinstance(seal, dict)
            and seal.get("anchors_sha256") == digest(resolved.get("anchors"))
            and seal.get("intent_sha256") == digest(resolved.get("intent"))
            and seal.get("model") == resolved.get("model")):
        defaults["threshold"] = seal.get("threshold", defaults["threshold"])
    for key in ("jobs", "request_budget", "calibration_budget"):
        if type(defaults[key]) is not int or defaults[key] < 1: raise ValueError("invalid request budget or concurrency")
    if type(defaults["threshold"]) not in (int, float) or not 0 <= defaults["threshold"] <= 1: raise ValueError("invalid threshold")
    adapter = adapter_path()
    # Verify all native evidence with the installed adapter's dry-run path, temp-only.
    if resolved.get("seal"):
        if not adapter:
            blockers.append("calibration verifier unavailable")
        elif setup_ready and not any(k in missing for k in (*KINDS, "model")) and not authority_issues:
            with tempfile.TemporaryDirectory() as td:
                argv = [adapter, "--plan-anchor-root", root, "--anchors", resolved["anchors"], "--intent", resolved["intent"],
                        "--items", resolved["items"], "--seal", resolved["seal"], "--model", resolved["model"], "--source-plan", plan,
                        "--out", td, "--dry-run", "--threshold", str(defaults["threshold"])]
                probe = run_python(python, argv)
                if probe.returncode: blockers.append("calibration seal invalid or stale")
    remote = credential(settings)
    remote["consent_for_this_process"] = remote["consent_for_this_process"] or getattr(args, "allow_remote", False)
    if not remote["credential_format_valid"]: blockers.append("remote credential missing or invalid")
    if not remote["consent_for_this_process"]: blockers.append("session remote consent missing")
    adapter_args = {"plan_anchor_root": str(root) if root else None, "source_plan": str(plan), **resolved,
                    "jobs": defaults["jobs"], "request_budget": defaults["request_budget"], "threshold": defaults["threshold"]}
    return {"schema": "plan-anchor/jev-setup/1", "operation": args.operation,
            "plan": {"path": str(plan), "exists": plan.is_file(), "sha256": digest(plan)},
            "installation": {"root": str(root) if root else None, "available": bool(skill),
                             "evaluator": str(evaluator) if evaluator else None, "evaluator_sha256": digest(evaluator), "capabilities": capabilities},
            "runtime": {"python": str(python), "available": py_ok, "dependencies": deps,
                        "sc_compose": {"path": compose, "version": compose_version, "available": compose_ok}},
            "settings": str(settings_path), "inputs": candidates, "resolved": {**adapter_args, "python": str(python),
            "credential_file": settings.get("credential_file"), "compose": compose, "missing_fields": missing,
            "adapter_args": [part for key, value in adapter_args.items() if value is not None
                             for part in ("--" + key.replace("_", "-"), str(value))]},
            "defaults": defaults, "remote": remote, "proposed_repairs": repairs, "questions": questions,
            "setup_ready": setup_ready, "runnable": not blockers, "remaining_blockers": blockers,
            "authority_issues": authority_issues, "authority_approved_current": current, "judgment": "not_run"}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def prepare(args):
    plan = pathlib.Path(args.plan).expanduser().resolve()
    if not plan.is_file() or plan.is_symlink(): raise ValueError("plan must be an existing nonsymlink file")
    choices, error = json_file(args.resolutions)
    if error or not isinstance(choices, dict): raise ValueError("explicit resolutions JSON object required")
    settings_path, old = settings_for(args)
    root = find_install(choices.get("plan_anchor_root") or args.plan_anchor_root, old)
    skill = skill_at(root)
    if not skill: raise ValueError("selected installation has no evaluator")
    python = pathlib.Path(choices.get("python") or args.python or old.get("python") or sys.executable).expanduser().absolute()
    if not python.is_file() or not os.access(python, os.X_OK): raise ValueError("Python runtime unavailable")
    settings = {"plan_anchor_root": str(root), "python": str(python), **{k: choices.get(k, getattr(args, k, None) if getattr(args, k, None) is not None else old.get(k, v)) for k, v in DEFAULTS.items()}}
    if old.get("compose"):
        settings["compose"] = str(pathlib.Path(old["compose"]).expanduser().absolute())
    for k in ("jobs", "request_budget", "calibration_budget"):
        if type(settings[k]) is not int or settings[k] < 1: raise ValueError(f"{k} must be a positive integer")
    if type(settings["threshold"]) not in (int, float) or not 0 <= settings["threshold"] <= 1: raise ValueError("threshold must be between zero and one")
    credential_file = choices.get("credential_file", old.get("credential_file"))
    if credential_file is not None:
        if not isinstance(credential_file, str): raise ValueError("credential_file must be a path")
        settings["credential_file"] = str(pathlib.Path(credential_file).expanduser().resolve())
    artifacts = pathlib.Path(str(plan.with_suffix("")) + ".jev")
    candidates = plan_candidates(plan)
    existing, _ = selected_inputs(args, plan, candidates)
    authority = choices.get("authority")
    anchors_path = pathlib.Path(choices.get("anchors") or existing.get("anchors") or artifacts / "authority.json").expanduser().resolve()
    if authority is None: authority, _ = json_file(anchors_path)
    issues = validate_authority(authority, skill, python)
    if issues: raise ValueError("; ".join(issues))
    intent = choices.get("intent_text")
    intent_path = pathlib.Path(choices.get("intent") or existing.get("intent") or artifacts / "intent.md").expanduser().resolve()
    if intent is None:
        try: intent = intent_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError): raise ValueError("intent text or existing intent file required")
    if not isinstance(intent, str) or not intent.strip(): raise ValueError("nonempty intent required")
    manifest_path = pathlib.Path(str(plan.with_suffix("")) + ".items.json")
    items = choices.get("items")
    if items is None:
        manifest_path = pathlib.Path(existing.get("items") or manifest_path)
        manifest, _ = json_file(manifest_path)
    elif isinstance(items, str):
        manifest_path = pathlib.Path(items).expanduser().resolve()
        manifest, _ = json_file(manifest_path)
    elif isinstance(items, list):
        records = []
        for entry in items:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str): raise ValueError("invalid item")
            source = pathlib.Path(entry["path"]).expanduser()
            if not source.is_absolute(): source = plan.parent / source
            if source.is_symlink(): raise ValueError("item cannot be symlink")
            source = source.resolve()
            try: rel = str(source.relative_to(manifest_path.parent))
            except ValueError: raise ValueError("item must be within plan directory")
            records.append({"id": entry.get("id"), "path": rel, "sha256": digest(source), **({"title": entry["title"]} if "title" in entry else {})})
        manifest = {"schema": "plan-review/jev-items/1", "items": records}
    else: raise ValueError("items must be a manifest path or item list")
    validate_manifest(manifest, manifest_path.parent, plan)
    selected = {"anchors": str(anchors_path), "intent": str(intent_path), "items": str(manifest_path)}
    for k in ("seal", "model"):
        raw = choices.get(k) or existing.get(k)
        if raw:
            if not isinstance(raw, str): raise ValueError("seal and model must be strings")
            selected[k] = str(pathlib.Path(raw).expanduser().resolve()) if k == "seal" else raw
    if choices.get("authority_approved") is not True: raise ValueError("explicit authority and intent approval required")
    # No user-state writes occur before all validation and approval checks above.
    write(settings_path, settings)
    write(anchors_path, authority)
    intent_path.parent.mkdir(parents=True, exist_ok=True)
    intent_path.write_text(intent, encoding="utf-8")
    write(manifest_path, manifest)
    write(artifacts / "choices.json", selected)
    write(artifacts / "authority-approval.json", {"approved": True, "plan_sha256": digest(plan),
          "authority_sha256": digest(anchors_path), "intent_sha256": digest(intent_path)})
    return {"schema": "plan-anchor/jev-setup/1", "operation": "prepare", "prepared": True,
            "settings": str(settings_path), "artifacts": str(artifacts), "choices": selected,
            "resolved": {**selected, **settings, "adapter_args": [part for key, value in {"plan_anchor_root": str(root), "source_plan": str(plan), **selected, "jobs": settings["jobs"], "request_budget": settings["request_budget"], "threshold": settings["threshold"]}.items()
                                                               for part in ("--" + key.replace("_", "-"), str(value))]},
            "approval": {"approved": True, "plan_sha256": digest(plan), "authority_sha256": digest(anchors_path), "intent_sha256": digest(intent_path)}, "judgment": "not_run"}


def status(args):
    return inspect(args)


def refresh(args):
    report = inspect(args)
    if not report["setup_ready"] or not report["authority_approved_current"]:
        raise ValueError("current approved authority and runtime required")
    plan = pathlib.Path(args.plan).expanduser().resolve()
    if not report["resolved"].get("items"):
        raise ValueError("current item manifest required")
    path = pathlib.Path(report["resolved"]["items"])
    manifest, error = json_file(path)
    if error or not isinstance(manifest, dict):
        raise ValueError("current item manifest required")
    for entry in manifest.get("items", []) + manifest.get("shared_constraints", []):
        source = safe_relative(entry.get("path"), path.parent)
        entry["sha256"] = digest(source)
    validate_manifest(manifest, path.parent, plan)
    write(path, manifest)
    return {"schema": "plan-anchor/jev-setup/1", "operation": "refresh", "prepared": True,
            "refreshed": True, "resolved": report["resolved"], "manifest": str(path),
            "judgment": "not_run"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("operation", choices=("inspect", "prepare", "refresh", "status"))
    parser.add_argument("--plan", required=True)
    parser.add_argument("--allow-remote", action="store_true", help="consent for this invocation only")
    for name in ("plan-anchor-root", "python", "resolutions", "settings", "anchors", "intent", "items", "seal", "model"):
        parser.add_argument("--" + name)
    for name in ("jobs", "request-budget", "calibration-budget"):
        parser.add_argument("--" + name, type=int)
    parser.add_argument("--threshold", type=float)
    args = parser.parse_args()
    try:
        result = {"prepare": prepare, "refresh": refresh}.get(args.operation, inspect)(args)
        print(json.dumps(result, sort_keys=True))
        ready = result.get("prepared") if args.operation in ("prepare", "refresh") else result["runnable"] if args.operation == "status" else result["setup_ready"]
        return 0 if ready else 1
    except (OSError, ValueError, TypeError, subprocess.SubprocessError):
        # Never echo exception text: a credential path or invalid secret must not leak.
        print(json.dumps({"schema": "plan-anchor/jev-setup/1", "success": False,
                          "error": {"code": "SETUP.INVALID", "message": "Invalid setup inputs; no remote judgment was run"}}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
