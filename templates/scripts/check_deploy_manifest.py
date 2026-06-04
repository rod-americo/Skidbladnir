
#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "deploy" / "manifest.json"


def require_mapping(payload: dict[str, object], key: str, errors: list[str]) -> dict[str, object]:
    value = payload.get(key)
    if not isinstance(value, dict):
        errors.append(f"campo obrigatorio ausente ou invalido: {key}")
        return {}
    return value


def require_text(payload: dict[str, object], key: str, path: str, errors: list[str]) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        errors.append(f"campo obrigatorio ausente ou vazio: {path}.{key}")
        return ""
    if "preencher" in value.lower() or value.strip().startswith("TODO"):
        errors.append(f"campo ainda esta como placeholder: {path}.{key}")
    return value.strip()


def require_list(payload: dict[str, object], key: str, path: str, errors: list[str]) -> list[object]:
    value = payload.get(key)
    if not isinstance(value, list):
        errors.append(f"campo obrigatorio ausente ou invalido: {path}.{key}")
        return []
    return value


def main() -> int:
    if not MANIFEST.exists():
        print(f"deploy manifest ausente: {MANIFEST}", file=sys.stderr)
        return 1

    try:
        payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"deploy/manifest.json invalido: {exc}", file=sys.stderr)
        return 1

    errors: list[str] = []
    if not isinstance(payload, dict):
        print("deploy/manifest.json deve ser um objeto JSON", file=sys.stderr)
        return 1

    if payload.get("version") != 1:
        errors.append("version deve ser 1")

    project = require_mapping(payload, "project", errors)
    runtime = require_mapping(payload, "runtime", errors)
    deploy = require_mapping(payload, "deploy", errors)
    process = require_mapping(payload, "process", errors)
    healthcheck = require_mapping(payload, "healthcheck", errors)
    environment = require_mapping(payload, "environment", errors)
    secrets = require_mapping(payload, "secrets", errors)
    runtime_state = require_mapping(payload, "runtime_state", errors)
    logs = require_mapping(payload, "logs", errors)
    restart = require_mapping(payload, "restart", errors)
    backup = require_mapping(payload, "backup", errors)
    rollback = require_mapping(payload, "rollback", errors)

    require_text(project, "name", "project", errors)
    require_text(project, "slug", "project", errors)
    require_text(runtime, "id", "runtime", errors)
    deploy_target = require_text(deploy, "target", "deploy", errors)
    require_text(deploy, "reason", "deploy", errors)
    require_list(payload, "ports", "root", errors)
    require_list(environment, "required", "environment", errors)
    require_list(secrets, "required", "secrets", errors)
    require_list(runtime_state, "paths", "runtime_state", errors)
    require_list(logs, "paths", "logs", errors)
    require_text(restart, "policy", "restart", errors)
    require_text(backup, "policy", "backup", errors)
    require_text(rollback, "strategy", "rollback", errors)

    if deploy_target != "none":
        require_text(process, "command", "process", errors)
        has_command = isinstance(healthcheck.get("command"), str) and bool(str(healthcheck["command"]).strip())
        has_http = isinstance(healthcheck.get("http"), dict)
        if not has_command and not has_http:
            errors.append("healthcheck precisa declarar command ou http quando deploy.target nao e none")
    else:
        require_text(deploy, "reason", "deploy", errors)

    if errors:
        print("deploy/manifest.json falhou na validacao.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("deploy/manifest.json validado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
