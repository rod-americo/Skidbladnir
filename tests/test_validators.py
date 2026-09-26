from __future__ import annotations

import json
from pathlib import Path
import runpy
import sys
import tempfile
import unittest

from test_starter_regression import SCAFFOLDER, STARTER_ROOT, run_cmd, write_valid_docs


class ValidatorTests(unittest.TestCase):
    def test_gate_v2_adds_evidence_without_rejecting_legacy_fields(self) -> None:
        gate = runpy.run_path(str(STARTER_ROOT / "templates/scripts/check_project_gate.py"))
        fields = {
            gate["normalize_label"](label): "Operação local com contratos explícitos e validação automatizada verificável."
            for label in gate["FIELD_RULES"]
        }
        self.assertEqual(gate["classify_fields"](fields), ([], [], []))
        pending, weak, short = gate["classify_fields"](fields, version=2)
        self.assertEqual(set(pending), set(gate["V2_FIELD_RULES"]))
        self.assertEqual(weak + short, [])

    def test_filled_real_gate_accepts_accents_and_spacing(self) -> None:
        gate = runpy.run_path(str(STARTER_ROOT / "templates/scripts/check_project_gate.py"))
        template = (STARTER_ROOT / "templates/common/PROJECT_GATE.md").read_text()
        filled = "\n".join(
            line.partition(":")[0] + ": Operação local com contratos explícitos e validação automatizada verificável."
            if line.startswith("- ") and ":" in line else line
            for line in template.splitlines()
        )
        for value in (filled, filled.replace("usuário ou operador", "  USUARIO   ou   operador")):
            with self.subTest(value=value[:20]):
                self.assertEqual(gate["classify_fields"](gate["collect_fields"](value), version=2), ([], [], []))

    def test_agents_template_validation_keeps_command_unchanged(self) -> None:
        doctor = runpy.run_path(str(STARTER_ROOT / "templates/scripts/project_doctor.py"))
        template = (STARTER_ROOT / "templates/common/AGENTS.md").read_text()
        command = 'python -m MinhaApp --config "config/Ação.json"'
        template = template.replace("{{VALIDACAO_MINIMA}}", command)
        self.assertEqual(doctor["extract_agents_validation"](template), command)
        self.assertEqual(doctor["extract_agents_validation"](template.replace("validação mínima", "validacao minima")), command)

    def test_http_healthcheck_requires_usable_url(self) -> None:
        validator = runpy.run_path(str(STARTER_ROOT / "templates/scripts/check_deploy_manifest.py"))
        scaffold = runpy.run_path(str(SCAFFOLDER))
        payload = scaffold["default_deploy_manifest"]("python", "Review", "review", "base")
        payload["deploy"]["target"] = "local"
        for url in (None, "", "file:///tmp/health", "http://", "http://localhost:99999", "https://user:secret@example.com", "http://local host"):
            payload["healthcheck"] = {"http": {} if url is None else {"url": url}}
            with self.subTest(url=url):
                self.assertTrue(validator["validate_operational_rules"](payload))
        for url in ("http://127.0.0.1:8000/health", "https://example.com/ready"):
            payload["healthcheck"] = {"http": {"url": url}}
            self.assertEqual(validator["validate_operational_rules"](payload), [])
        payload["deploy"]["target"] = "none"
        payload["process"] = {}
        payload["healthcheck"] = {}
        self.assertEqual(validator["validate_operational_rules"](payload), [])
        payload["healthcheck"] = {"command": "  "}
        self.assertTrue(validator["validate_operational_rules"](payload))
        self.assertTrue(validator["validate_operational_rules"]([]))

    def test_doctor_compares_operational_probe_separately(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "Review"
            run_cmd([sys.executable, str(SCAFFOLDER), str(repo), "--runtime", "python", "--preset", "worker"])
            write_valid_docs(repo, "Review", "review")
            operations = repo / "docs/OPERATIONS.md"
            operations.write_text(operations.read_text() + "\n### Saúde operacional\n\n```bash\nprobe --read-only\n```\n")
            manifest = repo / "deploy/manifest.json"
            payload = json.loads(manifest.read_text())
            payload["healthcheck"] = {"command": "probe --read-only"}
            manifest.write_text(json.dumps(payload))
            run_cmd([sys.executable, str(repo / "scripts/project_doctor.py"), "--deploy-strict"])
            payload["healthcheck"] = {"http": {"url": "http://127.0.0.1:8000/health"}}
            manifest.write_text(json.dumps(payload))
            result = run_cmd([sys.executable, str(repo / "scripts/project_doctor.py"), "--deploy-strict"], expected=1)
            self.assertIn("divergem na URL do healthcheck", result.stderr)

    def test_doctor_rejects_runtime_and_validation_divergence(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "Review"
            run_cmd([sys.executable, str(SCAFFOLDER), str(repo), "--runtime", "python", "--preset", "worker"])
            write_valid_docs(repo, "Review", "review")
            agents = repo / "AGENTS.md"
            agents.write_text(agents.read_text().replace("comando de validacao minima", "comando de validação mínima").replace("`python -m review --once`", "`python -m review --wrong`"))
            manifest = repo / "deploy/manifest.json"
            payload = json.loads(manifest.read_text())
            payload["runtime"]["id"] = "go"
            manifest.write_text(json.dumps(payload))
            result = run_cmd([sys.executable, str(repo / "scripts/project_doctor.py")], expected=1)
            self.assertIn("divergem na validacao minima", result.stderr)
            self.assertIn("divergem no runtime escolhido", result.stderr)


if __name__ == "__main__":
    unittest.main()
