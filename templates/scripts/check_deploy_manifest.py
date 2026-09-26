#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "deploy" / "manifest.json"
SCHEMA = ROOT / "schema" / "deploy-manifest.schema.json"


def load_json(path: Path, label: str) -> tuple[Any, list[str]]:
    if not path.exists():
        return None, [f"{label} ausente: {path}"]

    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except json.JSONDecodeError as exc:
        return None, [f"{label} invalido: {exc}"]


def json_type(value: Any) -> str:
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    if value is None:
        return "null"
    return type(value).__name__


def type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return (isinstance(value, int) or isinstance(value, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def validate_type(value: Any, schema: Mapping[str, Any], path: str, errors: list[str]) -> bool:
    expected = schema.get("type")
    if expected is None:
        return True

    expected_types = expected if isinstance(expected, list) else [expected]
    if not all(isinstance(item, str) for item in expected_types):
        errors.append(f"{path}: schema invalido em type")
        return False

    if not any(type_matches(value, item) for item in expected_types):
        allowed = " ou ".join(expected_types)
        errors.append(f"{path}: esperado {allowed}, recebido {json_type(value)}")
        return False

    return True


def validate_object(value: Any, schema: Mapping[str, Any], path: str, errors: list[str]) -> None:
    if not isinstance(value, dict):
        return

    required = schema.get("required", [])
    if not isinstance(required, list) or not all(isinstance(item, str) for item in required):
        errors.append(f"{path}: schema invalido em required")
        required = []

    for key in required:
        if key not in value:
            errors.append(f"{path}.{key}: campo obrigatorio ausente")

    properties = schema.get("properties", {})
    if not isinstance(properties, dict):
        errors.append(f"{path}: schema invalido em properties")
        properties = {}

    for key, nested_schema in properties.items():
        if key in value:
            validate_schema(value[key], nested_schema, f"{path}.{key}", errors)

    additional = schema.get("additionalProperties", True)
    known_keys = set(properties)
    for key, nested_value in value.items():
        if key in known_keys:
            continue
        nested_path = f"{path}.{key}"
        if additional is False:
            errors.append(f"{nested_path}: propriedade nao permitida")
        elif isinstance(additional, dict):
            validate_schema(nested_value, additional, nested_path, errors)


def validate_array(value: Any, schema: Mapping[str, Any], path: str, errors: list[str]) -> None:
    if not isinstance(value, list):
        return

    min_items = schema.get("minItems")
    if isinstance(min_items, int) and len(value) < min_items:
        errors.append(f"{path}: deve conter pelo menos {min_items} item(ns)")

    max_items = schema.get("maxItems")
    if isinstance(max_items, int) and len(value) > max_items:
        errors.append(f"{path}: deve conter no maximo {max_items} item(ns)")

    if schema.get("uniqueItems") is True:
        encoded_items = [json.dumps(item, sort_keys=True, ensure_ascii=True) for item in value]
        if len(encoded_items) != len(set(encoded_items)):
            errors.append(f"{path}: deve conter itens unicos")

    items_schema = schema.get("items")
    if isinstance(items_schema, dict):
        for index, item in enumerate(value):
            validate_schema(item, items_schema, f"{path}[{index}]", errors)


def validate_string(value: Any, schema: Mapping[str, Any], path: str, errors: list[str]) -> None:
    if not isinstance(value, str):
        return

    min_length = schema.get("minLength")
    if isinstance(min_length, int) and len(value) < min_length:
        errors.append(f"{path}: deve conter pelo menos {min_length} caractere(s)")

    max_length = schema.get("maxLength")
    if isinstance(max_length, int) and len(value) > max_length:
        errors.append(f"{path}: deve conter no maximo {max_length} caractere(s)")

    pattern = schema.get("pattern")
    if isinstance(pattern, str) and re.search(pattern, value) is None:
        errors.append(f"{path}: nao corresponde ao pattern esperado")


def validate_number(value: Any, schema: Mapping[str, Any], path: str, errors: list[str]) -> None:
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return

    minimum = schema.get("minimum")
    if isinstance(minimum, (int, float)) and value < minimum:
        errors.append(f"{path}: deve ser maior ou igual a {minimum}")

    maximum = schema.get("maximum")
    if isinstance(maximum, (int, float)) and value > maximum:
        errors.append(f"{path}: deve ser menor ou igual a {maximum}")

    exclusive_minimum = schema.get("exclusiveMinimum")
    if isinstance(exclusive_minimum, (int, float)) and value <= exclusive_minimum:
        errors.append(f"{path}: deve ser maior que {exclusive_minimum}")

    exclusive_maximum = schema.get("exclusiveMaximum")
    if isinstance(exclusive_maximum, (int, float)) and value >= exclusive_maximum:
        errors.append(f"{path}: deve ser menor que {exclusive_maximum}")


def validate_combiner(value: Any, schema: Mapping[str, Any], keyword: str, path: str, errors: list[str]) -> None:
    nested_schemas = schema.get(keyword)
    if nested_schemas is None:
        return

    if not isinstance(nested_schemas, list) or not all(isinstance(item, dict) for item in nested_schemas):
        errors.append(f"{path}: schema invalido em {keyword}")
        return

    matches = 0
    collected_errors: list[str] = []
    for nested_schema in nested_schemas:
        nested_errors: list[str] = []
        validate_schema(value, nested_schema, path, nested_errors)
        if nested_errors:
            collected_errors.extend(nested_errors)
        else:
            matches += 1

    if keyword == "allOf" and matches != len(nested_schemas):
        errors.extend(collected_errors)
    elif keyword == "anyOf" and matches == 0:
        errors.append(f"{path}: deve corresponder a pelo menos uma alternativa em anyOf")
    elif keyword == "oneOf" and matches != 1:
        errors.append(f"{path}: deve corresponder a exatamente uma alternativa em oneOf")


def validate_schema(value: Any, schema: Any, path: str, errors: list[str]) -> None:
    if schema is True:
        return
    if schema is False:
        errors.append(f"{path}: valor nao permitido pelo schema")
        return
    if not isinstance(schema, dict):
        errors.append(f"{path}: schema invalido")
        return

    for keyword in ("allOf", "anyOf", "oneOf"):
        validate_combiner(value, schema, keyword, path, errors)

    not_schema = schema.get("not")
    if isinstance(not_schema, dict):
        nested_errors: list[str] = []
        validate_schema(value, not_schema, path, nested_errors)
        if not nested_errors:
            errors.append(f"{path}: corresponde a uma regra proibida em not")

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: deve ser {schema['const']!r}")

    enum_values = schema.get("enum")
    if isinstance(enum_values, list) and value not in enum_values:
        errors.append(f"{path}: deve ser um de {enum_values!r}")

    if not validate_type(value, schema, path, errors):
        return

    validate_object(value, schema, path, errors)
    validate_array(value, schema, path, errors)
    validate_string(value, schema, path, errors)
    validate_number(value, schema, path, errors)


def walk_strings(value: Any, path: str) -> list[tuple[str, str]]:
    if isinstance(value, str):
        return [(path, value)]
    if isinstance(value, list):
        return [
            item
            for index, nested in enumerate(value)
            for item in walk_strings(nested, f"{path}[{index}]")
        ]
    if isinstance(value, dict):
        return [
            item
            for key, nested in value.items()
            for item in walk_strings(nested, f"{path}.{key}")
        ]
    return []


def require_text(payload: Mapping[str, Any], dotted_path: str, errors: list[str]) -> str:
    current: Any = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            errors.append(f"{dotted_path}: campo obrigatorio ausente")
            return ""
        current = current[part]

    if not isinstance(current, str) or not current.strip():
        errors.append(f"{dotted_path}: campo obrigatorio ausente ou vazio")
        return ""

    return current.strip()


def validate_operational_rules(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["manifesto: deve ser um objeto JSON"]

    for path, value in walk_strings(payload, "$"):
        normalized = value.strip().lower()
        if "{{" in normalized or "preencher" in normalized or normalized.startswith("todo"):
            errors.append(f"{path}: valor ainda esta como placeholder")

    for field in ("project.name", "project.slug", "runtime.id", "runtime.version", "restart.policy", "backup.policy", "rollback.strategy"):
        require_text(payload, field, errors)

    healthcheck = payload.get("healthcheck")
    has_command = isinstance(healthcheck, dict) and isinstance(healthcheck.get("command"), str) and bool(healthcheck["command"].strip())
    has_http = False
    if isinstance(healthcheck, dict) and "http" in healthcheck:
        http = healthcheck["http"]
        url = http.get("url") if isinstance(http, dict) else None
        try:
            parsed = urlsplit(url) if isinstance(url, str) else None
            has_http = bool(parsed and parsed.scheme in ("http", "https") and parsed.hostname and not parsed.username and not parsed.password and not any(char.isspace() for char in url))
            if parsed:
                _ = parsed.port
        except ValueError:
            has_http = False
        if not has_http:
            errors.append("healthcheck.http.url: exige URL HTTP(S) valida, sem credenciais")

    deploy_target = require_text(payload, "deploy.target", errors)
    require_text(payload, "deploy.reason", errors)
    if deploy_target != "none":
        require_text(payload, "process.command", errors)
        if not has_command and not has_http:
            errors.append("healthcheck: precisa declarar command ou http quando deploy.target nao e none")

    return errors


def main() -> int:
    payload, payload_errors = load_json(MANIFEST, "deploy/manifest.json")
    schema, schema_errors = load_json(SCHEMA, "schema/deploy-manifest.schema.json")
    errors = payload_errors + schema_errors

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    schema_errors = []
    validate_schema(payload, schema, "$", schema_errors)
    operational_errors = validate_operational_rules(payload)
    errors = schema_errors + operational_errors

    if errors:
        print("deploy/manifest.json falhou na validacao.", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print("deploy/manifest.json validado.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
