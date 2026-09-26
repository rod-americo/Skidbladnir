from __future__ import annotations

import json
from pathlib import Path
import re
import runpy
import sys
import tempfile
import unittest
from unittest.mock import patch

from scaffold_project import CATALOG, RUNTIMES, render_and_write_templates, runtime_commands
from test_starter_regression import NEWPROJ, SCAFFOLDER, STARTER_ROOT, run_cmd


class RuntimeContractsTests(unittest.TestCase):
    def test_generation_requires_explicit_runtime_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "absent"
            for tool in (SCAFFOLDER, NEWPROJ):
                for preset in ("base", "fastapi", "worker"):
                    result = run_cmd([sys.executable, str(tool), str(repo), "--preset", preset], expected=1)
                    self.assertIn("--runtime", result.stderr)
                    self.assertFalse(repo.exists())
                for flag in ("--help", "--version", "--list-presets"):
                    run_cmd([sys.executable, str(tool), flag])
            presets = run_cmd([sys.executable, str(NEWPROJ), "--list-presets"]).stdout
            self.assertIn("java: base", presets)
            self.assertIn("rust: base", presets)
            run_cmd([sys.executable, str(SCAFFOLDER), str(repo), "--runtime", "rust", "--preset", "fastapi"], expected=1)
            self.assertFalse(repo.exists())

    def test_all_baselines_generate_offline_with_coherent_commands(self) -> None:
        doctor = runpy.run_path(str(STARTER_ROOT / "templates/scripts/project_doctor.py"))
        validator = runpy.run_path(str(STARTER_ROOT / "templates/scripts/check_deploy_manifest.py"))
        with tempfile.TemporaryDirectory() as tmp:
            for runtime in RUNTIMES:
                with self.subTest(runtime=runtime):
                    repo = Path(tmp) / runtime
                    with patch("socket.socket", side_effect=AssertionError("generation must stay offline")):
                        render_and_write_templates(repo, runtime, "base", "Contract", "contract", "https://github.com/example/contract", False, False, True)
                    manifest = json.loads((repo / "deploy/manifest.json").read_text())
                    self.assertEqual(manifest["runtime"], {"id": runtime, "version": RUNTIMES[runtime]["version"]})
                    self.assertEqual(manifest["deploy"]["target"], "none")
                    self.assertEqual(manifest["runtime_state"]["paths"], [])
                    self.assertEqual(manifest["logs"]["paths"], [])
                    self.assertEqual(manifest["healthcheck"], {})
                    self.assertEqual(validator["validate_operational_rules"](manifest), [])
                    commands = runtime_commands(runtime, "contract")
                    agents = (repo / "AGENTS.md").read_text()
                    self.assertEqual(doctor["extract_agents_validation"](agents), commands["test"])
                    operations = (repo / "docs/OPERATIONS.md").read_text()
                    self.assertIn(commands["test"], operations)
                    self.assertIn(commands["smoke"], operations)
                    if runtime != "generic":
                        self.assertEqual(manifest["process"]["command"], commands["run"])
                        workflow = (repo / ".github/workflows/ci.yml").read_text()
                        self.assertIn(commands["test"], workflow)
                        self.assertIn("contents: read", workflow)
                        self.assertNotIn("{{", workflow)
                        self.assertIn(CATALOG['actions']['python'], workflow)
                        for ref in re.findall(r"uses: (\S+)", workflow):
                            self.assertRegex(ref, r"@[a-f0-9]{40}$")
                    if runtime == "java":
                        self.assertTrue((repo / "mvnw").stat().st_mode & 0o111)
                        self.assertIn("3.9.16", (repo / ".mvn/wrapper/maven-wrapper.properties").read_text())
                    if runtime == "rust":
                        self.assertTrue((repo / "Cargo.lock").exists())
                        self.assertIn('unsafe_code = "forbid"', (repo / "Cargo.toml").read_text())

    def test_http_and_worker_operation_reflect_the_code(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            for preset in ("fastapi", "worker", "playwright_worker"):
                repo = Path(tmp) / preset
                render_and_write_templates(repo, "python", preset, "Contract", "contract", "", False, False, False)
                manifest = json.loads((repo / "deploy/manifest.json").read_text())
                if preset == "fastapi":
                    self.assertEqual(manifest["deploy"]["target"], "local")
                    self.assertEqual(manifest["ports"], [8000])
                    self.assertEqual(manifest["healthcheck"]["http"]["url"], "http://127.0.0.1:8000/health")
                else:
                    self.assertEqual(manifest["deploy"]["target"], "none")
                    self.assertIn("probe seguro", manifest["deploy"]["reason"])

    def test_legacy_and_additional_manifest_runtime_ids(self) -> None:
        validator = runpy.run_path(str(STARTER_ROOT / "templates/scripts/check_deploy_manifest.py"))
        schema = json.loads((STARTER_ROOT / "schema/deploy-manifest.schema.json").read_text())
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            render_and_write_templates(repo, "node", "base", "Contract", "contract", "", False, False, False)
            payload = json.loads((repo / "deploy/manifest.json").read_text())
            for runtime in ("node", "js", "java", "rust", "elixir"):
                payload['runtime']['id'] = runtime
                errors = []
                validator['validate_schema'](payload, schema, '$', errors)
                self.assertEqual(errors + validator['validate_operational_rules'](payload), [])
            marker = repo / 'must-not-exist'
            payload['healthcheck'] = {'command': f'touch {marker}'}
            self.assertEqual(validator['validate_operational_rules'](payload), [])
            self.assertFalse(marker.exists())

    def test_missing_toolchain_fails_runtime_checks(self) -> None:
        import run_runtime_checks
        with patch('run_runtime_checks.shutil.which', return_value=None):
            with self.assertRaisesRegex(RuntimeError, 'toolchain obrigatória ausente'):
                run_runtime_checks.check_toolchain('java', {'PATH': ''})

    def test_toolchain_version_check_uses_catalog_exactly(self) -> None:
        import run_runtime_checks
        with patch('run_runtime_checks.shutil.which', return_value='/tool'):
            with patch('run_runtime_checks.run', return_value='Apple Swift version 6.4 (build)'):
                run_runtime_checks.check_toolchain('swift', {'PATH': ''})
                with patch.dict(RUNTIMES['swift'], version='6.5.0'):
                    with self.assertRaisesRegex(RuntimeError, 'esperado 6.5.0'):
                        run_runtime_checks.check_toolchain('swift', {'PATH': ''})
            with patch('run_runtime_checks.run', return_value='rustc 1.98.1-nightly'):
                with self.assertRaisesRegex(RuntimeError, 'esperado 1.98.1'):
                    run_runtime_checks.check_toolchain('rust', {'PATH': ''})


if __name__ == '__main__':
    unittest.main()
