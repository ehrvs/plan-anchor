import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
SETUP = ROOT / "plugins/sc-plan-anchor/skills/plan-anchoring/scripts/jev-setup.py"
spec = importlib.util.spec_from_file_location("jev_setup", SETUP)
setup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(setup)


def authority():
    return {"schema": "plan-anchoring/anchors/1", "anchors": [
        {"id": "REQ-003", "source_type": "REQ", "source_ref": "REQ-003", "statement": "Keep the API stable.",
         "status": "locked", "stated_at": "2026-10-14", "kind": "directive"}]}


class JevSetupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.plan = self.home / "plan.md"
        self.plan.write_text("# Plan\nKeep the API stable.\n", encoding="utf-8")
        self.settings = self.home / "settings.json"
        self.resolutions = self.home / "resolution.json"
        self.env = {k: v for k, v in os.environ.items() if k not in ("TYPESAFE_API_KEY", "PLAN_ANCHOR_ALLOW_REMOTE_JUDGE", "PLAN_ANCHOR_ROOT", "PLAN_REVIEW_PLAN_ANCHOR_ROOT")}
        self.env["PYTHONDONTWRITEBYTECODE"] = "1"

    def run_helper(self, operation, *extra):
        run = subprocess.run([sys.executable, str(SETUP), operation, "--plan", str(self.plan),
                              "--settings", str(self.settings), *extra], env=self.env, capture_output=True, text=True)
        self.assertEqual(run.stderr, "")
        return run.returncode, json.loads(run.stdout)

    def prepare(self, **overrides):
        choices = {"plan_anchor_root": str(ROOT), "python": sys.executable, "authority": authority(),
                   "intent_text": "Keep client compatibility.\n", "items": [{"id": "plan", "path": str(self.plan)}],
                   "authority_approved": True, **overrides}
        self.resolutions.write_text(json.dumps(choices), encoding="utf-8")
        return self.run_helper("prepare", "--resolutions", str(self.resolutions))

    def test_inspect_separates_mechanical_readiness_and_judgment(self):
        code, data = self.run_helper("inspect", "--plan-anchor-root", str(ROOT))
        self.assertEqual(code, 0)
        self.assertTrue(data["setup_ready"])
        self.assertFalse(data["runnable"])
        self.assertEqual(data["judgment"], "not_run")
        self.assertFalse(data["remote"]["credential_present"])
        self.assertIn("seal", data["resolved"]["missing_fields"])

    def test_approval_binds_authority_intent_and_keeps_plan_provenance(self):
        code, prepared = self.prepare()
        self.assertEqual(code, 0)
        self.assertTrue(prepared["prepared"])
        code, current = self.run_helper("status")
        self.assertEqual(code, 1)  # no seal or live credentials
        self.assertTrue(current["authority_approved_current"])
        self.assertEqual(current["resolved"]["plan_anchor_root"], str(ROOT))
        self.assertEqual(current["runtime"]["python"], str(Path(sys.executable).absolute()))
        intent = Path(current["resolved"]["intent"])
        intent.write_text("Changed intent\n")
        _, stale = self.run_helper("status")
        self.assertFalse(stale["authority_approved_current"])
        intent.write_text("Keep client compatibility.\n")
        self.plan.write_text("# Changed plan\n")
        _, stale = self.run_helper("status")
        self.assertTrue(stale["authority_approved_current"])
        self.assertIn("items invalid or stale", stale["remaining_blockers"])
        anchors = Path(stale["resolved"]["anchors"])
        changed = json.loads(anchors.read_text())
        changed["anchors"][0]["statement"] = "A new authority requirement."
        anchors.write_text(json.dumps(changed))
        _, stale = self.run_helper("status")
        self.assertFalse(stale["authority_approved_current"])

    def test_invalid_prepare_has_no_writes(self):
        code, data = self.prepare(authority={"anchors": []})
        self.assertEqual(code, 2)
        self.assertFalse(self.settings.exists())
        self.assertFalse((self.home / "plan.jev").exists())
        self.assertFalse((self.home / "plan.items.json").exists())
        self.assertFalse(data["success"])
        code, _ = self.prepare(items=[{"id": "plan", "path": str(self.home / "missing.md")}])
        self.assertEqual(code, 2)
        self.assertFalse(self.settings.exists())
        code, _ = self.prepare(authority_approved=False)
        self.assertEqual(code, 2)
        self.assertFalse(self.settings.exists())

    def test_authority_uses_actual_evaluator_contract(self):
        self.assertTrue(setup.validate_authority({"anchors": []}))
        self.assertTrue(setup.validate_authority({"anchors": [{"id": "REQ-003", "statement": "Keep API"}]}))
        self.assertEqual(setup.validate_authority(authority()), [])
        duplicate = authority()
        duplicate["anchors"] *= 2
        self.assertTrue(any("duplicate" in x for x in setup.validate_authority(duplicate)))

    def test_manifest_has_relative_path_hash_and_rejects_unsafe_sources(self):
        code, _ = self.prepare()
        self.assertEqual(code, 0)
        manifest = json.loads((self.home / "plan.items.json").read_text())
        self.assertEqual(manifest["items"][0]["path"], "plan.md")
        self.assertEqual(manifest["items"][0]["sha256"], setup.digest(self.plan))
        setup.validate_manifest(manifest, self.home, self.plan)
        for path in (str(self.plan), "../plan.md"):
            manifest["items"][0]["path"] = path
            with self.assertRaises(ValueError): setup.validate_manifest(manifest, self.home, self.plan)
        linked = self.home / "link.md"
        linked.symlink_to(self.plan)
        manifest["items"][0]["path"] = "link.md"
        with self.assertRaises(ValueError): setup.validate_manifest(manifest, self.home, self.plan)

    def test_native_compose_dependency_is_a_reported_repair(self):
        self.env["PATH"] = ""
        code, data = self.run_helper("inspect", "--plan-anchor-root", str(ROOT))
        self.assertEqual(code, 1)
        self.assertFalse(data["setup_ready"])
        self.assertFalse(data["runtime"]["sc_compose"]["available"])
        self.assertTrue(any(x["id"] == "install-sc-compose" for x in data["proposed_repairs"]))

    def test_saved_python_is_honored(self):
        code, _ = self.prepare()
        self.assertEqual(code, 0)
        settings = json.loads(self.settings.read_text())
        settings["python"] = str(self.home / "missing-python")
        self.settings.write_text(json.dumps(settings))
        code, data = self.run_helper("inspect")
        self.assertEqual(code, 1)
        self.assertFalse(data["runtime"]["available"])
        self.assertEqual(data["runtime"]["python"], str(Path(settings["python"]).absolute()))

    def test_plugin_and_repository_install_layouts_and_registry_discovery(self):
        plugin = ROOT / "plugins/sc-plan-anchor"
        self.assertEqual(setup.skill_at(plugin), setup.skill_at(ROOT))
        registry = self.home / ".claude/plugins/installed_plugins.json"
        registry.parent.mkdir(parents=True)
        registry.write_text(json.dumps({"plugins": {"sc-plan-anchor@example": [{"scope": "user", "installPath": str(plugin)}]}}))
        with patch.object(setup.pathlib.Path, "home", return_value=self.home), patch.dict(os.environ, {}, clear=True):
            self.assertEqual(setup.find_install(), plugin.resolve())
            self.assertIsNone(setup.find_install(str(self.home / "invalid")))

    def test_bootstrap_requires_null_supersedes_not_version_string(self):
        skill = self.home / "fake-skill"
        (skill / "assets/schemas").mkdir(parents=True)
        for name in ("request", "result"):
            schema = {"$defs": {"event": {"properties": {"supersedes": {"type": "object"}}, "description": "plan-anchor/tuning-history/2"}}}
            (skill / f"assets/schemas/anchor-tuning-{name}.schema.json").write_text(json.dumps(schema))
        self.assertFalse(setup.bootstrap_capable(skill, sys.executable))
        self.assertTrue(setup.bootstrap_capable(setup.skill_at(ROOT), sys.executable))

    def test_candidates_bounded_references_and_ambiguity(self):
        (self.home / "anchors.json").write_text("{}")
        (self.home / "plan.anchors.json").write_text("{}")
        self.plan.write_text("[anchors](anchors.json)\n[escape](../private-anchors.json)\n[external](https://example.com/anchors.json)\n")
        candidates = setup.plan_candidates(self.plan)
        self.assertEqual(len(candidates), 2)
        self.assertTrue(any(x["provenance"] == "conventional_sidecar" for x in candidates))
        self.plan.write_text("# Plan\n")
        _, data = self.run_helper("inspect", "--plan-anchor-root", str(ROOT))
        self.assertTrue(any(x["id"] == "anchors" for x in data["questions"]))
        self.assertNotIn("anchors", {k for k, v in data["resolved"].items() if v is not None})

    def test_stale_seal_cannot_become_runnable(self):
        seal = self.home / "seal.json"
        seal.write_text(json.dumps({"schema": "plan-review/jev-seal/1", "model": "jev-test-pin", "anchors_sha256": "0" * 64, "intent_sha256": "0" * 64}))
        code, _ = self.prepare(seal=str(seal), model="jev-test-pin")
        self.assertEqual(code, 0)
        self.env["TYPESAFE_API_KEY"] = "test-only-key"
        code, data = self.run_helper("status", "--allow-remote")
        self.assertEqual(code, 1)
        self.assertFalse(data["runnable"])
        self.assertTrue(any("calibration" in blocker for blocker in data["remaining_blockers"]))

    def test_cli_policy_overrides_are_resolved_and_validated(self):
        _, data = self.run_helper("inspect", "--plan-anchor-root", str(ROOT), "--jobs", "2", "--request-budget", "55", "--threshold", "0.7")
        self.assertEqual(data["resolved"]["jobs"], 2)
        self.assertEqual(data["resolved"]["request_budget"], 55)
        self.assertEqual(data["resolved"]["threshold"], 0.7)
        self.assertIn("--jobs", data["resolved"]["adapter_args"])
        code, _ = self.run_helper("inspect", "--plan-anchor-root", str(ROOT), "--jobs", "0")
        self.assertEqual(code, 2)

    def test_credential_file_is_silent_env_wins_and_no_consent_saved(self):
        secret = "test-only-key-value"
        dotenv = self.home / ".env"
        dotenv.write_text("API_KEY_ENV=PRIVATE_TEST_KEY\nPRIVATE_TEST_KEY='" + secret + "'\n")
        self.prepare(credential_file=str(dotenv))
        _, data = self.run_helper("inspect", "--allow-remote")
        self.assertTrue(data["remote"]["credential_present"])
        self.assertTrue(data["remote"]["consent_for_this_process"])
        self.assertNotIn(secret, json.dumps(data))
        dotenv.write_text("export API_KEY_ENV='" + secret + "' # a literal key\n")
        _, literal = self.run_helper("inspect")
        self.assertTrue(literal["remote"]["credential_format_valid"])
        self.assertNotIn(secret, json.dumps(literal))
        _, data = self.run_helper("inspect")
        self.assertFalse(data["remote"]["consent_for_this_process"])
        self.env["TYPESAFE_API_KEY"] = ""
        _, data = self.run_helper("inspect")
        self.assertFalse(data["remote"]["credential_present"])
        self.assertEqual(data["remote"]["credential_source"], "environment")
        self.assertNotIn("consent", self.settings.read_text())

    def test_selected_venv_executable_preserves_environment(self):
        runtime = self.home / "venv"
        venv.EnvBuilder(with_pip=False).create(runtime)
        python = runtime / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        _, data = self.run_helper("inspect", "--plan-anchor-root", str(ROOT), "--python", str(python))
        self.assertEqual(data["runtime"]["python"], str(python.absolute()))
        probe = setup.run_python(data["runtime"]["python"], ["-c", "import sys; print(sys.prefix)"])
        self.assertEqual(Path(probe.stdout.strip()).resolve(), runtime.resolve())

    def test_bound_seal_threshold_precedes_machine_default(self):
        _, prepared = self.prepare()
        values = prepared["resolved"]
        seal = self.home / "plan.jev/seal.json"
        seal.write_text(json.dumps({"schema": "plan-review/jev-seal/1",
                                   "anchors_sha256": setup.digest(values["anchors"]),
                                   "intent_sha256": setup.digest(values["intent"]),
                                   "model": "jev-1.13.0", "threshold": 0.7,
                                   "calibrations": []}))
        _, report = self.run_helper("inspect")
        self.assertEqual(report["resolved"]["threshold"], 0.7)
        _, explicit = self.run_helper("inspect", "--threshold", "0.8")
        self.assertEqual(explicit["resolved"]["threshold"], 0.8)

    def test_refresh_rehashes_declared_items_without_authority_changes(self):
        _, prepared = self.prepare()
        approval = self.home / "plan.jev/authority-approval.json"
        before = approval.read_bytes()
        self.plan.write_text("# Repaired plan\nKeep the API stable with compatibility tests.\n")
        code, result = self.run_helper("refresh")
        self.assertEqual(code, 0)
        self.assertTrue(result["refreshed"])
        self.assertEqual(approval.read_bytes(), before)
        manifest = json.loads(Path(prepared["resolved"]["items"]).read_text())
        self.assertEqual(manifest["items"][0]["sha256"], setup.digest(self.plan))
        _, report = self.run_helper("status")
        self.assertTrue(report["authority_approved_current"])
        self.assertNotIn("items invalid or stale", report["remaining_blockers"])

    def test_registered_renderer_survives_minimal_path_and_prepare(self):
        self.settings.write_text(json.dumps({"compose": shutil.which("sc-compose")}))
        self.prepare()
        self.env["PATH"] = ""
        _, report = self.run_helper("inspect")
        self.assertTrue(report["runtime"]["sc_compose"]["available"])


if __name__ == "__main__":
    unittest.main()
