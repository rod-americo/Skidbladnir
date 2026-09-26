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
CATALOG = json.loads((TEMPLATE_DIR / "runtimes" / "catalog.json").read_text(encoding="utf-8"))
RUNTIMES = CATALOG["runtimes"]
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
    "docs/TASK_TEMPLATE.md": COMMON_TEMPLATE_DIR / "docs" / "TASK_TEMPLATE.md",
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
    "java": TEMPLATE_DIR / ".github" / "workflows" / "ci-java.yml",
    "generic": TEMPLATE_DIR / ".github" / "workflows" / "ci-generic.yml",
    "rust": TEMPLATE_DIR / ".github" / "workflows" / "ci-rust.yml",
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
    "base": "baseline mínimo com layout convencional e núcleo testável",
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
    print("Runtimes e combinações disponíveis (nenhum runtime é default):")
    for runtime, profile in RUNTIMES.items():
        print(f"- {runtime}: {', '.join(item.replace('_', '-') for item in profile['presets'])}")
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

    profile = RUNTIMES[runtime]
    if runtime != "generic":
        badges.append(f"![{profile['name']}](https://img.shields.io/badge/{runtime}-{profile['version']}-blue)")

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

    common = {
        "PROJECT_NAME": project_name,
        "PROJECT_SLUG": project_slug,
        "PROJECT_PHASE": "prototipo",
        "REPO_URL": repo_url,
        "README_BADGES": default_readme_badges(runtime, repo_url),
        "OPTIONAL_RESEARCH_STRUCTURE": "",
        "OPTIONAL_RESEARCH_DOCS": "",
        "RUNTIME_STRUCTURE": textwrap.dedent(
            f"""
            ├── {project_slug}/
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
        "RESTART_POLICY": "preencher regra de restart por tipo de mudanca",
        "RUNTIME_ID": runtime,
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
        "PRIMARY_RUN_COMMAND": "preencher comando principal",
        "config_local": "preencher arquivo local",
        "obs": "preencher observacao",
        "CI_GATE_STEP": "",
        "CI_DEPLOY_STEP": "      - name: Check deploy manifest\n        run: python3 scripts/check_deploy_manifest.py",
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
                "RUN_COMMAND": f"python -m {project_slug}",
                "RESTART_POLICY": "mudancas de codigo Python exigem restart do processo; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug}",
                "config_local": "config/settings.local.json",
                "logger": f"{project_slug}.infrastructure.logging",
                "storage": "filesystem local ou banco definido pelo projeto",
            }
        )
    elif runtime == "node":
        common.update(
            {
                "RUN_COMMAND": "npm start",
                "RESTART_POLICY": "mudancas em codigo Node exigem restart do processo; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": "npm start",
                "config_local": "config/settings.local.json",
                "logger": f"{project_slug}/infrastructure/logger.mjs",
                "storage": "filesystem local ou banco definido pelo projeto",
            }
        )
    elif runtime == "go":
        common.update(
            {
                "RUN_COMMAND": f"go run ./cmd/{project_slug}",
                "RESTART_POLICY": "mudancas em codigo Go exigem rebuild/restart do processo; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": f"go run ./cmd/{project_slug}",
                "config_local": "config/settings.local.json",
                "logger": "JSON em stdout; implementação em internal/app",
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
                "RUN_COMMAND": "npm start",
                "RESTART_POLICY": "mudancas em TypeScript exigem rebuild e restart do processo; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": "npm start",
                "config_local": "config/settings.local.json",
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
                "RUN_COMMAND": f"swift run {swift_module}",
                "RESTART_POLICY": "mudancas em Swift exigem rebuild/restart do binario; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": f"swift run {swift_module}",
                "config_local": "config/settings.local.json",
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
        csharp_solution = f"{csharp_project}.sln"
        csharp_project_file = f"src/{csharp_project}/{csharp_project}.csproj"
        common.update(
            {
                "RUN_COMMAND": f"dotnet run --project {csharp_project_file}",
                "RESTART_POLICY": "mudancas em C# exigem rebuild/restart do processo; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": f"dotnet run --project {csharp_project_file}",
                "config_local": "config/settings.local.json",
                "logger": f"src/{csharp_project}",
                "storage": "filesystem local ou banco definido pelo projeto",
                "entrypoint_1": f"dotnet run --project {csharp_project_file}",
                "entrypoint_2": f"dotnet test {csharp_solution}",
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
                "RUN_COMMAND": "preencher comando de execucao",
                "PRIMARY_RUN_COMMAND": "preencher comando principal",
                "config_local": "config/settings.local.json",
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
                "RESTART_POLICY": "mudancas na API exigem restart do processo HTTP; docs isoladas nao exigem restart",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug}",
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
                "entrypoint_1": "python -m tui",
                "entrypoint_2": f"python -m {project_slug} doctor",
                "API / host / banco / fila / worker / PACS / browser / etc": "terminal do operador, textual, rich e fontes locais de estado",
                "risco_tecnico_principal": "misturar regra de negocio com rendering da interface e perder operabilidade fora da TUI",
                "passo_1": "definir quais estados aparecem no painel e quais ficam fora da interface",
                "passo_2": "separar fonte de dados, comando doctor e app Textual",
                "passo_3": "registrar fallback operacional sem TUI em docs/OPERATIONS.md",
                "DOMINIO_CRITICO": "estado operacional visivel, comandos de triagem e leitura consistente",
                "RUN_COMMAND": "python -m tui",
                "RESTART_POLICY": "mudancas na TUI exigem nova execucao da interface; nao ha processo residente obrigatorio",
                "PRIMARY_RUN_COMMAND": "python -m tui",
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
                "RESTART_POLICY": "mudancas na CLI nao exigem restart; exigem nova execucao do comando",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} doctor",
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
                "RESTART_POLICY": "mudancas no worker ou no fluxo de browser exigem restart do processo residente",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --interval 30 --dry-run",
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
                "RESTART_POLICY": "mudancas de codigo do worker exigem restart do processo residente",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --interval 30",
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
                "RESTART_POLICY": "mudancas de etapa exigem nova execucao do pipeline e revisao do staging local",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --inbox runtime/inbox --outbox runtime/outbox",
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
                "RESTART_POLICY": "mudancas de etapa exigem restart da execucao; dados em runtime nao podem ser sobrescritos sem intencao explicita",
                "PRIMARY_RUN_COMMAND": f"python -m {project_slug} --item-id demo-001",
            }
        )

    commands = runtime_commands(runtime, project_slug, preset)
    profile = RUNTIMES[runtime]
    common.update({
        "PRIMARY_RUNTIME": f"{profile['name']} {profile['version']}",
        "runtime": f"{profile['name']} {profile['version']}",
        "PRIMARY_RUNTIME_VERSION": profile["version"],
        "DEPENDENCY_FILE": profile["dependency_file"].format(module=pascalize(project_slug)),
        "SETUP_COMMANDS": commands["setup"],
        "LOCAL_BOOT_COMMANDS": commands["setup"] + "\ncp config/settings.example.json config/settings.local.json",
        "VALIDACAO_MINIMA": commands["test"],
        "TEST_COMMAND": commands["test"],
        "CI_VALIDATE_COMMAND": commands["test"],
        "CI_STATIC_CHECK_COMMAND": commands["build"],
        "SMOKE_TEST_COMMAND": commands["smoke"],
        "HEALTHCHECK_DESCRIPTION": "nenhum probe configurado; implantação ainda não declarada",
        "PYTHON_VERSION": RUNTIMES["python"]["version"],
        "NODE_VERSION": RUNTIMES["node"]["version"],
        "GO_VERSION": RUNTIMES["go"]["version"],
        "DOTNET_VERSION": RUNTIMES["csharp"]["version"],
        "JAVA_VERSION": RUNTIMES["java"]["version"],
        "RUST_VERSION": RUNTIMES["rust"]["version"],
        "SWIFT_VERSION": RUNTIMES["swift"]["version"],
        "SWIFT_CONTAINER": RUNTIMES["swift"]["container"],
        "DOTNET_RESTORE_COMMAND": runtime_commands("csharp", project_slug)["setup"],
        "CI_SETUP_PYTHON": "      - name: Set up validation Python\n        uses: " + CATALOG["actions"]["python"] + "\n        with:\n          python-version: \"" + CATALOG["validation_python"] + "\"",
        "CONFIG_DESCRIPTION": "O baseline lê settings.local.json ou settings.example.json; a variável " + env_prefix + "_CONFIG_FILE seleciona outro arquivo." if uses_config(runtime, preset) else "Exemplo de configuração para adaptação; este baseline ainda não lê esse arquivo.",
        "OPTIONAL_ENV_SETUP": "# Ajuste somente as entradas documentadas em OPERATIONS.md.",
        "ENV_1": env_prefix + "_CONFIG_FILE" if uses_config(runtime, preset) else "nenhuma variável consumida pelo baseline",
        "ENV_2": "nenhuma outra variável obrigatória no baseline",
        "runtime_path": "sem estado persistente no baseline",
        "logs_path": "stdout; nenhum arquivo de log criado pelo baseline",
    })
    common.update({"ACTION_" + key.upper(): value for key, value in CATALOG["actions"].items()})
    if preset == "base":
        common.update({"RUN_COMMAND": commands["run"], "PRIMARY_RUN_COMMAND": commands["run"], "entrypoint_1": commands["run"], "entrypoint_2": commands["test"]})
    if runtime == "generic":
        common["RUNTIME_STRUCTURE"] = "├── src/ (adapte somente se houver código)"
    if runtime in {"python", "node"} and preset == "base":
        common["RUNTIME_STRUCTURE"] = f"├── {project_slug}/\n│   └── entrypoint e configuração do programa"
    if runtime in {"java", "rust"}:
        common.update({
            "RUNTIME_STRUCTURE": "├── src/\n│   └── código e testes conforme convenção do runtime",
            "config_local": "config/settings.local.json",
            "logger": "logger JSON em stdout",
            "RESTART_POLICY": "recompilar após mudanças; o baseline é um comando local finito",
        })
    if preset == "fastapi":
        common["HEALTHCHECK_DESCRIPTION"] = "HTTP GET http://127.0.0.1:8000/health (ajuste junto de SERVER_HOST e SERVER_PORT)"
    if preset in {"pipeline", "dicom_pipeline", "playwright_worker"}:
        common["runtime_path"] = ", ".join(default_deploy_manifest(runtime, project_name, project_slug, preset)["runtime_state"]["paths"])
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


def uses_config(runtime: str, preset: str) -> bool:
    return runtime in {"node", "ts", "go", "java", "rust"} or (runtime == "python" and preset in {"base", "fastapi", "playwright_worker"})


def runtime_commands(runtime: str, project_slug: str, preset: str = "base") -> dict[str, str]:
    values = {"slug": project_slug, "dist": project_slug.replace("_", "-"), "module": pascalize(project_slug), "sources": project_slug + (" tui" if preset == "textual_cli" else "")}
    return {key: str(RUNTIMES[runtime][key]).format(**values) for key in ("setup", "run", "test", "build", "smoke")}


def runtime_process_defaults(runtime: str, project_slug: str, preset: str) -> tuple[str, str, str]:
    commands = runtime_commands(runtime, project_slug, preset)
    run = commands["run"]
    if runtime == "python":
        suffixes = {"cli": " doctor", "worker": " --interval 30", "playwright_worker": " --interval 30 --dry-run", "pipeline": " --item-id demo-001", "dicom_pipeline": " --inbox runtime/inbox --outbox runtime/outbox"}
        run += suffixes.get(preset, "")
        if preset == "textual_cli":
            run = "python -m tui"
    return run, commands["smoke"], RUNTIMES[runtime]["version"]


def default_deploy_manifest(runtime: str, project_name: str, project_slug: str, preset: str) -> dict[str, object]:
    command, _, version = runtime_process_defaults(runtime, project_slug, preset)
    http = runtime == "python" and preset == "fastapi"
    paths = {"playwright_worker": ["runtime/browser/session.json"], "pipeline": ["runtime/outbox/"], "dicom_pipeline": ["runtime/inbox/", "runtime/outbox/"]}.get(preset, [])
    reason = "serviço HTTP local de exemplo; reveja o contrato antes de implantar"
    if not http:
        reason = "baseline sem implantação configurada; comando local documentado"
        if preset in {"worker", "playwright_worker"}:
            reason = "worker de exemplo sem supervisão ou probe seguro; configure antes de implantar"
    manifest = json.loads((TEMPLATE_DIR / "deploy/manifest.json").read_text(encoding="utf-8"))
    manifest.update({
        "project": {"name": project_name, "slug": project_slug},
        "runtime": {"id": runtime, "version": version},
        "deploy": {"target": "local" if http else "none", "reason": reason},
        "process": {"command": command, "working_directory": "."} if runtime != "generic" else {},
        "healthcheck": {"http": {"url": "http://127.0.0.1:8000/health"}, "timeout_seconds": 5} if http else {},
        "ports": [8000] if http else [],
        "environment": {"required": [], "optional": ([project_slug.upper() + "_CONFIG_FILE"] if uses_config(runtime, preset) else []) + (["SERVER_HOST", "SERVER_PORT"] if http else [])},
        "runtime_state": {"paths": paths},
    })
    if http:
        manifest["restart"]["policy"] = "reiniciar processo após alteração de código ou configuração"
    if paths:
        manifest["backup"]["policy"] = "preservar os artefatos nos caminhos de estado antes de reprocessar"
    return manifest


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

    if preset == "textual_cli":
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
            .mypy_cache/
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
            target/
            .build/
            obj/

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
                "engines": {"node": RUNTIMES["node"]["version"]},
            },
            indent=2,
            ensure_ascii=True,
        ),
        f"{base_dir}/main.mjs": textwrap.dedent(
            """
            import { loadSettings } from "./infrastructure/config.mjs";
            import { logEvent } from "./infrastructure/logger.mjs";


            export function main() {
              const settings = loadSettings();
              logEvent({
                lvl: settings.app.logLevel,
                svc: settings.app.name,
                mod: "main",
                evt: "startup",
                msg: "service initialized"
              });
              return 0;
            }


            if (import.meta.url === `file://${process.argv[1]}`) {
              process.exit(main());
            }
            """
        ),
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

            go 1.27.0

            toolchain go{RUNTIMES["go"]["version"]}
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
    dist_name = project_slug.replace("_", "-")
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
                "engines": {"node": RUNTIMES["node"]["version"]},
                "devDependencies": {
                    "@types/node": "24.10.1",
                    "typescript": "5.9.3",
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
            // swift-tools-version: 6.4
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
                    .executableTarget(name: "{module_name}", dependencies: ["{core_name}"]),
                    .testTarget(name: "{module_name}Tests", dependencies: ["{core_name}"])
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

            import Foundation

            exit(App.run())
            """
        ),
    }


def csharp_generated_files(project_name: str, project_slug: str, preset: str) -> dict[str, str]:
    project = pascalize(project_slug)
    test_project = f"{project}.Tests"
    app_guid = "11111111-1111-1111-1111-111111111111"
    test_guid = "22222222-2222-2222-2222-222222222222"
    return {
        f"{project}.sln": "\n".join(
            [
                "Microsoft Visual Studio Solution File, Format Version 12.00",
                "# Visual Studio Version 17",
                "VisualStudioVersion = 17.0.31903.59",
                "MinimumVisualStudioVersion = 10.0.40219.1",
                f'Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{project}", "src\\{project}\\{project}.csproj", "{{{app_guid}}}"',
                "EndProject",
                f'Project("{{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC}}") = "{test_project}", "tests\\{test_project}\\{test_project}.csproj", "{{{test_guid}}}"',
                "EndProject",
                "Global",
                "\tGlobalSection(SolutionConfigurationPlatforms) = preSolution",
                "\t\tDebug|Any CPU = Debug|Any CPU",
                "\t\tRelease|Any CPU = Release|Any CPU",
                "\tEndGlobalSection",
                "\tGlobalSection(ProjectConfigurationPlatforms) = postSolution",
                f"\t\t{{{app_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU",
                f"\t\t{{{app_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU",
                f"\t\t{{{app_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU",
                f"\t\t{{{app_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU",
                f"\t\t{{{test_guid}}}.Debug|Any CPU.ActiveCfg = Debug|Any CPU",
                f"\t\t{{{test_guid}}}.Debug|Any CPU.Build.0 = Debug|Any CPU",
                f"\t\t{{{test_guid}}}.Release|Any CPU.ActiveCfg = Release|Any CPU",
                f"\t\t{{{test_guid}}}.Release|Any CPU.Build.0 = Release|Any CPU",
                "\tEndGlobalSection",
                "\tGlobalSection(SolutionProperties) = preSolution",
                "\t\tHideSolutionNode = FALSE",
                "\tEndGlobalSection",
                "EndGlobal",
            ]
        ),
        f"src/{project}/{project}.csproj": textwrap.dedent(
            """
            <Project Sdk="Microsoft.NET.Sdk">
              <PropertyGroup>
                <OutputType>Exe</OutputType>
                <TargetFramework>net10.0</TargetFramework>
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
                    output.WriteLine(JsonSerializer.Serialize(StartupEvent(), new JsonSerializerOptions {{ PropertyNamingPolicy = JsonNamingPolicy.CamelCase }}));
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
                <TargetFramework>net10.0</TargetFramework>
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
                public void RunWritesCanonicalJsonFields()
                {{
                    using var output = new StringWriter();
                    Assert.Equal(0, App.Run(output));
                    using var json = System.Text.Json.JsonDocument.Parse(output.ToString());
                    Assert.Equal("startup", json.RootElement.GetProperty("evt").GetString());
                    Assert.Equal("INFO", json.RootElement.GetProperty("lvl").GetString());
                    Assert.True(DateTimeOffset.TryParse(json.RootElement.GetProperty("ts").GetString(), out _));
                }}

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
    return {
        "src/.gitkeep": "",
    }


def runtime_template_files(runtime: str, project_name: str, project_slug: str, directory: str = "files") -> dict[str, str]:
    source = TEMPLATE_DIR / "runtimes" / runtime / directory
    values = {
        "PROJECT_NAME": project_name,
        "PROJECT_NAME_LITERAL": json.dumps(project_name, ensure_ascii=False),
        "PROJECT_SLUG": project_slug,
        "DIST_NAME": project_slug.replace("_", "-"),
        "MODULE": pascalize(project_slug),
        "MODULE_LOWER": pascalize(project_slug).lower(),
        "ENV_PREFIX": project_slug.upper(),
        "JAVA_PACKAGE": "local.project_" + project_slug,
        "JAVA_PACKAGE_PATH": "local/project_" + project_slug,
        "RUST_CRATE": "project_" + project_slug,
        "RUST_VERSION": RUNTIMES["rust"]["version"],
    }
    return {
        render_template(str(path.relative_to(source)), values, runtime): render_template(path.read_text(encoding="utf-8"), values, runtime)
        for path in sorted(source.rglob("*")) if path.is_file()
    }


def generate_files(
    runtime: str,
    project_name: str,
    project_slug: str,
    preset: str,
    gate_enforced: bool,
) -> dict[str, str]:
    files = common_generated_files(runtime, project_name, project_slug, preset, gate_enforced)
    if runtime == "node":
        files.update(node_generated_files(project_name, project_slug, preset))
    elif runtime == "go":
        files.update(go_generated_files(project_name, project_slug, preset))
    elif runtime == "ts":
        files.update(ts_generated_files(project_name, project_slug, preset))
    elif runtime == "swift":
        files.update(swift_generated_files(project_name, project_slug, preset))
    elif runtime == "csharp":
        files.update(csharp_generated_files(project_name, project_slug, preset))
    elif runtime == "generic":
        files.update(generic_generated_files(project_slug))
    files.update(runtime_template_files(runtime, project_name, project_slug))
    if runtime == "python":
        files.update(runtime_template_files(runtime, project_name, project_slug, "presets/" + preset))
        if not gate_enforced:
            files.pop("tests/test_project_gate.py", None)
        if preset == "base":
            for package in ("domain", "application", "interfaces"):
                files.pop(f"{project_slug}/{package}/__init__.py", None)
        dependency_profile = RUNTIMES["python"]["dependency_profiles"][preset]
        for filename in ("requirements.in", "requirements.txt"):
            lock = TEMPLATE_DIR / "runtimes" / "python" / "requirements" / dependency_profile / filename
            files[filename] = lock.read_text(encoding="utf-8")
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
        choices=tuple(RUNTIMES),
        help="runtime explícito, escolhido pelas restrições do projeto; sem default",
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

    if args.runtime is None:
        raise SystemExit("geração exige --runtime explícito; consulte --list-presets e docs/runtimes.md")

    preset = canonicalize_preset(args.preset)
    destination = Path(args.target).expanduser().resolve()
    project_name = args.name or destination.name
    project_slug = args.slug or slugify(project_name)
    if not re.fullmatch(r"[a-z][a-z0-9_]*", project_slug):
        raise SystemExit("--slug deve começar com letra minúscula e conter somente letras, números e underscore")
    if any(ord(char) < 32 for char in project_name):
        raise SystemExit("--name não pode conter caracteres de controle")
    repo_url = args.repo_url or f"git@github.com:SEU_USUARIO/{kebabify(project_name)}.git"

    if preset not in RUNTIMES[args.runtime]["presets"]:
        raise SystemExit(f"runtime {args.runtime} suporta apenas: {', '.join(RUNTIMES[args.runtime]["presets"])}; o protocolo admite adaptação por agente")

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
