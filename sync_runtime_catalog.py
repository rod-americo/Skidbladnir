#!/usr/bin/env python3
"""Materializa tabela de suporte e CI do kit a partir do catálogo versionado."""
from __future__ import annotations

import argparse
from pathlib import Path

from scaffold_project import BASE_DIR, CATALOG, RUNTIMES


def artifacts() -> dict[Path, str]:
    actions = CATALOG['actions']
    lines = ["# Catálogo de runtimes", "", "Gerado por `python3 sync_runtime_catalog.py`. Edite `templates/runtimes/catalog.json` e regenere; os checks de CI detectam divergência.", "", f"Versões concretas da release; consulta em {CATALOG['reviewed_on']}. Python {CATALOG['validation_python']} executa os validadores estruturais em todos os jobs, sem determinar a linguagem da aplicação.", "", "| ID | Linguagem | Toolchain | Presets |", "| --- | --- | --- | --- |"]
    for runtime, profile in RUNTIMES.items():
        lines.append(f"| `{runtime}` | {profile['language']} | {profile['version']} | {', '.join(p.replace('_', '-') for p in profile['presets'])} |")
    lines += ["", "`node` gera JavaScript; `ts` gera TypeScript sobre Node. `js` continua válido como identificador legado no manifesto. `generic` representa ausência de runtime dominante, não uma escolha automática.", "", "## Comandos por runtime", "", "Os marcadores `{slug}`, `{module}`, `{dist}` e `{sources}` são substituídos na geração. O Java usa Maven " + RUNTIMES['java']['maven_version'] + " pelo wrapper versionado. O Rust fixa edição " + RUNTIMES['rust']['edition'] + ".", ""]
    for runtime, profile in RUNTIMES.items():
        if runtime == 'generic':
            continue
        lines += [f"### {profile['name']} (`{runtime}`)", "", "Bootstrap:", "", "```bash", profile['setup'], "```", "", "Checks de desenvolvimento:", "", "```bash", profile['test'], profile['build'], "```", "", "Smoke local:", "", "```bash", profile['smoke'], "```", ""]
    workflow = f'''# Gerado por sync_runtime_catalog.py; não editar versões aqui.
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  structural:
    runs-on: ubuntu-24.04
    timeout-minutes: 10
    steps:
      - uses: {actions['checkout']}
        with:
          persist-credentials: false
      - uses: {actions['python']}
        with:
          python-version: "{CATALOG['validation_python']}"
      - run: python3 run_regression_suite.py
      - run: python3 -m py_compile scaffold_project.py run_regression_suite.py run_runtime_checks.py sync_runtime_catalog.py bin/newproj
      - run: python3 sync_runtime_catalog.py --check
'''
    for runtime, profile in RUNTIMES.items():
        if runtime == 'generic':
            continue
        workflow += f'''
  runtime-{runtime}:
    runs-on: ubuntu-24.04
    timeout-minutes: 30
'''
        if runtime == 'swift':
            workflow += f"    container: {profile['container']}\n"
        workflow += f'''    steps:
      - uses: {actions['checkout']}
        with:
          persist-credentials: false
      - uses: {actions['python']}
        with:
          python-version: "{CATALOG['validation_python']}"
'''
        if runtime in ('node', 'ts', 'go', 'csharp', 'java'):
            action = {'ts': 'node', 'csharp': 'dotnet'}.get(runtime, runtime)
            workflow += f"      - uses: {actions[action]}\n        with:\n          {action}-version: \"{profile['version']}\"\n"
            if runtime == 'java':
                workflow += '          distribution: temurin\n'
            if runtime == 'go':
                workflow += '          cache: false\n'
        elif runtime == 'rust':
            workflow += f"      - run: rustup toolchain install {profile['version']} --profile minimal --component rustfmt,clippy\n      - run: rustup default {profile['version']}\n"
        workflow += f"      - run: python3 run_runtime_checks.py --runtime {runtime}\n"
    return {BASE_DIR / 'docs/runtime-catalog.md': '\n'.join(lines), BASE_DIR / '.github/workflows/ci.yml': workflow}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    changed = []
    for path, content in artifacts().items():
        if not path.exists() or path.read_text() != content:
            changed.append(path)
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content)
    if args.check and changed:
        print('Artefatos divergentes: ' + ', '.join(str(p.relative_to(BASE_DIR)) for p in changed))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
