#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import textwrap
import unicodedata
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = BASE_DIR / "templates"
COMMON_TEMPLATE_DIR = TEMPLATE_DIR / "common"
STARTER_VERSION_FILE = BASE_DIR / "VERSION"
STARTER_VERSION = STARTER_VERSION_FILE.read_text(encoding="utf-8").strip() if STARTER_VERSION_FILE.exists() else "0.0.0"
TEMPLATE_FILES = {
    "README.md": COMMON_TEMPLATE_DIR / "README.md",
    "AGENTS.md": COMMON_TEMPLATE_DIR / "AGENTS.md",
    "PROJECT_GATE.md": COMMON_TEMPLATE_DIR / "PROJECT_GATE.md",
    "CHANGELOG.md": COMMON_TEMPLATE_DIR / "CHANGELOG.md",
    "docs/ARCHITECTURE.md": COMMON_TEMPLATE_DIR / "docs" / "ARCHITECTURE.md",
    "docs/CONTRACTS.md": COMMON_TEMPLATE_DIR / "docs" / "CONTRACTS.md",
    "docs/OPERATIONS.md": COMMON_TEMPLATE_DIR / "docs" / "OPERATIONS.md",
    "docs/DECISIONS.md": COMMON_TEMPLATE_DIR / "docs" / "DECISIONS.md",
}
OPTIONAL_TEMPLATE_FILES = {
    "START_CHECKLIST.md": COMMON_TEMPLATE_DIR / "START_CHECKLIST.md",
}
OPTIONAL_STRUCTURE_TEMPLATE_FILES = {
    "papers/README.md": COMMON_TEMPLATE_DIR / "papers" / "README.md",
}
WORKFLOW_TEMPLATE_FILES = {
    "python": TEMPLATE_DIR / ".github" / "workflows" / "ci-python.yml",
    "node": TEMPLATE_DIR / ".github" / "workflows" / "ci-node.yml",
    "go": TEMPLATE_DIR / ".github" / "workflows" / "ci-go.yml",
    "ts": TEMPLATE_DIR / ".github" / "workflows" / "ci-node.yml",
    "swift": TEMPLATE_DIR / ".github" / "workflows" / "ci-swift.yml",
    "csharp": TEMPLATE_DIR / ".github" / "workflows" / "ci-csharp.yml",
}
SCRIPT_TEMPLATE_FILES = {
    "scripts/check_project_gate.py": TEMPLATE_DIR / "scripts" / "check_project_gate.py",
    "scripts/check_deploy_manifest.py": TEMPLATE_DIR / "scripts" / "check_deploy_manifest.py",
    "scripts/project_doctor.py": TEMPLATE_DIR / "scripts" / "project_doctor.py",
}
SCHEMA_TEMPLATE_FILES = {
    "schema/deploy-manifest.schema.json": BASE_DIR / "schema" / "deploy-manifest.schema.json",
}
GATE_ENFORCEMENT_TEMPLATE_FILES = {
    ".githooks/pre-commit": TEMPLATE_DIR / "githooks" / "pre-commit",
    "scripts/install_git_hooks.sh": TEMPLATE_DIR / "scripts" / "install_git_hooks.sh",
}
PLACEHOLDER_RE = re.compile(r"\{\{([^}]+)\}\}")
PRESET_CHOICES = (
    "base",
    "fastapi",
    "fastapi-service",
    "cli",
    "textual-cli",
    "worker",
    "playwright-worker",
    "pipeline",
    "dicom-pipeline",
)
PRESET_ALIASES = {
    "base": "base",
    "fastapi": "fastapi",
    "fastapi-service": "fastapi",
    "cli": "cli",
    "textual-cli": "textual_cli",
    "worker": "worker",
    "playwright-worker": "playwright_worker",
    "pipeline": "pipeline",
    "dicom-pipeline": "dicom_pipeline",
}
PRESET_SUMMARIES = {
    "base": "baseline neutro com camadas e documentacao minima",
    "fastapi": "servico HTTP pequeno com FastAPI, uvicorn e /health",
    "fastapi-service": "alias de fastapi com nome mais explicito para servicos",
    "cli": "CLI minima com subcomando doctor",
    "textual-cli": "CLI operacional com TUI Textual e doctor separado",
    "worker": "worker/daemon simples com loop, --once e --interval",
    "playwright-worker": "worker com artefatos de sessao de browser e bootstrap dry-run",
    "pipeline": "pipeline generico orientado a item e materializacao local",
    "dicom-pipeline": "pipeline DICOM com pydicom, inbox/outbox e manifesto de estudo",
}


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^A-Za-z0-9]+", "_", ascii_only).strip("_").lower()
    if not slug:
        slug = "project"
    if slug[0].isdigit():
        slug = f"project_{slug}"
    return slug


def kebabify(value: str) -> str:
    return slugify(value).replace("_", "-")


def pascalize(value: str) -> str:
    parts = re.findall(r"[A-Za-z0-9]+", value)
    candidate = "".join(part[:1].upper() + part[1:] for part in parts if part)
    if not candidate:
        candidate = "Project"
    if candidate[0].isdigit():
        candidate = f"Project{candidate}"
    return candidate


def todo_value(raw: str) -> str:
    cleaned = " ".join(raw.split())
    return f"TODO: {cleaned}"


def canonicalize_preset(value: str) -> str:
    return PRESET_ALIASES.get(value, value)


def print_available_presets() -> None:
    print("Presets disponiveis:")
    for preset in PRESET_CHOICES:
        print(f"- {preset}: {PRESET_SUMMARIES[preset]}")


def prepend_gate_check(command: str, gate_enforced: bool) -> str:
    if not gate_enforced:
        return command
    gate_cmd = "python3 scripts/check_project_gate.py"
    if not command or command.startswith(gate_cmd):
        return gate_cmd
    return f"{gate_cmd} && {command}"


def github_repo_slug(repo_url: str) -> str | None:
    cleaned = repo_url.strip()
    ssh_match = re.match(r"git@github\.com:(?P<slug>[^/]+/[^/]+?)(?:\.git)?$", cleaned)
    if ssh_match:
        return ssh_match.group("slug")

    https_match = re.match(r"https://github\.com/(?P<slug>[^/]+/[^/]+?)(?:\.git)?/?$", cleaned)
    if https_match:
        return https_match.group("slug")

    return None


def default_readme_badges(runtime: str, repo_url: str) -> str:
    badges: list[str] = []
    repo_slug = github_repo_slug(repo_url)
    if repo_slug:
        workflow_url = f"https://github.com/{repo_slug}/actions/workflows/ci.yml"
        badges.append(f"[![CI]({workflow_url}/badge.svg)]({workflow_url})")

    if runtime == "python":
        badges.append("![Python](https://img.shields.io/badge/python-3.11%2B-blue)")
    elif runtime == "node":
        badges.append("![Node](https://img.shields.io/badge/node-20%2B-5fa04e)")
    elif runtime == "go":
        badges.append("![Go](https://img.shields.io/badge/go-1.22%2B-00ADD8)")
    elif runtime == "ts":
        badges.append("![TypeScript](https://img.shields.io/badge/typescript-5%2B-3178c6)")
    elif runtime == "swift":
        badges.append("![Swift](https://img.shields.io/badge/swift-5.9%2B-f05138)")
    elif runtime == "csharp":
        badges.append("![.NET](https://img.shields.io/badge/.NET-8.0%2B-512bd4)")

    return "\n".join(badges)


def runtime_defaults(
    runtime: str,
    preset: str,
    project_name: str,
    project_slug: str,
    repo_url: str,
    gate_enforced: bool,
) -> dict[str, str]:
    env_prefix = project_slug.upper()
    dist_name = kebabify(project_name)

    common = {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": project_slug,
        "PROJECT_PHASE": "prototipo",
        "REPO_URL": repo_url,
        "README_BADGES": default_readme_badges(runtime, repo_url),
        "OPTIONAL_RESEARCH_STRUCTURE": "",
        "OPTIONAL_RESEARCH_DOCS": "",
        "DEPENDENCY_FILE": "requirements.txt / package.json",
        "RUNTIME_STRUCTURE": textwrap.dedent(
            f"""
            ├── {project_slug}/
            │   ├── domain/
            │   ├── application/
            │   ├── infrastructure/
            │   ├── interfaces/
            │   └── main.py
            """
        ).strip(),
        "DOMINIO_CRITICO": "preencher dominio critico do projeto",
        "DEPENDENCIA_EXTERNA": "preencher dependencia externa principal",
        "HOST_PRINCIPAL": "preencher host principal ou ambiente de referencia",
        "TIPO_DE_DADO_SENSIVEL": "credenciais, configuracao host-local e payloads operacionais",
        "VALIDACAO_MINIMA": "preencher comando minimo de validacao",
        "RESTART_POLICY": "preencher regra de restart por tipo de mudanca",
        "PRIMARY_RUNTIME": "preencher runtime principal",
        "ENV_OR_SETTING_1": f"{env_prefix}_CONFIG_FILE",
        "ENV_OR_SETTING_2": "LOG_LEVEL",
        "host | local | CI": "host",
        "valor_exemplo": "preencher",
        "API / host / banco / fila / worker / PACS / browser / etc": "preencher dependencia principal",
        "uma biblioteca, servico, pipeline, automacao, produto interno, etc.": "produto interno",
        "a capacidade principal": "preencher capacidade principal",
        "o contexto operacional ou de negocio": "preencher contexto operacional",
        "motivacao_1": "preencher por que este repositorio precisa existir agora",
        "motivacao_2": "preencher por que a fronteira dele merece ser explicita",
        "motivacao_3": "preencher que tipo de desgaste ou improviso este projeto evita",
        "escopo que voce quer proibir desde o inicio": "preencher",
        "escopo que parece proximo, mas pertence a outro sistema": "preencher fronteira fora do escopo",
        "atalhos que voce quer proibir desde o inicio": "pular contrato, logica de dominio solta na raiz e crescimento sem runtime claro",
        "integracoes ou comportamentos que nao devem nascer aqui": "funcionalidades que pertencem a outro sistema ou repositorio",
        "entrypoint_1": "preencher entrypoint principal",
        "entrypoint_2": "preencher entrypoint secundario",
        "SETUP_COMMANDS": "preencher setup",
        "OPTIONAL_ENV_SETUP": "# opcional: preencher ajuste de ambiente local",
        "RUN_COMMAND": "preencher comando de execucao",
        "risco_tecnico_principal": "preencher risco tecnico principal",
        "dependencia_mais_fragil": "preencher dependencia mais fragil",
        "divida_tecnica_principal": "preencher divida tecnica principal",
        "consolidado_1": "baseline documental e estrutural gerada pelo scaffold",
        "consolidado_2": "entrypoint principal e validacao minima materializados no repositório",
        "consolidado_3": "baseline de CI e guardrails locais preparados para evolucao segura",
        "em_andamento_1": "preencher frente que esta sendo endurecida agora",
        "em_andamento_2": "preencher area ainda parcial ou dependente de validacao real",
        "passo_1": "preencher",
        "passo_2": "preencher",
        "passo_3": "preencher",
        "responsabilidade_1": "preencher responsabilidade central",
        "responsabilidade_2": "preencher responsabilidade secundaria",
        "fora_do_escopo_1": "preencher",
        "fora_do_escopo_2": "preencher",
        "API / fila / arquivo / PACS / webhook / operador": "preencher entrada externa principal",
        "banco / evento / arquivo / API / dashboard / integracao": "preencher saida externa principal",
        "dependencia_1": "integracao externa principal",
        "dependencia_2": "configuracao host-local e runtime state",
        "entrada": "preencher entrada inicial",
        "validacao / transformacao": "preencher etapa de validacao ou transformacao",
        "persistencia / orquestracao": "preencher etapa de persistencia ou orquestracao",
        "saida": "preencher saida final",
        "entrada_canonica": "preencher entrada canonica",
        "saida_canonica": "preencher saida canonica",
        "id_primario": "preencher identificador primario",
        "invariante_1": "preencher invariante",
        "invariante_2": "preencher invariante",
        "sqlite / postgres / filesystem / none": "filesystem",
        "path": "runtime/",
        "estrategia": "preencher estrategia de persistencia e backup",
        "como_migrar": "preencher estrategia de migracao",
        "arquivo_exemplo": "config/settings.example.*",
        "arquivo_local": "config/settings.local.*",
        "sim/nao": "sim",
        "json / key-value / outro parseavel": "json",
        "fila, latency, throughput, errors, etc": "errors, throughput e latency",
        "comando ou endpoint": "preencher smoke test",
        "risco_1": "preencher risco tecnico",
        "acoplamento_1": "preencher acoplamento consciente",
        "parte_experimental": "preencher parte ainda experimental",
        "decisao_aberta_1": "preencher decisao aberta",
        "decisao_aberta_2": "preencher decisao aberta",
        "input_1": "preencher input",
        "input_2": "preencher input",
        "origem": "preencher origem",
        "json/csv/http/file": "file",
        "observacao": "preencher observacao",
        "output_1": "preencher output",
        "output_2": "preencher output",
        "destino": "preencher destino",
        "json/file/db": "file",
        "garantia": "preencher garantia",
        "entidade_1": "preencher entidade",
        "field_1": "preencher campo",
        "nao assumir equivalencia com ...": "preencher quando houver identificadores diferentes",
        "entidade_2": "preencher entidade",
        "field_2": "preencher campo",
        "step_1": "preencher etapa",
        "step_2": "preencher etapa",
        "input": "preencher entrada",
        "output": "preencher saida",
        "failures": "preencher falhas esperadas",
        "assuncao_1": "preencher assuncao nao validada",
        "assuncao_2": "preencher assuncao nao validada",
        "descricao_curta_da_quebra": "preencher quebra de contrato",
        "LOCAL_BOOT_COMMANDS": "preencher boot local",
        "PRIMARY_RUN_COMMAND": "preencher comando principal",
        "config_local": "preencher arquivo local",
        "ENV_1": "preencher env critica",
        "ENV_2": "preencher env critica",
        "runtime": "preencher runtime",
        "obs": "preencher observacao",
        "runtime_path": "runtime/",
        "logs_path": "runtime/logs/",
        "SMOKE_TEST_COMMAND": "preencher smoke test",
        "CI_GATE_STEP": "",
        "CI_DEPLOY_STEP": "      - name: Check deploy manifest\n        run: python3 scripts/check_deploy_manifest.py",
        "CI_STATIC_CHECK_COMMAND": "preencher checagem sintatica",
        "CI_VALIDATE_COMMAND": "preencher validacao de CI",
        "PYTHON_VERSION": "3.11",
        "NODE_VERSION": "20",
        "GO_VERSION": "1.22",
        "DOTNET_VERSION": "8.0.x",
        "logger": "preencher logger principal",
        "json / key-value / outro": "json",
        "arquivo_ou_journal": "preencher local dos logs",
        "falha_1": "preencher falha comum",
        "falha_2": "preencher falha comum",
        "restart_impact": "preencher impacto de restart",
        "storage": "preencher storage",
        "como_e_onde": "preencher backup",
        "politica": "preencher politica",
        "o_que_pode_ser_removido": "preencher limpeza segura",
        "estado_critico_1": "preencher estado critico",
        "estado_critico_2": "preencher estado critico",
        "titulo_curto_da_decisao": "preencher titulo",
        "qual problema levou a decisao": "preencher contexto",
        "o que foi escolhido": "preencher decisao",
        "impacto_1": "preencher impacto",
        "impacto_2": "preencher impacto",
        "tradeoff_1": "preencher tradeoff",
        "tradeoff_2": "preencher tradeoff",
        "alternativa_1": "preencher alternativa rejeitada",
        "alternativa_2": "preencher alternativa rejeitada",
        "nova capacidade": "preencher nova capacidade",
        "mudanca de comportamento ou arquitetura": "preencher mudanca",
        "correcao com impacto observavel": "preencher correcao",
        "comportamento em processo de remocao": "preencher depreciacao",
        "comportamento removido": "preencher remocao",
        "migracao, restart, dados, compatibilidade, risco": "preencher nota operacional",
        "placeholder": "preencher",
    }

    if runtime == "python":
        common.update(
            {
                "PRIMARY_RUNTIME": "python3.11+",
                "DEPENDENCY_FILE": "requirements.txt",
                "SETUP_COMMANDS": textwrap.dedent(
                    """
                    python3 -m venv .venv --prompt $(basename "$PWD")
                    source .venv/bin/activate
                    python -m pip install --upgrade pip
                    python -m pip install -r requirements.txt
                    """
                ).strip(),
                "OPTIONAL_ENV_SETUP": "export APP_ENV=dev",
                "RUN_COMMAND": f"python -m {project_slug}",
                "VALIDACAO_MINIMA": "python -m pytest -q",
                "RESTART_POLICY": "mudancas de codigo Python exigem restart do processo; docs isoladas nao exigem restart",
                "runtime": "python3.11+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "APP_ENV",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    f"""
                    python3 -m venv .venv --prompt $(basename "$PWD")
                    source .venv/bin/activate
                    python -m pip install -r requirements.txt
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug}",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "python -m pytest -q",
                "CI_STATIC_CHECK_COMMAND": f"python -m compileall -q {project_slug} scripts tests",
                "CI_VALIDATE_COMMAND": "python -m pytest -q",
                "logger": f"{project_slug}.infrastructure.logging",
                "storage": "filesystem local ou banco definido pelo projeto",
            }
        )
    elif runtime == "node":
        common.update(
            {
                "PRIMARY_RUNTIME": "node20+",
                "DEPENDENCY_FILE": "package.json",
                "SETUP_COMMANDS": "npm install",
                "OPTIONAL_ENV_SETUP": "export NODE_ENV=development",
                "RUN_COMMAND": "npm start",
                "VALIDACAO_MINIMA": "npm test",
                "RESTART_POLICY": "mudancas em codigo Node exigem restart do processo; docs isoladas nao exigem restart",
                "runtime": "node20+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "NODE_ENV",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    """
                    npm install
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": "npm start",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "npm test",
                "CI_VALIDATE_COMMAND": "npm test",
                "logger": f"{project_slug}/infrastructure/logger.mjs",
                "storage": "filesystem local ou banco definido pelo projeto",
            }
        )
    elif runtime == "go":
        common.update(
            {
                "PRIMARY_RUNTIME": "go1.22+",
                "DEPENDENCY_FILE": "go.mod",
                "SETUP_COMMANDS": "go mod download",
                "OPTIONAL_ENV_SETUP": "export APP_ENV=development",
                "RUN_COMMAND": f"go run ./cmd/{project_slug}",
                "VALIDACAO_MINIMA": "go test ./...",
                "RESTART_POLICY": "mudancas em codigo Go exigem rebuild/restart do processo; docs isoladas nao exigem restart",
                "runtime": "go1.22+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "APP_ENV",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    """
                    go mod download
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"go run ./cmd/{project_slug}",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "go test ./...",
                "CI_STATIC_CHECK_COMMAND": "go test ./...",
                "CI_VALIDATE_COMMAND": "go test ./...",
                "logger": f"{project_slug}/internal/logging",
                "storage": "filesystem local ou banco definido pelo projeto",
                "entrypoint_1": f"go run ./cmd/{project_slug}",
                "entrypoint_2": "go test ./...",
                "a capacidade principal": "oferecer um binario Go pequeno, testavel e operacionalmente explicito",
                "o contexto operacional ou de negocio": "servico, worker ou CLI compilavel com contrato de operacao documentado",
                "motivacao_1": "nascer com modulo Go, testes e manifesto operacional desde o primeiro commit",
                "motivacao_2": "separar entrypoint, pacote interno e operacao sem scripts soltos",
                "motivacao_3": "evitar binario sem contrato de runtime, restart ou smoke test",
                "API / host / banco / fila / worker / PACS / browser / etc": "runtime Go, host local e dependencias operacionais declaradas",
                "risco_tecnico_principal": "crescer logica de dominio diretamente no entrypoint sem contratos claros",
                "passo_1": "definir contrato de comando e flags publicas",
                "passo_2": "separar pacote interno e entrypoint em cmd",
                "passo_3": "registrar build, smoke e rollback em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "contrato do binario, flags e operacao local",
            }
        )
    elif runtime == "ts":
        common.update(
            {
                "PRIMARY_RUNTIME": "node20+ / typescript5+",
                "DEPENDENCY_FILE": "package.json / tsconfig.json",
                "SETUP_COMMANDS": "npm install",
                "OPTIONAL_ENV_SETUP": "export NODE_ENV=development",
                "RUN_COMMAND": "npm start",
                "VALIDACAO_MINIMA": "npm test",
                "RESTART_POLICY": "mudancas em TypeScript exigem rebuild e restart do processo; docs isoladas nao exigem restart",
                "runtime": "node20+ / typescript5+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "NODE_ENV",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    """
                    npm install
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": "npm start",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "npm test",
                "CI_VALIDATE_COMMAND": "npm test",
                "logger": "src/infrastructure/logger.ts",
                "storage": "filesystem local ou banco definido pelo projeto",
                "entrypoint_1": "npm start",
                "entrypoint_2": "npm test",
                "a capacidade principal": "oferecer um app TypeScript tipado, testavel e operacionalmente explicito",
                "o contexto operacional ou de negocio": "servico, worker ou CLI em Node com build e contratos declarados",
                "motivacao_1": "nascer com typecheck, teste e manifesto operacional desde o primeiro commit",
                "motivacao_2": "separar fonte TypeScript, artefato buildado e operacao",
                "motivacao_3": "evitar JavaScript gerado ou runtime Node sem contrato de smoke e rollback",
                "API / host / banco / fila / worker / PACS / browser / etc": "Node.js, TypeScript e dependencias operacionais declaradas",
                "risco_tecnico_principal": "deixar build, runtime e contratos de modulo divergirem silenciosamente",
                "passo_1": "definir comandos publicos de start, build e test",
                "passo_2": "separar fonte em src e testes tipados",
                "passo_3": "registrar build, smoke e rollback em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "contrato de build, comandos npm e operacao Node",
                "RUNTIME_STRUCTURE": textwrap.dedent(
                    """
                    ├── package.json
                    ├── tsconfig.json
                    ├── src/
                    │   ├── infrastructure/
                    │   └── main.ts
                    """
                ).strip(),
            }
        )
    elif runtime == "swift":
        swift_module = pascalize(project_slug)
        common.update(
            {
                "PRIMARY_RUNTIME": "swift5.9+",
                "DEPENDENCY_FILE": "Package.swift",
                "SETUP_COMMANDS": "swift package resolve",
                "OPTIONAL_ENV_SETUP": "export APP_ENV=development",
                "RUN_COMMAND": f"swift run {swift_module}",
                "VALIDACAO_MINIMA": f"swift build && swift run {swift_module}",
                "RESTART_POLICY": "mudancas em Swift exigem rebuild/restart do binario; docs isoladas nao exigem restart",
                "runtime": "swift5.9+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "APP_ENV",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    """
                    swift package resolve
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"swift run {swift_module}",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": f"swift build && swift run {swift_module}",
                "CI_VALIDATE_COMMAND": f"swift build && swift run {swift_module}",
                "logger": f"Sources/{swift_module}Core",
                "storage": "filesystem local ou banco definido pelo projeto",
                "entrypoint_1": f"swift run {swift_module}",
                "entrypoint_2": "swift build",
                "a capacidade principal": "oferecer um executavel Swift Package Manager com teste e operacao explicita",
                "o contexto operacional ou de negocio": "CLI, worker ou componente local em Swift com contrato de runtime documentado",
                "motivacao_1": "nascer como pacote Swift testavel sem improvisar operacao depois",
                "motivacao_2": "separar core testavel, executavel e manifesto operacional",
                "motivacao_3": "evitar binario local sem smoke, restart ou rollback declarado",
                "API / host / banco / fila / worker / PACS / browser / etc": "Swift Package Manager, host local e dependencias operacionais declaradas",
                "risco_tecnico_principal": "misturar logica testavel diretamente no entrypoint do executavel",
                "passo_1": "definir comandos publicos de run e test",
                "passo_2": "separar core testavel e executable target",
                "passo_3": "registrar build, smoke e rollback em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "contrato do executavel Swift e operacao local",
                "RUNTIME_STRUCTURE": textwrap.dedent(
                    f"""
                    ├── Package.swift
                    ├── Sources/
                    │   ├── {swift_module}/
                    │   └── {swift_module}Core/
                    """
                ).strip(),
            }
        )
    elif runtime == "csharp":
        csharp_project = pascalize(project_slug)
        common.update(
            {
                "PRIMARY_RUNTIME": "dotnet8+",
                "DEPENDENCY_FILE": f"{csharp_project}.sln / *.csproj",
                "SETUP_COMMANDS": "dotnet restore",
                "OPTIONAL_ENV_SETUP": "export DOTNET_ENVIRONMENT=Development",
                "RUN_COMMAND": f"dotnet run --project src/{csharp_project}",
                "VALIDACAO_MINIMA": "dotnet test",
                "RESTART_POLICY": "mudancas em C# exigem rebuild/restart do processo; docs isoladas nao exigem restart",
                "runtime": "dotnet8+",
                "ENV_1": f"{env_prefix}_CONFIG_FILE",
                "ENV_2": "DOTNET_ENVIRONMENT",
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    """
                    dotnet restore
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"dotnet run --project src/{csharp_project}",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "dotnet test",
                "CI_VALIDATE_COMMAND": "dotnet test",
                "logger": f"src/{csharp_project}",
                "storage": "filesystem local ou banco definido pelo projeto",
                "entrypoint_1": f"dotnet run --project src/{csharp_project}",
                "entrypoint_2": "dotnet test",
                "a capacidade principal": "oferecer um projeto .NET testavel com operacao e manifesto explicitos",
                "o contexto operacional ou de negocio": "CLI, worker ou servico .NET com comandos publicos claros",
                "motivacao_1": "nascer com solucao, projeto, testes e manifesto operacional desde o primeiro commit",
                "motivacao_2": "seguir convencoes .NET sem fingir layout Python",
                "motivacao_3": "evitar binario .NET sem smoke, restart ou rollback documentado",
                "API / host / banco / fila / worker / PACS / browser / etc": ".NET SDK, host local e dependencias operacionais declaradas",
                "risco_tecnico_principal": "misturar app, contratos e testes sem fronteira de projeto clara",
                "passo_1": "definir comando de run e projeto principal",
                "passo_2": "separar src e tests conforme convencao .NET",
                "passo_3": "registrar build, smoke e rollback em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "contrato do projeto .NET e operacao local",
                "RUNTIME_STRUCTURE": textwrap.dedent(
                    f"""
                    ├── {csharp_project}.sln
                    ├── src/
                    │   └── {csharp_project}/
                    ├── tests/
                    │   └── {csharp_project}.Tests/
                    """
                ).strip(),
            }
        )
    else:
        common.update(
            {
                "PRIMARY_RUNTIME": "preencher runtime principal",
                "SETUP_COMMANDS": "preencher setup do projeto",
                "RUN_COMMAND": "preencher comando de execucao",
                "VALIDACAO_MINIMA": "preencher validacao minima",
                "LOCAL_BOOT_COMMANDS": "preencher boot local",
                "PRIMARY_RUN_COMMAND": "preencher comando principal",
                "config_local": "config/settings.local.json",
                "SMOKE_TEST_COMMAND": "preencher smoke test",
                "CI_STATIC_CHECK_COMMAND": "preencher checagem sintatica",
                "CI_VALIDATE_COMMAND": "preencher validacao de CI",
                "logger": "preencher logger principal",
                "storage": "preencher storage principal",
            }
        )

    common.setdefault("escopo que voce quer proibir desde o inicio", "preencher")
    common["valor_exemplo"] = "preencher"
    common["host | local | CI"] = "host"
    common["REPO_URL"] = repo_url
    common["PROJECT_NAME"] = project_name
    common["PROJECT_SLUG"] = project_slug
    common["API / host / banco / fila / worker / PACS / browser / etc"] = "preencher dependencia externa critica"
    common["API / fila / arquivo / PACS / webhook / operador"] = "preencher entrada externa principal"

    if preset == "fastapi":
        common.update(
            {
                "a capacidade principal": "expor uma API HTTP pequena, coerente e integravel",
                "o contexto operacional ou de negocio": "servico HTTP interno orientado a integracoes e operacao",
                "motivacao_1": "nascer com contrato HTTP claro, sem improvisar estrutura de servico depois",
                "motivacao_2": "isolar a fronteira da API, os contratos e a operacao desde o primeiro dia",
                "motivacao_3": "evitar que endpoint, regra de negocio e infraestrutura crescam misturados",
                "entrypoint_1": f"python -m {project_slug}",
                "entrypoint_2": f"uvicorn {project_slug}.interfaces.http.app:create_app --factory --reload",
                "API / host / banco / fila / worker / PACS / browser / etc": "FastAPI, uvicorn e dependencias HTTP do servico",
                "risco_tecnico_principal": "deixar a camada HTTP crescer sem contratos ou sem separar aplicacao de infraestrutura",
                "passo_1": "definir endpoints e contratos minimos",
                "passo_2": "implementar validacao e tratamento de erro coerentes",
                "passo_3": "registrar restart policy e smoke test HTTP em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "contratos HTTP, payloads e fronteira da API",
                "RUN_COMMAND": f"python -m {project_slug}",
                "VALIDACAO_MINIMA": "python -m pytest -q",
                "RESTART_POLICY": "mudancas na API exigem restart do processo HTTP; docs isoladas nao exigem restart",
                "OPTIONAL_ENV_SETUP": textwrap.dedent(
                    """
                    export APP_ENV=dev
                    export SERVER_HOST=127.0.0.1
                    export SERVER_PORT=8000
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug}",
                "SMOKE_TEST_COMMAND": "python -m pytest -q",
            }
        )
    elif preset == "textual_cli":
        common.update(
            {
                "a capacidade principal": "oferecer uma interface textual operacional, local e auditavel",
                "o contexto operacional ou de negocio": "cockpit local para triagem, monitoramento e acoes humanas",
                "motivacao_1": "dar ao operador um cockpit local antes que a rotina vire script solto e opaco",
                "motivacao_2": "separar interface, estado operacional e comandos de diagnostico com intencao clara",
                "motivacao_3": "evitar acoplamento entre regra de negocio e rendering da interface textual",
                "entrypoint_1": f"python -m {project_slug} tui",
                "entrypoint_2": f"python -m {project_slug} doctor",
                "API / host / banco / fila / worker / PACS / browser / etc": "terminal do operador, textual, rich e fontes locais de estado",
                "risco_tecnico_principal": "misturar regra de negocio com rendering da interface e perder operabilidade fora da TUI",
                "passo_1": "definir quais estados aparecem no painel e quais ficam fora da interface",
                "passo_2": "separar fonte de dados, comando doctor e app Textual",
                "passo_3": "registrar fallback operacional sem TUI em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "estado operacional visivel, comandos de triagem e leitura consistente",
                "RUN_COMMAND": f"python -m {project_slug} tui",
                "VALIDACAO_MINIMA": f"python -m {project_slug} doctor",
                "RESTART_POLICY": "mudancas na TUI exigem nova execucao da interface; nao ha processo residente obrigatorio",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} tui",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} doctor",
            }
        )
    elif preset == "cli":
        common.update(
            {
                "a capacidade principal": "oferecer uma CLI clara, estavel e auditavel",
                "o contexto operacional ou de negocio": "automacao local ou operacional orientada a comando explicito",
                "motivacao_1": "registrar desde cedo um contrato de linha de comando defensavel e versionavel",
                "motivacao_2": "dar forma de produto a uma automacao que poderia nascer como script descartavel",
                "motivacao_3": "evitar proliferacao de comandos ad hoc sem dono, documentacao ou smoke claro",
                "entrypoint_1": f"python -m {project_slug}",
                "entrypoint_2": f"python -m {project_slug} --help",
                "API / host / banco / fila / worker / PACS / browser / etc": "shell do operador, filesystem e dependencias do host",
                "risco_tecnico_principal": "quebrar interface de linha de comando sem documentacao ou compatibilidade minima",
                "passo_1": "definir subcomandos e saida canonicamente",
                "passo_2": "documentar exemplos reais no README",
                "passo_3": "garantir smoke test dos comandos principais",
                "DOMINIO_CRITICO": "contrato da CLI e estabilidade de comandos",
                "RUN_COMMAND": f"python -m {project_slug} doctor",
                "VALIDACAO_MINIMA": f"python -m {project_slug} doctor",
                "RESTART_POLICY": "mudancas na CLI nao exigem restart; exigem nova execucao do comando",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} doctor",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} doctor",
            }
        )
    elif preset == "playwright_worker":
        common.update(
            {
                "a capacidade principal": "automatizar sessao de browser e ciclo recorrente de integracao web",
                "o contexto operacional ou de negocio": "worker orientado a browser automation, sessao persistida e integracao hostil",
                "motivacao_1": "isolar sessao, browser e loop recorrente antes que a integracao fique irreparavelmente frágil",
                "motivacao_2": "tratar browser automation como fronteira operacional propria, nao como detalhe incidental",
                "motivacao_3": "evitar scripts de login e scraping sem contrato de artefato, retry ou observabilidade",
                "entrypoint_1": f"python -m {project_slug} --interval 30 --dry-run",
                "entrypoint_2": f"python -m {project_slug} --refresh-session",
                "API / host / banco / fila / worker / PACS / browser / etc": "playwright, chromium e sistema web autenticado",
                "risco_tecnico_principal": "deixar login, sessao e scraping crescerem sem contrato de artefato nem regra de reautenticacao",
                "passo_1": "definir storage de sessao, sinais de expiracao e estrategia de relogin",
                "passo_2": "separar login, fetch e loop operacional",
                "passo_3": "registrar bootstrap do browser e instalacao do chromium em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "sessao autenticada, cookies e fronteira entre browser e worker",
                "RUN_COMMAND": f"python -m {project_slug} --interval 30 --dry-run",
                "VALIDACAO_MINIMA": f"python -m {project_slug} --once --dry-run",
                "RESTART_POLICY": "mudancas no worker ou no fluxo de browser exigem restart do processo residente",
                "OPTIONAL_ENV_SETUP": textwrap.dedent(
                    """
                    export APP_ENV=dev
                    python -m playwright install chromium
                    """
                ).strip(),
                "LOCAL_BOOT_COMMANDS": textwrap.dedent(
                    f"""
                    python3 -m venv .venv --prompt $(basename "$PWD")
                    source .venv/bin/activate
                    python -m pip install -r requirements.txt
                    python -m playwright install chromium
                    cp config/settings.example.json config/settings.local.json
                    """
                ).strip(),
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --interval 30 --dry-run",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} --once --dry-run",
            }
        )
    elif preset == "worker":
        common.update(
            {
                "a capacidade principal": "executar trabalho recorrente ou residente com regras explicitas de loop e retry",
                "o contexto operacional ou de negocio": "worker ou daemon leve orientado a fila, polling ou timer",
                "motivacao_1": "tirar a rotina recorrente do campo do improviso e colocá-la sob operacao explicita",
                "motivacao_2": "delimitar loop, retry, idempotencia e restart como responsabilidades centrais do repo",
                "motivacao_3": "evitar cron solto ou script residente sem contrato de falha e observabilidade minima",
                "entrypoint_1": f"python -m {project_slug} --once",
                "entrypoint_2": f"python -m {project_slug} --interval 30",
                "API / host / banco / fila / worker / PACS / browser / etc": "runtime local, scheduler e dependencias operacionais do worker",
                "risco_tecnico_principal": "loop residente sem observabilidade, retry ou criterio claro de falha",
                "passo_1": "definir unidade de trabalho e criterio de retry",
                "passo_2": "documentar execucao once vs residente",
                "passo_3": "registrar restart e sinais de falha no OPERATIONS.md",
                "DOMINIO_CRITICO": "unidade de trabalho, idempotencia e retry",
                "RUN_COMMAND": f"python -m {project_slug} --interval 30",
                "VALIDACAO_MINIMA": f"python -m {project_slug} --once",
                "RESTART_POLICY": "mudancas de codigo do worker exigem restart do processo residente",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --interval 30",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} --once",
            }
        )
    elif preset == "dicom_pipeline":
        common.update(
            {
                "a capacidade principal": "materializar metadados DICOM e agrupar estudos em manifestos reprodutiveis",
                "o contexto operacional ou de negocio": "pipeline local de ingestao DICOM com staging controlado",
                "motivacao_1": "materializar um fluxo DICOM reproduzivel antes que staging e identidade clinica se confundam",
                "motivacao_2": "isolar contratos de estudo, staging e materializacao em uma fronteira rastreavel",
                "motivacao_3": "evitar mistura entre ingestao bruta, enriquecimento e regras de reprocessamento",
                "entrypoint_1": f"python -m {project_slug} --sample",
                "entrypoint_2": f"python -m {project_slug} --inbox runtime/inbox --outbox runtime/outbox",
                "API / host / banco / fila / worker / PACS / browser / etc": "filesystem de staging, pydicom e contrato de estudo",
                "risco_tecnico_principal": "misturar identidades DICOM, staging e enriquecimento sem manifesto canonico",
                "passo_1": "definir manifesto minimo por estudo e invariantes de identificacao",
                "passo_2": "separar ingestao bruta, extração de cabecalho e materializacao",
                "passo_3": "registrar politicas de staging, limpeza e reprocessamento em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "StudyInstanceUID, identificadores canonicos e staging do pipeline",
                "RUN_COMMAND": f"python -m {project_slug} --inbox runtime/inbox --outbox runtime/outbox",
                "VALIDACAO_MINIMA": f"python -m {project_slug} --sample",
                "RESTART_POLICY": "mudancas de etapa exigem nova execucao do pipeline e revisao do staging local",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --inbox runtime/inbox --outbox runtime/outbox",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} --sample",
            }
        )
    elif preset == "pipeline":
        common.update(
            {
                "a capacidade principal": "orquestrar um fluxo em etapas com contratos explicitos de entrada e saida",
                "o contexto operacional ou de negocio": "pipeline batch ou incremental com runtime state controlado",
                "motivacao_1": "dar forma a um pipeline que precisa crescer por etapas sem perder rastreabilidade",
                "motivacao_2": "explicitar fronteira entre entrada, transformacao, materializacao e runtime state",
                "motivacao_3": "evitar que o fluxo vire um script longo sem contratos, checkpoints ou saida canonica",
                "entrypoint_1": f"python -m {project_slug} --once",
                "entrypoint_2": f"python -m {project_slug} --item-id demo-001",
                "API / host / banco / fila / worker / PACS / browser / etc": "fonte de entrada, staging local e destino final do pipeline",
                "risco_tecnico_principal": "crescer por etapas ad hoc sem contrato canonico entre elas",
                "passo_1": "definir input canonico e output canonico",
                "passo_2": "separar etapas e materializacoes",
                "passo_3": "documentar pipeline end-to-end e paths de runtime",
                "DOMINIO_CRITICO": "contratos de pipeline, staging e materializacao",
                "RUN_COMMAND": f"python -m {project_slug} --item-id demo-001",
                "VALIDACAO_MINIMA": f"python -m {project_slug} --item-id demo-001",
                "RESTART_POLICY": "mudancas de etapa exigem restart da execucao; dados em runtime nao podem ser sobrescritos sem intencao explicita",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --item-id demo-001",
                "SMOKE_TEST_COMMAND": f"python -m {project_slug} --item-id demo-001",
            }
        )

    common["VALIDACAO_MINIMA"] = prepend_gate_check(common["VALIDACAO_MINIMA"], gate_enforced)
    if gate_enforced:
        common["CI_GATE_STEP"] = (
            "      - name: Check project gate\n"
            "        run: python3 scripts/check_project_gate.py"
        )
    return common


def render_template(template_text: str, values: dict[str, str], runtime: str) -> str:
    rendered = template_text
    if runtime == "node":
        rendered = rendered.replace("settings.example.toml", "settings.example.json")
        rendered = rendered.replace("settings.local.toml", "settings.local.json")
        rendered = rendered.replace("main.py", "main.mjs")

    def replace(match: re.Match[str]) -> str:
        key = match.group(1).strip()
        return values.get(key, todo_value(key))

    return PLACEHOLDER_RE.sub(replace, rendered)


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    normalized = content
    if normalized.lstrip().startswith("#!"):
        normalized = normalized.lstrip()
    path.write_text(normalized.rstrip() + "\n", encoding="utf-8")
    if normalized.startswith("#!"):
        path.chmod(path.stat().st_mode | 0o755)


def runtime_process_defaults(runtime: str, project_slug: str, preset: str) -> tuple[str, str, str]:
    if runtime == "python":
        process_command = f"python -m {project_slug}"
        healthcheck_command = "python -m pytest -q"
        runtime_version = "3.11+"
        if preset == "cli":
            process_command = f"python -m {project_slug} doctor"
            healthcheck_command = f"python -m {project_slug} doctor"
        elif preset == "textual_cli":
            process_command = f"python -m {project_slug} tui"
            healthcheck_command = f"python -m {project_slug} doctor"
        elif preset == "worker":
            process_command = f"python -m {project_slug} --interval 30"
            healthcheck_command = f"python -m {project_slug} --once"
        elif preset == "playwright_worker":
            process_command = f"python -m {project_slug} --interval 30 --dry-run"
            healthcheck_command = f"python -m {project_slug} --once --dry-run"
        elif preset == "pipeline":
            process_command = f"python -m {project_slug} --item-id demo-001"
            healthcheck_command = f"python -m {project_slug} --item-id demo-001"
        elif preset == "dicom_pipeline":
            process_command = f"python -m {project_slug} --inbox runtime/inbox --outbox runtime/outbox"
            healthcheck_command = f"python -m {project_slug} --sample"
        return process_command, healthcheck_command, runtime_version

    if runtime == "node":
        return "npm start", "npm test", "20+"

    if runtime == "go":
        return f"go run ./cmd/{project_slug}", "go test ./...", "1.22+"

    if runtime == "ts":
        return "npm start", "npm test", "node20+ / typescript5+"

    if runtime == "swift":
        module_name = pascalize(project_slug)
        return f"swift run {module_name}", f"swift build && swift run {module_name}", "5.9+"

    if runtime == "csharp":
        project_name = pascalize(project_slug)
        return f"dotnet run --project src/{project_name}", "dotnet test", "8.0+"

    return "definido pelo projeto", "definido pelo projeto", "not-applicable"


def default_deploy_manifest(
    runtime: str,
    project_name: str,
    project_slug: str,
    preset: str,
) -> dict[str, object]:
    process_command, healthcheck_command, runtime_version = runtime_process_defaults(
        runtime,
        project_slug,
        preset,
    )
    optional_env = {
        "python": "APP_ENV",
        "node": "NODE_ENV",
        "ts": "NODE_ENV",
        "go": "APP_ENV",
        "swift": "APP_ENV",
        "csharp": "DOTNET_ENVIRONMENT",
    }.get(runtime)

    return {
        "version": 1,
        "project": {
            "name": project_name,
            "slug": project_slug,
        },
        "runtime": {
            "id": runtime,
            "version": runtime_version,
        },
        "deploy": {
            "target": "local",
            "reason": "baseline local gerada pelo Skidbladnir; ajuste antes de publicar ou operar em outro ambiente",
        },
        "process": {
            "command": process_command,
            "working_directory": ".",
            "user": "local operator",
        },
        "healthcheck": {
            "command": healthcheck_command,
            "timeout_seconds": 30,
        },
        "ports": [],
        "environment": {
            "required": [],
            "optional": [optional_env] if optional_env else [],
        },
        "secrets": {
            "required": [],
        },
        "runtime_state": {
            "paths": ["runtime/"],
        },
        "logs": {
            "paths": ["runtime/logs/"],
        },
        "restart": {
            "policy": "restart do processo quando codigo, configuracao ou manifesto de deploy mudar",
        },
        "backup": {
            "policy": "revisar runtime state antes de operar fora do ambiente local",
        },
        "rollback": {
            "strategy": "voltar para ultimo commit validado e reaplicar configuracao host-local preservada",
        },
    }


def default_logging_config() -> dict[str, object]:
    return {
        "version": 1,
        "formatters": {
            "json": {
                "type": "json",
                "required_fields": ["ts", "lvl", "svc", "mod", "evt", "msg"],
            }
        },
        "policy": {
            "rule": "logs devem ser estruturados e parseaveis",
            "example": {
                "ts": "2026-01-01T00:00:00+00:00",
                "lvl": "INFO",
                "svc": "service-name",
                "mod": "module-name",
                "evt": "startup",
                "msg": "servico inicializado",
            },
        },
    }


def default_doctor_config() -> dict[str, object]:
    return {
        "version": 1,
        "ignored_warnings": [],
        "token_alias_groups": [],
    }


def default_app_config(runtime: str, project_name: str, preset: str) -> tuple[str, dict[str, object]]:
    config_example_path = "config/settings.example.json"
    if runtime in {"node", "ts"}:
        config_payload: dict[str, object] = {
            "app": {
                "name": project_name,
                "env": "dev",
                "logLevel": "INFO",
            }
        }
        return config_example_path, config_payload

    config_payload = {
        "app": {
            "name": project_name,
            "env": "dev",
            "log_level": "INFO",
        }
    }

    if preset == "fastapi":
        config_payload["server"] = {"host": "127.0.0.1", "port": 8000}
    elif preset == "textual_cli":
        config_payload["tui"] = {"refresh_seconds": 2, "title": project_name}
    elif preset == "playwright_worker":
        config_payload["browser"] = {
            "storage_path": "runtime/browser/session.json",
            "login_url": "",
            "headless": True,
        }
    elif preset == "dicom_pipeline":
        config_payload["pipeline"] = {
            "inbox": "runtime/inbox",
            "outbox": "runtime/outbox",
            "accept_suffixes": [".dcm", ".dicom"],
        }

    return config_example_path, config_payload


def common_generated_files(
    runtime: str,
    project_name: str,
    project_slug: str,
    preset: str,
    gate_enforced: bool,
) -> dict[str, str]:
    config_example_path, config_payload = default_app_config(runtime, project_name, preset)
    files = {
        ".gitignore": textwrap.dedent(
            """
            # Runtime state
            runtime/**
            !runtime/.gitignore

            # Local configuration
            .env
            .env.*
            !.env.example
            config/*.local.toml
            config/*.local.json

            # Python
            .venv/
            __pycache__/
            *.py[cod]
            .pytest_cache/
            .ruff_cache/
            htmlcov/
            .coverage*

            # Node
            node_modules/
            coverage/

            # Go
            bin/

            # Build artifacts
            build/
            dist/

            # Editor / OS noise
            .DS_Store
            *.log
            """
        ),
        "runtime/.gitignore": "*\n!.gitignore\n",
        "config/logging.example.json": json.dumps(default_logging_config(), indent=2, ensure_ascii=True),
        "config/doctor.json": json.dumps(default_doctor_config(), indent=2, ensure_ascii=True),
        "deploy/manifest.json": json.dumps(
            default_deploy_manifest(runtime, project_name, project_slug, preset),
            indent=2,
            ensure_ascii=True,
        ),
        config_example_path: json.dumps(config_payload, indent=2, ensure_ascii=True),
    }

    if preset == "playwright_worker":
        files["runtime/browser/.gitignore"] = "*\n!.gitignore\n"

    return files


def python_generated_files(
    project_name: str,
    project_slug: str,
    preset: str,
    gate_enforced: bool,
) -> dict[str, str]:
    package_dir = project_slug
    dependencies: list[str] = []
    dev_dependencies = [
        "pytest>=8.0",
        "ruff>=0.6.0",
    ]

    if preset == "fastapi":
        dependencies.extend(
            [
                "fastapi>=0.115,<1",
                "uvicorn>=0.30,<1",
            ]
        )
        dev_dependencies.append("httpx>=0.27")
    elif preset == "textual_cli":
        dependencies.extend(
            [
                "rich>=13.7,<14",
                "textual>=0.58,<1",
            ]
        )
    elif preset == "playwright_worker":
        dependencies.extend(
            [
                "playwright>=1.58,<2",
                "requests>=2.31,<3",
            ]
        )
    elif preset == "dicom_pipeline":
        dependencies.append("pydicom>=2.4,<3")

    requirements_lines = dependencies + dev_dependencies

    files = {
        "requirements.txt": "\n".join(requirements_lines) + "\n",
        f"{package_dir}/__init__.py": textwrap.dedent(
            f'''
            """Pacote principal de {project_name}."""
            '''
        ),
        f"{package_dir}/__main__.py": textwrap.dedent(
            f"""
            import sys

            from {project_slug}.main import main


            if __name__ == "__main__":
                raise SystemExit(main(sys.argv[1:]))
            """
        ),
        f"{package_dir}/main.py": textwrap.dedent(
            f"""
            from __future__ import annotations

            import argparse

            from {project_slug}.infrastructure.config import load_settings
            from {project_slug}.infrastructure.logging import build_logger


            def main(argv: list[str] | None = None) -> int:
                parser = argparse.ArgumentParser(description="Entrypoint principal do projeto")
                parser.parse_args([] if argv is None else argv)
                settings = load_settings()
                logger = build_logger(settings.app.name, settings.app.log_level)
                logger.info("servico inicializado", extra={{"evt": "startup"}})
                return 0
            """
        ),
        f"{package_dir}/domain/__init__.py": '"""Camada de dominio."""\n',
        f"{package_dir}/application/__init__.py": '"""Casos de uso e orquestracao."""\n',
        f"{package_dir}/interfaces/__init__.py": '"""Interfaces externas do sistema."""\n',
        f"{package_dir}/infrastructure/__init__.py": '"""Infraestrutura e IO."""\n',
        f"{package_dir}/infrastructure/config.py": textwrap.dedent(
            f"""
            from __future__ import annotations

            import json
            import os
            from dataclasses import dataclass
            from pathlib import Path


            @dataclass
            class AppSettings:
                name: str
                env: str
                log_level: str


            @dataclass
            class Settings:
                app: AppSettings
                config_path: Path
                raw: dict[str, object]


            def _candidate_paths() -> list[Path]:
                env_path = os.getenv("{project_slug.upper()}_CONFIG_FILE")
                paths: list[Path] = []
                if env_path:
                    paths.append(Path(env_path))
                paths.append(Path("config/settings.local.json"))
                paths.append(Path("config/settings.example.json"))
                return paths


            def load_settings() -> Settings:
                for path in _candidate_paths():
                    if not path.exists():
                        continue

                    data = json.loads(path.read_text(encoding="utf-8"))
                    app_data = data.get("app", {{}})
                    return Settings(
                        app=AppSettings(
                            name=str(app_data.get("name", "{project_name}")),
                            env=str(app_data.get("env", "dev")),
                            log_level=str(app_data.get("log_level", "INFO")),
                        ),
                        config_path=path,
                        raw=data,
                    )

                return Settings(
                    app=AppSettings(
                        name="{project_name}",
                        env="dev",
                        log_level="INFO",
                    ),
                    config_path=Path("config/settings.example.json"),
                    raw={{}},
                )
            """
        ),
        f"{package_dir}/infrastructure/logging.py": textwrap.dedent(
            """
            from __future__ import annotations

            from datetime import datetime, timezone
            import json
            import logging
            import sys


            class JsonFormatter(logging.Formatter):
                def __init__(self, service_name: str) -> None:
                    super().__init__()
                    self.service_name = service_name

                def format(self, record: logging.LogRecord) -> str:
                    payload = {
                        "ts": datetime.now(timezone.utc).isoformat(),
                        "lvl": record.levelname,
                        "svc": self.service_name,
                        "mod": record.name,
                        "evt": getattr(record, "evt", "log"),
                        "msg": record.getMessage(),
                    }
                    return json.dumps(payload, ensure_ascii=True)


            def build_logger(service_name: str, level: str = "INFO") -> logging.Logger:
                logger = logging.getLogger(service_name)
                logger.setLevel(getattr(logging, level.upper(), logging.INFO))

                if logger.handlers:
                    return logger

                handler = logging.StreamHandler(sys.stdout)
                handler.setFormatter(JsonFormatter(service_name))
                logger.addHandler(handler)
                logger.propagate = False
                return logger
            """
        ),
        "tests/test_smoke.py": textwrap.dedent(
            f"""
            from {project_slug}.main import main


            def test_main_returns_zero() -> None:
                assert main() == 0
            """
        ),
    }

    if gate_enforced:
        files["tests/test_project_gate.py"] = textwrap.dedent(
            """
            import subprocess
            import sys
            from pathlib import Path


            def test_project_gate_is_filled() -> None:
                root = Path(__file__).resolve().parents[1]
                result = subprocess.run(
                    [sys.executable, str(root / "scripts" / "check_project_gate.py")],
                    capture_output=True,
                    text=True,
                    check=False,
                )
                assert result.returncode == 0, result.stdout + result.stderr
            """
        )

    return files


def preset_python_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    package_dir = project_slug

    if preset == "fastapi":
        return {
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import argparse
                import os
                import sys


                def main(argv: list[str] | None = None) -> int:
                    parser = argparse.ArgumentParser(description="Executa o servico HTTP")
                    parser.add_argument("--host", default=os.getenv("SERVER_HOST", "127.0.0.1"))
                    parser.add_argument("--port", type=int, default=int(os.getenv("SERVER_PORT", "8000")))
                    args = parser.parse_args([] if argv is None else argv)

                    import uvicorn

                    uvicorn.run(
                        "{project_slug}.interfaces.http.app:create_app",
                        factory=True,
                        host=args.host,
                        port=args.port,
                        reload=False,
                    )
                    return 0


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            f"{package_dir}/interfaces/http/__init__.py": '"""Interface HTTP do servico."""\n',
            f"{package_dir}/interfaces/http/app.py": textwrap.dedent(
                f"""
                from fastapi import FastAPI

                from {project_slug}.interfaces.http.routers.health import router as health_router


                def create_app() -> FastAPI:
                    app = FastAPI(title="{project_name}")
                    app.include_router(health_router)
                    return app
                """
            ),
            f"{package_dir}/interfaces/http/routers/__init__.py": '"""Routers HTTP do servico."""\n',
            f"{package_dir}/interfaces/http/routers/health.py": textwrap.dedent(
                """
                from fastapi import APIRouter


                router = APIRouter(tags=["health"])


                @router.get("/health")
                def health() -> dict[str, str]:
                    return {"status": "ok"}
                """
            ),
            "tests/test_http_health.py": textwrap.dedent(
                f"""
                from fastapi.testclient import TestClient

                from {project_slug}.interfaces.http.app import create_app


                def test_health_route() -> None:
                    client = TestClient(create_app())
                    response = client.get("/health")
                    assert response.status_code == 200
                    assert response.json() == {{"status": "ok"}}
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.interfaces.http.app import create_app


                def test_create_app() -> None:
                    app = create_app()
                    assert app.title == "{project_name}"
                """
            ),
        }

    if preset == "cli":
        return {
            f"{package_dir}/application/commands.py": textwrap.dedent(
                """
                def doctor() -> str:
                    return "ok"
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do sistema."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="CLI do projeto")
                    subparsers = parser.add_subparsers(dest="command", required=True)

                    doctor = subparsers.add_parser("doctor", help="valida baseline minima")
                    doctor.set_defaults(command="doctor")
                    return parser
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys

                from {project_slug}.application.commands import doctor
                from {project_slug}.interfaces.cli.parser import build_parser


                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)

                    if args.command == "doctor":
                        print(doctor())
                        return 0

                    parser.error("comando nao suportado")
                    return 2


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "tests/test_cli_doctor.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_doctor_command() -> None:
                    assert main(["doctor"]) == 0
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_doctor() -> None:
                    assert main(["doctor"]) == 0
                """
            ),
        }

    if preset == "textual_cli":
        return {
            f"{package_dir}/application/commands.py": textwrap.dedent(
                """
                def doctor() -> str:
                    return "ok"
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do cockpit textual."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="CLI com cockpit Textual")
                    subparsers = parser.add_subparsers(dest="command", required=True)

                    doctor = subparsers.add_parser("doctor", help="valida baseline minima")
                    doctor.set_defaults(command="doctor")

                    tui = subparsers.add_parser("tui", help="abre a interface textual")
                    tui.set_defaults(command="tui")
                    return parser
                """
            ),
            f"{package_dir}/interfaces/tui/__init__.py": '"""TUI do sistema."""\n',
            f"{package_dir}/interfaces/tui/app.py": textwrap.dedent(
                f"""
                from textual.app import App, ComposeResult
                from textual.binding import Binding
                from textual.widgets import Footer, Header, Static


                class DashboardApp(App[None]):
                    TITLE = "{project_name}"
                    SUB_TITLE = "Textual cockpit baseline"
                    BINDINGS = [
                        Binding("q", "quit", "Sair"),
                        Binding("r", "notify_refresh", "Refresh"),
                    ]
                    CSS = \"\"\"
                    Screen {{
                        align: center middle;
                        background: #132726;
                    }}

                    #hero {{
                        width: 72;
                        padding: 1 2;
                        border: round #4fd3d0;
                        background: #1a2f2e;
                        color: #edf4ef;
                    }}
                    \"\"\"

                    def compose(self) -> ComposeResult:
                        yield Header(show_clock=True)
                        yield Static(
                            "Preencha a fonte de dados operacional antes de crescer a TUI.\\n"
                            "Use doctor para smoke e mantenha a regra de negocio fora da interface.",
                            id="hero",
                        )
                        yield Footer()

                    def action_notify_refresh(self) -> None:
                        self.notify("refresh manual", timeout=1.5)


                def build_app() -> DashboardApp:
                    return DashboardApp()
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys

                from {project_slug}.application.commands import doctor
                from {project_slug}.interfaces.cli.parser import build_parser

                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)

                    if args.command == "doctor":
                        print(doctor())
                        return 0

                    if args.command == "tui":
                        from {project_slug}.interfaces.tui.app import build_app

                        build_app().run()
                        return 0

                    parser.error("comando nao suportado")
                    return 2


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "tests/test_textual_cli.py": textwrap.dedent(
                f"""
                from {project_slug}.interfaces.tui.app import build_app
                from {project_slug}.main import main


                def test_doctor_command() -> None:
                    assert main(["doctor"]) == 0


                def test_build_app() -> None:
                    app = build_app()
                    assert app.__class__.__name__ == "DashboardApp"
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_doctor() -> None:
                    assert main(["doctor"]) == 0
                """
            ),
        }

    if preset == "playwright_worker":
        return {
            f"{package_dir}/application/contracts.py": textwrap.dedent(
                """
                from __future__ import annotations

                from dataclasses import asdict, dataclass


                @dataclass
                class BrowserCookie:
                    name: str
                    value: str
                    domain: str = ""
                    path: str = "/"

                    @classmethod
                    def from_playwright_dict(cls, payload: dict[str, object]) -> "BrowserCookie":
                        return cls(
                            name=str(payload.get("name", "")),
                            value=str(payload.get("value", "")),
                            domain=str(payload.get("domain", "")),
                            path=str(payload.get("path", "/")),
                        )

                    def to_dict(self) -> dict[str, str]:
                        return asdict(self)


                @dataclass
                class SessionArtifacts:
                    cookies: list[BrowserCookie]
                    created_at_epoch: float
                    base_url: str = ""
                    notes: str = ""

                    def to_dict(self) -> dict[str, object]:
                        return {
                            "cookies": [cookie.to_dict() for cookie in self.cookies],
                            "created_at_epoch": self.created_at_epoch,
                            "base_url": self.base_url,
                            "notes": self.notes,
                        }

                    @classmethod
                    def from_dict(cls, payload: dict[str, object]) -> "SessionArtifacts":
                        raw_cookies = payload.get("cookies", [])
                        cookies = []
                        if isinstance(raw_cookies, list):
                            for item in raw_cookies:
                                if isinstance(item, dict):
                                    cookies.append(BrowserCookie.from_playwright_dict(item))
                        return cls(
                            cookies=cookies,
                            created_at_epoch=float(payload.get("created_at_epoch", 0.0) or 0.0),
                            base_url=str(payload.get("base_url", "")),
                            notes=str(payload.get("notes", "")),
                        )
                """
            ),
            f"{package_dir}/application/session.py": textwrap.dedent(
                """
                from __future__ import annotations

                import json
                import time
                from pathlib import Path

                from .contracts import BrowserCookie, SessionArtifacts


                def save_session_artifacts(path: str | Path, artifacts: SessionArtifacts) -> Path:
                    destination = Path(path).expanduser().resolve()
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.write_text(
                        json.dumps(artifacts.to_dict(), ensure_ascii=True, indent=2) + "\\n",
                        encoding="utf-8",
                    )
                    return destination


                def load_session_artifacts(path: str | Path) -> SessionArtifacts:
                    source = Path(path).expanduser().resolve()
                    payload = json.loads(source.read_text(encoding="utf-8"))
                    return SessionArtifacts.from_dict(payload)


                def build_placeholder_session(base_url: str = "") -> SessionArtifacts:
                    return SessionArtifacts(
                        cookies=[
                            BrowserCookie(
                                name="session",
                                value="placeholder",
                                domain="example.invalid",
                                path="/",
                            )
                        ],
                        created_at_epoch=time.time(),
                        base_url=base_url,
                        notes="TODO: substituir bootstrap placeholder por login real",
                    )
                """
            ),
            f"{package_dir}/application/worker.py": textwrap.dedent(
                """
                from __future__ import annotations

                import logging
                import time
                from pathlib import Path

                from .contracts import BrowserCookie, SessionArtifacts
                from .session import build_placeholder_session, save_session_artifacts


                def refresh_session(
                    logger: logging.Logger,
                    storage_path: Path,
                    *,
                    dry_run: bool = False,
                    show_browser: bool = False,
                    login_url: str = "",
                ) -> int:
                    if dry_run:
                        artifacts = build_placeholder_session(login_url)
                        save_session_artifacts(storage_path, artifacts)
                        logger.info("sessao de browser simulada", extra={"evt": "browser_session_dry_run"})
                        return 1

                    try:
                        from playwright.sync_api import sync_playwright
                    except ModuleNotFoundError as exc:
                        raise RuntimeError(
                            "playwright nao esta instalado; rode `python -m playwright install chromium`"
                        ) from exc

                    with sync_playwright() as playwright:
                        browser = playwright.chromium.launch(headless=not show_browser)
                        context = browser.new_context()
                        page = context.new_page()
                        if login_url:
                            page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
                        cookies = [
                            BrowserCookie.from_playwright_dict(item)
                            for item in context.cookies()
                        ]
                        browser.close()

                    artifacts = SessionArtifacts(
                        cookies=cookies,
                        created_at_epoch=time.time(),
                        base_url=login_url,
                        notes="TODO: inserir login real e validacao de sessao",
                    )
                    save_session_artifacts(storage_path, artifacts)
                    logger.info("sessao de browser atualizada", extra={"evt": "browser_session_refreshed"})
                    return 1


                def run_once(
                    logger: logging.Logger,
                    storage_path: Path,
                    *,
                    dry_run: bool = False,
                    show_browser: bool = False,
                    login_url: str = "",
                ) -> int:
                    return refresh_session(
                        logger,
                        storage_path,
                        dry_run=dry_run,
                        show_browser=show_browser,
                        login_url=login_url,
                    )


                def run_loop(
                    logger: logging.Logger,
                    interval_seconds: int,
                    storage_path: Path,
                    *,
                    once: bool = False,
                    dry_run: bool = False,
                    show_browser: bool = False,
                    login_url: str = "",
                ) -> int:
                    processed = run_once(
                        logger,
                        storage_path,
                        dry_run=dry_run,
                        show_browser=show_browser,
                        login_url=login_url,
                    )
                    if once:
                        return processed

                    while True:
                        time.sleep(interval_seconds)
                        run_once(
                            logger,
                            storage_path,
                            dry_run=dry_run,
                            show_browser=show_browser,
                            login_url=login_url,
                        )
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do worker Playwright."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="Worker com sessao de browser")
                    parser.add_argument("--once", action="store_true", help="executa um ciclo e sai")
                    parser.add_argument("--interval", type=int, default=30, help="intervalo entre ciclos")
                    parser.add_argument(
                        "--refresh-session",
                        action="store_true",
                        help="faz apenas o bootstrap/refresh dos artefatos de sessao",
                    )
                    parser.add_argument("--dry-run", action="store_true", help="gera artefatos placeholder sem abrir browser")
                    parser.add_argument("--show-browser", action="store_true", help="abre browser visivel no refresh real")
                    parser.add_argument("--login-url", default="", help="URL inicial para bootstrap de sessao")
                    return parser
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys
                from pathlib import Path

                from {project_slug}.application.worker import refresh_session, run_loop
                from {project_slug}.infrastructure.config import load_settings
                from {project_slug}.infrastructure.logging import build_logger
                from {project_slug}.interfaces.cli.parser import build_parser


                def _browser_storage_path(settings) -> Path:
                    browser = settings.raw.get("browser", {{}})
                    if isinstance(browser, dict):
                        configured = browser.get("storage_path")
                        if configured:
                            return Path(str(configured))
                    return Path("runtime/browser/session.json")


                def _login_url(settings, cli_value: str) -> str:
                    if cli_value:
                        return cli_value
                    browser = settings.raw.get("browser", {{}})
                    if isinstance(browser, dict):
                        return str(browser.get("login_url", "") or "")
                    return ""


                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)
                    settings = load_settings()
                    logger = build_logger(settings.app.name, settings.app.log_level)
                    storage_path = _browser_storage_path(settings)
                    login_url = _login_url(settings, args.login_url)

                    if args.refresh_session:
                        return refresh_session(
                            logger,
                            storage_path,
                            dry_run=args.dry_run,
                            show_browser=args.show_browser,
                            login_url=login_url,
                        )

                    return run_loop(
                        logger,
                        args.interval,
                        storage_path,
                        once=args.once,
                        dry_run=args.dry_run,
                        show_browser=args.show_browser,
                        login_url=login_url,
                    )


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "tests/test_playwright_worker.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_worker_dry_run_creates_session_artifact(tmp_path, monkeypatch) -> None:
                    monkeypatch.chdir(tmp_path)
                    assert main(["--once", "--dry-run"]) == 1
                    assert (tmp_path / "runtime" / "browser" / "session.json").exists()
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_dry_run(tmp_path, monkeypatch) -> None:
                    monkeypatch.chdir(tmp_path)
                    assert main(["--once", "--dry-run"]) == 1
                """
            ),
        }

    if preset == "worker":
        return {
            f"{package_dir}/application/worker.py": textwrap.dedent(
                """
                from __future__ import annotations

                import logging
                import time


                def run_once(logger: logging.Logger) -> int:
                    logger.info("ciclo executado", extra={"evt": "worker_cycle"})
                    return 1


                def run_loop(logger: logging.Logger, interval_seconds: int, *, once: bool = False) -> int:
                    processed = run_once(logger)
                    if once:
                        return processed

                    while True:
                        time.sleep(interval_seconds)
                        run_once(logger)
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do worker."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="Worker residente")
                    parser.add_argument("--once", action="store_true", help="executa um ciclo e sai")
                    parser.add_argument("--interval", type=int, default=30, help="intervalo entre ciclos")
                    return parser
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys

                from {project_slug}.application.worker import run_loop
                from {project_slug}.infrastructure.logging import build_logger
                from {project_slug}.interfaces.cli.parser import build_parser


                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)
                    logger = build_logger("{project_name}")
                    return run_loop(logger, args.interval, once=args.once)


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "tests/test_worker_once.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_worker_once() -> None:
                    assert main(["--once"]) == 1
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_once() -> None:
                    assert main(["--once"]) == 1
                """
            ),
        }

    if preset == "dicom_pipeline":
        return {
            f"{package_dir}/application/contracts.py": textwrap.dedent(
                """
                from __future__ import annotations

                from dataclasses import asdict, dataclass


                @dataclass
                class StudyManifest:
                    study_instance_uid: str
                    accession_number: str
                    patient_name: str
                    file_count: int
                    files: list[str]

                    def to_dict(self) -> dict[str, object]:
                        return asdict(self)
                """
            ),
            f"{package_dir}/application/pipeline.py": textwrap.dedent(
                """
                from __future__ import annotations

                import json
                from pathlib import Path

                import pydicom
                from pydicom.dataset import FileDataset, FileMetaDataset
                from pydicom.uid import ExplicitVRLittleEndian, SecondaryCaptureImageStorage, generate_uid

                from .contracts import StudyManifest


                def iter_dicom_files(inbox: Path) -> list[Path]:
                    accepted = {".dcm", ".dicom"}
                    return sorted(path for path in inbox.rglob("*") if path.is_file() and path.suffix.lower() in accepted)


                def build_study_manifests(inbox: Path) -> list[StudyManifest]:
                    grouped: dict[str, dict[str, object]] = {}

                    for dicom_path in iter_dicom_files(inbox):
                        dataset = pydicom.dcmread(str(dicom_path), stop_before_pixels=True, force=True)
                        study_uid = str(getattr(dataset, "StudyInstanceUID", "") or "unknown-study")
                        patient_name = str(getattr(dataset, "PatientName", "") or "").strip()
                        accession_number = str(getattr(dataset, "AccessionNumber", "") or "").strip()
                        state = grouped.setdefault(
                            study_uid,
                            {
                                "study_instance_uid": study_uid,
                                "accession_number": accession_number,
                                "patient_name": patient_name,
                                "files": [],
                            },
                        )
                        state["files"].append(str(dicom_path))
                        if not state["accession_number"] and accession_number:
                            state["accession_number"] = accession_number
                        if not state["patient_name"] and patient_name:
                            state["patient_name"] = patient_name

                    manifests = []
                    for state in grouped.values():
                        files = [str(item) for item in state["files"]]
                        manifests.append(
                            StudyManifest(
                                study_instance_uid=str(state["study_instance_uid"]),
                                accession_number=str(state["accession_number"]),
                                patient_name=str(state["patient_name"]),
                                file_count=len(files),
                                files=files,
                            )
                        )
                    return manifests


                def write_manifests(manifests: list[StudyManifest], outbox: Path) -> list[Path]:
                    outbox.mkdir(parents=True, exist_ok=True)
                    written = []
                    for manifest in manifests:
                        destination = outbox / f"{manifest.study_instance_uid}.json"
                        destination.write_text(
                            json.dumps(manifest.to_dict(), ensure_ascii=True, indent=2) + "\\n",
                            encoding="utf-8",
                        )
                        written.append(destination)
                    return written


                def run_pipeline(inbox: Path, outbox: Path) -> list[Path]:
                    manifests = build_study_manifests(inbox)
                    return write_manifests(manifests, outbox)


                def write_sample_dicom(inbox: Path) -> Path:
                    inbox.mkdir(parents=True, exist_ok=True)
                    destination = inbox / "sample.dcm"

                    file_meta = FileMetaDataset()
                    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
                    file_meta.MediaStorageSOPInstanceUID = generate_uid()
                    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

                    dataset = FileDataset(str(destination), {}, file_meta=file_meta, preamble=b"\\0" * 128)
                    dataset.PatientName = "SAMPLE^PATIENT"
                    dataset.AccessionNumber = "ACC-001"
                    dataset.StudyInstanceUID = generate_uid()
                    dataset.SeriesInstanceUID = generate_uid()
                    dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
                    dataset.Modality = "OT"
                    dataset.is_little_endian = True
                    dataset.is_implicit_VR = False
                    dataset.save_as(str(destination), write_like_original=False)
                    return destination
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do pipeline DICOM."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="Executa pipeline DICOM local")
                    parser.add_argument("--inbox", default="runtime/inbox", help="diretorio de entrada")
                    parser.add_argument("--outbox", default="runtime/outbox", help="diretorio de saida")
                    parser.add_argument("--sample", action="store_true", help="gera um DICOM de exemplo antes de processar")
                    return parser
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys
                from pathlib import Path

                from {project_slug}.application.pipeline import run_pipeline, write_sample_dicom
                from {project_slug}.interfaces.cli.parser import build_parser


                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)
                    inbox = Path(args.inbox)
                    outbox = Path(args.outbox)

                    if args.sample:
                        write_sample_dicom(inbox)

                    outputs = run_pipeline(inbox, outbox)
                    for output in outputs:
                        print(output)
                    return 0


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "runtime/inbox/.gitignore": "*\n!.gitignore\n",
            "runtime/outbox/.gitignore": "*\n!.gitignore\n",
            "tests/test_dicom_pipeline.py": textwrap.dedent(
                f"""
                import json

                from {project_slug}.application.pipeline import run_pipeline, write_sample_dicom


                def test_dicom_pipeline_writes_manifest(tmp_path) -> None:
                    inbox = tmp_path / "inbox"
                    outbox = tmp_path / "outbox"
                    write_sample_dicom(inbox)
                    outputs = run_pipeline(inbox, outbox)
                    assert len(outputs) == 1
                    payload = json.loads(outputs[0].read_text(encoding="utf-8"))
                    assert payload["file_count"] == 1
                    assert payload["study_instance_uid"]
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_sample(tmp_path, monkeypatch) -> None:
                    monkeypatch.chdir(tmp_path)
                    assert main(["--sample"]) == 0
                """
            ),
        }

    if preset == "pipeline":
        return {
            f"{package_dir}/application/contracts.py": textwrap.dedent(
                """
                from __future__ import annotations

                from dataclasses import dataclass


                @dataclass
                class PipelineItem:
                    item_id: str
                    payload: dict
                """
            ),
            f"{package_dir}/application/pipeline.py": textwrap.dedent(
                """
                from __future__ import annotations

                import json
                from pathlib import Path

                from .contracts import PipelineItem


                def extract(item_id: str) -> PipelineItem:
                    return PipelineItem(item_id=item_id, payload={"item_id": item_id, "status": "extracted"})


                def transform(item: PipelineItem) -> PipelineItem:
                    item.payload["status"] = "transformed"
                    return item


                def load(item: PipelineItem, output_dir: Path) -> Path:
                    output_dir.mkdir(parents=True, exist_ok=True)
                    destination = output_dir / f"{item.item_id}.json"
                    destination.write_text(json.dumps(item.payload, ensure_ascii=True, indent=2), encoding="utf-8")
                    return destination


                def run_pipeline(item_id: str, output_dir: Path) -> Path:
                    item = extract(item_id)
                    item = transform(item)
                    return load(item, output_dir)
                """
            ),
            f"{package_dir}/interfaces/cli/__init__.py": '"""CLI do pipeline."""\n',
            f"{package_dir}/interfaces/cli/parser.py": textwrap.dedent(
                """
                from __future__ import annotations

                import argparse


                def build_parser() -> argparse.ArgumentParser:
                    parser = argparse.ArgumentParser(description="Executa pipeline em etapas")
                    parser.add_argument("--item-id", default="demo-001", help="identificador do item")
                    parser.add_argument("--once", action="store_true", help="mantido para compatibilidade operacional")
                    return parser
                """
            ),
            f"{package_dir}/main.py": textwrap.dedent(
                f"""
                from __future__ import annotations

                import sys
                from pathlib import Path

                from {project_slug}.application.pipeline import run_pipeline
                from {project_slug}.interfaces.cli.parser import build_parser


                def main(argv: list[str] | None = None) -> int:
                    parser = build_parser()
                    args = parser.parse_args([] if argv is None else argv)
                    output = run_pipeline(args.item_id, Path("runtime/outbox"))
                    print(output)
                    return 0


                if __name__ == "__main__":
                    raise SystemExit(main(sys.argv[1:]))
                """
            ),
            "runtime/inbox/.gitignore": "*\n!.gitignore\n",
            "runtime/outbox/.gitignore": "*\n!.gitignore\n",
            "tests/test_pipeline_once.py": textwrap.dedent(
                f"""
                from pathlib import Path

                from {project_slug}.application.pipeline import run_pipeline


                def test_pipeline_writes_output(tmp_path: Path) -> None:
                    output = run_pipeline("demo-001", tmp_path)
                    assert output.exists()
                """
            ),
            "tests/test_smoke.py": textwrap.dedent(
                f"""
                from {project_slug}.main import main


                def test_smoke_pipeline() -> None:
                    assert main(["--item-id", "demo-001"]) == 0
                """
            ),
        }

    return {}


def node_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    dist_name = project_slug.replace("_", "-")
    base_dir = project_slug
    return {
        "package.json": json.dumps(
            {
                "name": dist_name,
                "version": "0.1.0",
                "private": True,
                "type": "module",
                "scripts": {
                    "start": f"node {base_dir}/main.mjs",
                    "test": "node --test tests/*.test.mjs",
                },
                "engines": {"node": ">=20"},
            },
            indent=2,
            ensure_ascii=True,
        ),
        f"{base_dir}/main.mjs": textwrap.dedent(
            f"""
            import {{ loadSettings }} from "./infrastructure/config.mjs";
            import {{ logEvent }} from "./infrastructure/logger.mjs";


            export function main() {{
              const settings = loadSettings();
              logEvent({{
                lvl: settings.app.logLevel,
                svc: settings.app.name,
                mod: "main",
                evt: "startup",
                msg: "service initialized"
              }});
              return 0;
            }}


            if (import.meta.url === `file://${{process.argv[1]}}`) {{
              process.exit(main());
            }}
            """
        ),
        f"{base_dir}/domain/.gitkeep": "",
        f"{base_dir}/application/.gitkeep": "",
        f"{base_dir}/interfaces/.gitkeep": "",
        f"{base_dir}/infrastructure/config.mjs": textwrap.dedent(
            f"""
            import fs from "node:fs";
            import process from "node:process";


            function candidatePaths() {{
              const envPath = process.env.{project_slug.upper()}_CONFIG_FILE;
              return [envPath, "config/settings.local.json", "config/settings.example.json"].filter(Boolean);
            }}


            export function loadSettings() {{
              for (const path of candidatePaths()) {{
                if (!fs.existsSync(path)) {{
                  continue;
                }}

                const payload = JSON.parse(fs.readFileSync(path, "utf-8"));
                return {{
                  app: {{
                    name: payload.app?.name ?? "{project_name}",
                    env: payload.app?.env ?? process.env.NODE_ENV ?? "dev",
                    logLevel: payload.app?.logLevel ?? "INFO"
                  }},
                  configPath: path
                }};
              }}

              return {{
                app: {{
                  name: "{project_name}",
                  env: process.env.NODE_ENV ?? "dev",
                  logLevel: "INFO"
                }},
                configPath: null
              }};
            }}
            """
        ),
        f"{base_dir}/infrastructure/logger.mjs": textwrap.dedent(
            """
            export function logEvent(payload = {}) {
              const event = {
                ts: payload.ts ?? new Date().toISOString(),
                lvl: payload.lvl ?? "INFO",
                svc: payload.svc ?? "service-name",
                mod: payload.mod ?? "main",
                evt: payload.evt ?? "log",
                msg: payload.msg ?? "",
                ...payload
              };
              process.stdout.write(`${JSON.stringify(event)}\\n`);
            }
            """
        ),
        "tests/smoke.test.mjs": textwrap.dedent(
            f"""
            import test from "node:test";
            import assert from "node:assert/strict";
            import {{ main }} from "../{project_slug}/main.mjs";


            test("main returns zero", () => {{
              assert.equal(main(), 0);
            }});
            """
        ),
    }


def go_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    module_name = kebabify(project_name)
    env_prefix = project_slug.upper()
    return {
        "go.mod": textwrap.dedent(
            f"""
            module {module_name}

            go 1.22
            """
        ),
        f"cmd/{project_slug}/main.go": textwrap.dedent(
            f"""
            package main

            import (
                "os"

                "{module_name}/internal/app"
            )

            func main() {{
                os.Exit(app.Run(os.Stdout))
            }}
            """
        ),
        "internal/app/app.go": textwrap.dedent(
            f"""
            package app

            import (
                "encoding/json"
                "fmt"
                "io"
                "os"
                "time"
            )

            type Settings struct {{
                App struct {{
                    Name     string `json:"name"`
                    Env      string `json:"env"`
                    LogLevel string `json:"log_level"`
                }} `json:"app"`
            }}

            type LogEvent struct {{
                TS  string `json:"ts"`
                Lvl string `json:"lvl"`
                Svc string `json:"svc"`
                Mod string `json:"mod"`
                Evt string `json:"evt"`
                Msg string `json:"msg"`
            }}

            func Run(output io.Writer) int {{
                settings := loadSettings()
                event := LogEvent{{
                    TS:  time.Now().UTC().Format(time.RFC3339),
                    Lvl: defaultText(settings.App.LogLevel, "INFO"),
                    Svc: defaultText(settings.App.Name, "{project_name}"),
                    Mod: "main",
                    Evt: "startup",
                    Msg: "service initialized",
                }}
                if err := json.NewEncoder(output).Encode(event); err != nil {{
                    fmt.Fprintln(os.Stderr, err)
                    return 1
                }}
                return 0
            }}

            func loadSettings() Settings {{
                for _, path := range candidatePaths() {{
                    if path == "" {{
                        continue
                    }}
                    payload, err := os.ReadFile(path)
                    if err != nil {{
                        continue
                    }}
                    var settings Settings
                    if err := json.Unmarshal(payload, &settings); err == nil {{
                        return settings
                    }}
                }}
                var settings Settings
                settings.App.Name = "{project_name}"
                settings.App.Env = defaultText(os.Getenv("APP_ENV"), "dev")
                settings.App.LogLevel = "INFO"
                return settings
            }}

            func candidatePaths() []string {{
                return []string{{
                    os.Getenv("{env_prefix}_CONFIG_FILE"),
                    "config/settings.local.json",
                    "config/settings.example.json",
                }}
            }}

            func defaultText(value string, fallback string) string {{
                if value == "" {{
                    return fallback
                }}
                return value
            }}
            """
        ),
        "internal/app/app_test.go": textwrap.dedent(
            """
            package app

            import (
                "bytes"
                "encoding/json"
                "testing"
            )

            func TestRunWritesStartupEvent(t *testing.T) {
                var output bytes.Buffer
                if code := Run(&output); code != 0 {
                    t.Fatalf("Run() code = %d, want 0", code)
                }

                var event LogEvent
                if err := json.Unmarshal(output.Bytes(), &event); err != nil {
                    t.Fatalf("startup event is not JSON: %v", err)
                }
                if event.Evt != "startup" {
                    t.Fatalf("event = %q, want startup", event.Evt)
                }
            }
            """
        ),
    }


def ts_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    dist_name = kebabify(project_name)
    env_prefix = project_slug.upper()
    return {
        "package.json": json.dumps(
            {
                "name": dist_name,
                "version": "0.1.0",
                "private": True,
                "type": "module",
                "scripts": {
                    "build": "tsc -p tsconfig.json",
                    "start": "npm run build && node dist/src/main.js",
                    "test": "npm run build && node --test dist/tests/*.test.js",
                },
                "engines": {"node": ">=20"},
                "devDependencies": {
                    "@types/node": "^20.0.0",
                    "typescript": "^5.0.0",
                },
            },
            indent=2,
            ensure_ascii=True,
        ),
        "tsconfig.json": json.dumps(
            {
                "compilerOptions": {
                    "target": "ES2022",
                    "module": "NodeNext",
                    "moduleResolution": "NodeNext",
                    "strict": True,
                    "rootDir": ".",
                    "outDir": "dist",
                    "declaration": True,
                    "skipLibCheck": True,
                },
                "include": ["src/**/*.ts", "tests/**/*.ts"],
            },
            indent=2,
            ensure_ascii=True,
        ),
        "src/main.ts": textwrap.dedent(
            f"""
            import fs from "node:fs";
            import process from "node:process";

            type Settings = {{
              app?: {{
                name?: string;
                env?: string;
                logLevel?: string;
                log_level?: string;
              }};
            }};

            type LogEvent = {{
              ts: string;
              lvl: string;
              svc: string;
              mod: string;
              evt: string;
              msg: string;
            }};

            function candidatePaths(): string[] {{
              return [
                process.env.{env_prefix}_CONFIG_FILE,
                "config/settings.local.json",
                "config/settings.example.json"
              ].filter((value): value is string => Boolean(value));
            }}

            function loadSettings(): Settings {{
              for (const path of candidatePaths()) {{
                if (!fs.existsSync(path)) {{
                  continue;
                }}
                return JSON.parse(fs.readFileSync(path, "utf-8")) as Settings;
              }}
              return {{}};
            }}

            export function startupEvent(): LogEvent {{
              const settings = loadSettings();
              return {{
                ts: new Date().toISOString(),
                lvl: settings.app?.logLevel ?? settings.app?.log_level ?? "INFO",
                svc: settings.app?.name ?? "{project_name}",
                mod: "main",
                evt: "startup",
                msg: "service initialized"
              }};
            }}

            export function main(): number {{
              process.stdout.write(`${{JSON.stringify(startupEvent())}}\\n`);
              return 0;
            }}

            if (import.meta.url === `file://${{process.argv[1]}}`) {{
              process.exit(main());
            }}
            """
        ),
        "tests/smoke.test.ts": textwrap.dedent(
            """
            import test from "node:test";
            import assert from "node:assert/strict";
            import { startupEvent } from "../src/main.js";

            test("startup event is structured", () => {
              const event = startupEvent();
              assert.equal(event.evt, "startup");
              assert.ok(event.ts);
            });
            """
        ),
    }


def swift_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    module_name = pascalize(project_slug)
    core_name = f"{module_name}Core"
    return {
        "Package.swift": textwrap.dedent(
            f"""
            // swift-tools-version: 5.9
            import PackageDescription

            let package = Package(
                name: "{module_name}",
                platforms: [
                    .macOS(.v13)
                ],
                products: [
                    .executable(name: "{module_name}", targets: ["{module_name}"])
                ],
                targets: [
                    .target(name: "{core_name}"),
                    .executableTarget(name: "{module_name}", dependencies: ["{core_name}"])
                ]
            )
            """
        ),
        f"Sources/{core_name}/App.swift": textwrap.dedent(
            f"""
            import Foundation

            public struct LogEvent: Codable {{
                public let ts: String
                public let lvl: String
                public let svc: String
                public let mod: String
                public let evt: String
                public let msg: String
            }}

            public enum App {{
                public static func startupEvent(now: Date = Date()) -> LogEvent {{
                    let formatter = ISO8601DateFormatter()
                    return LogEvent(
                        ts: formatter.string(from: now),
                        lvl: "INFO",
                        svc: "{project_name}",
                        mod: "main",
                        evt: "startup",
                        msg: "service initialized"
                    )
                }}

                public static func run() -> Int32 {{
                    let event = startupEvent()
                    let encoder = JSONEncoder()
                    guard let payload = try? encoder.encode(event), let line = String(data: payload, encoding: .utf8) else {{
                        return 1
                    }}
                    print(line)
                    return 0
                }}
            }}
            """
        ),
        f"Sources/{module_name}/main.swift": textwrap.dedent(
            f"""
            import {core_name}

            _ = App.run()
            """
        ),
    }


def csharp_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    project = pascalize(project_slug)
    test_project = f"{project}.Tests"
    return {
        f"{project}.sln": "\n".join(
            [
                "Microsoft Visual Studio Solution File, Format Version 12.00",
                "# Visual Studio Version 17",
                "VisualStudioVersion = 17.0.31903.59",
                "MinimumVisualStudioVersion = 10.0.40219.1",
                f'Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{project}", "src\\{project}\\{project}.csproj", "{{11111111-1111-1111-1111-111111111111}}"',
                "EndProject",
                f'Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{test_project}", "tests\\{test_project}\\{test_project}.csproj", "{{22222222-2222-2222-2222-222222222222}}"',
                "EndProject",
                "Global",
                "EndGlobal",
            ]
        ),
        f"src/{project}/{project}.csproj": textwrap.dedent(
            """
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <OutputType>Exe</OutputType>
                <TargetFramework>net8.0</TargetFramework>
                <ImplicitUsings>enable</ImplicitUsings>
                <Nullable>enable</Nullable>
              </PropertyGroup>
            </Project>
            """
        ),
        f"src/{project}/Program.cs": textwrap.dedent(
            f"""
            using System.Text.Json;

            namespace {project};

            public record LogEvent(string Ts, string Lvl, string Svc, string Mod, string Evt, string Msg);

            public static class App
            {{
                public static LogEvent StartupEvent() =>
                    new(DateTimeOffset.UtcNow.ToString("O"), "INFO", "{project_name}", "main", "startup", "service initialized");

                public static int Run(TextWriter output)
                {{
                    output.WriteLine(JsonSerializer.Serialize(StartupEvent()));
                    return 0;
                }}
            }}

            public static class Program
            {{
                public static int Main() => App.Run(Console.Out);
            }}
            """
        ),
        f"tests/{test_project}/{test_project}.csproj": textwrap.dedent(
            f"""
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <TargetFramework>net8.0</TargetFramework>
                <ImplicitUsings>enable</ImplicitUsings>
                <Nullable>enable</Nullable>
                <IsPackable>false</IsPackable>
              </PropertyGroup>
              <ItemGroup>
                <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.10.0" />
                <PackageReference Include="xunit" Version="2.9.0" />
                <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
              </ItemGroup>
              <ItemGroup>
                <ProjectReference Include="../../src/{project}/{project}.csproj" />
              </ItemGroup>
            </Project>
            """
        ),
        f"tests/{test_project}/AppTests.cs": textwrap.dedent(
            f"""
            using {project};
            using Xunit;

            namespace {test_project};

            public class AppTests
            {{
                [Fact]
                public void StartupEventIsStructured()
                {{
                    var evt = App.StartupEvent();
                    Assert.Equal("startup", evt.Evt);
                    Assert.False(string.IsNullOrWhiteSpace(evt.Ts));
                }}
            }}
            """
        ),
    }


def generic_generated_files(project_slug: str) -> dict[str, str]:
    base_dir = project_slug
    return {
        f"{base_dir}/domain/.gitkeep": "",
        f"{base_dir}/application/.gitkeep": "",
        f"{base_dir}/infrastructure/.gitkeep": "",
        f"{base_dir}/interfaces/.gitkeep": "",
        "tests/.gitkeep": "",
    }


def generate_files(
    runtime: str,
    project_name: str,
    project_slug: str,
    preset: str,
    gate_enforced: bool,
) -> dict[str, str]:
    files = common_generated_files(runtime, project_name, project_slug, preset, gate_enforced)
    if runtime == "python":
        files.update(python_generated_files(project_name, project_slug, preset, gate_enforced))
        files.update(preset_python_files(project_name, project_slug, preset))
    elif runtime == "node":
        files.update(node_generated_files(project_name, project_slug, preset))
    elif runtime == "go":
        files.update(go_generated_files(project_name, project_slug, preset))
    elif runtime == "ts":
        files.update(ts_generated_files(project_name, project_slug, preset))
    elif runtime == "swift":
        files.update(swift_generated_files(project_name, project_slug, preset))
    elif runtime == "csharp":
        files.update(csharp_generated_files(project_name, project_slug, preset))
    else:
        files.update(generic_generated_files(project_slug))
    return files


def render_and_write_templates(
    destination: Path,
    runtime: str,
    preset: str,
    project_name: str,
    project_slug: str,
    repo_url: str,
    include_checklist: bool,
    include_papers: bool,
    gate_enforced: bool,
) -> None:
    values = runtime_defaults(runtime, preset, project_name, project_slug, repo_url, gate_enforced)
    if include_papers:
        values["OPTIONAL_RESEARCH_STRUCTURE"] = "├── papers/\n│   └── README.md              # contexto cientifico, metodo e avaliacao\n"
        values["OPTIONAL_RESEARCH_DOCS"] = "- `papers/`: hipótese, método, métricas, avaliação e discussão científica associada ao software\n"
    template_files = dict(TEMPLATE_FILES)
    if include_checklist:
        template_files.update(OPTIONAL_TEMPLATE_FILES)
    if include_papers:
        template_files.update(OPTIONAL_STRUCTURE_TEMPLATE_FILES)

    for relative_path, source_path in template_files.items():
        source_text = source_path.read_text(encoding="utf-8")
        rendered_text = render_template(source_text, values, runtime)
        write_text(destination / relative_path, rendered_text)

    script_template_files = dict(SCRIPT_TEMPLATE_FILES)
    if gate_enforced:
        script_template_files.update(GATE_ENFORCEMENT_TEMPLATE_FILES)
    for relative_path, source_path in script_template_files.items():
        source_text = source_path.read_text(encoding="utf-8")
        rendered_text = render_template(source_text, values, runtime)
        write_text(destination / relative_path, rendered_text)

    for relative_path, source_path in SCHEMA_TEMPLATE_FILES.items():
        source_text = source_path.read_text(encoding="utf-8")
        rendered_text = render_template(source_text, values, runtime)
        write_text(destination / relative_path, rendered_text)

    workflow_template = WORKFLOW_TEMPLATE_FILES.get(runtime)
    if workflow_template is not None:
        source_text = workflow_template.read_text(encoding="utf-8")
        rendered_text = render_template(source_text, values, runtime)
        write_text(destination / ".github" / "workflows" / "ci.yml", rendered_text)

    for relative_path, content in generate_files(runtime, project_name, project_slug, preset, gate_enforced).items():
        write_text(destination / relative_path, content)


def ensure_destination(destination: Path, force: bool) -> None:
    if destination.exists() and not destination.is_dir():
        raise NotADirectoryError(f"o destino {destination} existe, mas nao e um diretorio")
    if destination.exists() and any(destination.iterdir()) and not force:
        raise FileExistsError(
            f"o diretorio {destination} ja existe e nao esta vazio; use --force se quiser sobrescrever"
        )
    destination.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera um projeto novo a partir do starter kit de arquitetura."
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {STARTER_VERSION}",
    )
    parser.add_argument("target", nargs="?", help="diretorio de destino do novo projeto")
    parser.add_argument(
        "--name",
        help="nome do projeto exibido nos arquivos (default: nome da pasta de destino)",
    )
    parser.add_argument(
        "--slug",
        help="slug tecnico do projeto (default: derivado do nome em snake_case)",
    )
    parser.add_argument(
        "--runtime",
        choices=("python", "node", "ts", "go", "swift", "csharp", "generic"),
        default="python",
        help="runtime base do scaffolding (default: python)",
    )
    parser.add_argument(
        "--preset",
        choices=PRESET_CHOICES,
        default="base",
        help="preset estrutural do projeto (default: base)",
    )
    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="lista os presets disponiveis e sai",
    )
    parser.add_argument(
        "--repo-url",
        help="URL do repositorio remoto para preencher no README",
    )
    parser.add_argument(
        "--include-checklist",
        action="store_true",
        help="inclui START_CHECKLIST.md no projeto gerado",
    )
    parser.add_argument(
        "--include-papers",
        action="store_true",
        help="inclui papers/ para contexto cientifico associado ao software",
    )
    parser.add_argument(
        "--enforce-gate",
        action="store_true",
        help="ativa enforcement do PROJECT_GATE.md via hook local e teste de validacao",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="permite gerar em diretorio ja existente e nao vazio",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.list_presets:
        print_available_presets()
        return 0

    if not args.target:
        raise SystemExit("informe o diretorio de destino ou use --list-presets")

    preset = canonicalize_preset(args.preset)
    destination = Path(args.target).expanduser().resolve()
    project_name = args.name or destination.name
    project_slug = args.slug or slugify(project_name)
    repo_url = args.repo_url or f"git@github.com:SEU_USUARIO/{kebabify(project_name)}.git"

    if preset != "base" and args.runtime != "python":
        raise SystemExit("presets estruturais atualmente exigem --runtime python")

    ensure_destination(destination, args.force)
    render_and_write_templates(
        destination=destination,
        runtime=args.runtime,
        preset=preset,
        project_name=project_name,
        project_slug=project_slug,
        repo_url=repo_url,
        include_checklist=args.include_checklist,
        include_papers=args.include_papers,
        gate_enforced=args.enforce_gate,
    )

    print(f"Projeto criado em: {destination}")
    print(f"Runtime: {args.runtime}")
    print(f"Preset: {args.preset}")
    print(f"Slug tecnico: {project_slug}")
    print(f"Preencha primeiro: {destination / 'PROJECT_GATE.md'}")
    if args.enforce_gate:
        print("Gate enforcement ativo: rode `bash scripts/install_git_hooks.sh` apos `git init`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
