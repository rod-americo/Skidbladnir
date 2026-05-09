from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


STARTER_ROOT = Path(__file__).resolve().parents[1]
SCAFFOLDER = STARTER_ROOT / "scaffold_project.py"
INSTALL_SCRIPT = STARTER_ROOT / "install_newproj.sh"
RUNNER = STARTER_ROOT / "run_regression_suite.py"
NEWPROJ = STARTER_ROOT / "bin" / "newproj"
KIT_VERSION = (STARTER_ROOT / "VERSION").read_text(encoding="utf-8").strip()


def run_cmd(command: list[str], cwd: Path | None = None, expected: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        command,
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != expected:
        raise AssertionError(
            f"comando falhou: {command}\n"
            f"esperado={expected} obtido={result.returncode}\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )
    return result


def write_valid_docs(repo: Path, project_name: str, slug: str) -> None:
    (repo / "README.md").write_text(
        f"""# {project_name}

Daemon operacional para reconciliacao remota de cargas assincronas.
Existe para a equipe de integracao e para o host local que opera o ciclo.

## O que este repositorio e

- daemon autonomo para reconciliacao remota de cargas assincronas
- componente duravel focado em coleta ciclica
- fronteira separada porque lida com browser, polling e isolamento local

## O que este repositorio NAO e

- servico HTTP para consulta manual
- repositorio de contratos clinicos
- lugar para dashboards ou ETL generico

## Estado atual

- fase: `funcional`
- runtime principal: `python3.11`
- entrypoints principais:
  - `python -m {slug}.main --interval 30`
  - `python -m {slug}.main --once`
- dependencia externa critica:
  - `portal autenticado e filesystem local`

## Baseline arquitetural

- camadas preservadas em `domain`, `application`, `infrastructure` e `interfaces`
- runtime state isolado em `runtime/`
- configuracao local mantida fora do versionamento por `config/settings.local.json`

## Quick start

### 1. Clonar

```bash
git clone git@github.com:example/{slug}.git
cd {project_name}
```

### 2. Preparar ambiente

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Configurar

```bash
cp config/settings.example.json config/settings.local.json
export APP_ENV=dev
```

### 4. Rodar

```bash
python -m {slug}.main --interval 30
```

## Configuracao

| Entrada | Tipo | Obrigatorio | Origem | Exemplo |
| --- | --- | --- | --- | --- |
| `{slug.upper()}_CONFIG_FILE` | `env` | sim | `host` | `config/settings.local.json` |
| `APP_ENV` | `env` | nao | `host` | `dev` |

## Contratos e fronteiras

- entrada canonica: comando de execucao com target identificavel
- saida canonica: manifesto consolidado em `runtime/outbox`
- inferencias externas ficam marcadas em `docs/CONTRACTS.md`
- limites com sistemas vizinhos ficam em `docs/ARCHITECTURE.md`

## Persistencia e runtime

- manifestos, caches e artefatos locais ficam em `runtime/`
- logs operacionais ficam em `runtime/logs/worker.log`
- configuracao local fica em `config/settings.local.json`

## Validacao

- `python3 scripts/check_project_gate.py`
- `python3 scripts/project_doctor.py`
- `python -m {slug}.main --once`
- `python -m pytest -q`

## Documentacao do repositorio

- `AGENTS.md`: regras de colaboracao
- `PROJECT_GATE.md`: justificativa e fronteira
- `config/doctor.json`: aliases e excecoes conscientes do doctor
- `docs/ARCHITECTURE.md`: desenho do sistema
- `docs/CONTRACTS.md`: contratos e identificadores
- `docs/OPERATIONS.md`: execucao e restart

## Regras operacionais

- commits em `en-US` no formato `type(scope): summary`
- documentacao humana em `pt-BR`
- toda mudanca de operacao atualiza `docs/OPERATIONS.md`

## Riscos e limites atuais

- risco principal: `sessao expirada ou loop sem criterio claro de falha`
- dependencia mais fragil: `portal autenticado do parceiro`
- maior divida tecnica conhecida: `reatenticacao automatica ainda simplificada`

## Proximos passos

1. endurecer criterio de retry e limite de erro consecutivo
2. materializar manifesto consolidado com schema fixo
3. publicar sinais operacionais minimos no logger estruturado
""",
        encoding="utf-8",
    )

    (repo / "AGENTS.md").write_text(
        f"""# AGENTS.md

## 1. Ordem minima de leitura

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/CONTRACTS.md`
4. `docs/OPERATIONS.md`
5. `docs/DECISIONS.md`

## 2. Regras de colaboracao

- documentacao humana em `pt-BR`
- identificadores tecnicos e commits em `en-US`
- preservar a separacao `domain / application / infrastructure / interfaces`
- nao empilhar dashboards, HTTP manual ou ETL generico neste repositorio

## 3. Politica de commit e push

- manter um commit por mudanca logica
- preferir commits curtos, intencionais e faceis de reverter
- revisar diff e validacao antes de push para remoto

## 4. Validacao obrigatoria

- revisar `git diff`
- declarar impacto de restart quando houver
- atualizar docs estruturais quando o comportamento mudar

## 5. Doctor e gate

- gate check local: `python3 scripts/check_project_gate.py`
- doctor estrutural: `python3 scripts/project_doctor.py`
- doctor estrito: `python3 scripts/project_doctor.py --strict`
- doctor audit: `python3 scripts/project_doctor.py --audit-config`
- policy do doctor: `config/doctor.json`
- comando de validacao minima: `python -m {slug}.main --once`

## 6. Extensoes especificas do repositorio

- dominio critico: `consolidacao de manifestos, retry e reprocessamento`
- dependencia externa critica: `portal autenticado do parceiro`
- dados sensiveis: `cookies de sessao e manifestos operacionais`
- host principal: `worker local no host de integracao`
- regra de restart: `mudancas em codigo residente exigem restart do processo`
""",
        encoding="utf-8",
    )

    (repo / "PROJECT_GATE.md").write_text(
        """# PROJECT GATE

Documento preenchido antes do primeiro commit relevante.

## 1. Por que este projeto existe?

- problema real: operacao manual quebrada para sincronizar lotes vindos do portal parceiro com retries consistentes.
- usuario ou operador alvo: operador de integracao responsavel por acompanhar lotes pendentes no host local.
- resultado esperado: worker residente capaz de sincronizar dados e materializar manifestos confiaveis.

## 2. Por que isto NAO deveria ser um modulo?

- repositorio candidato que poderia absorver isso: Heimdallr
- por que esse acoplamento seria inadequado: misturaria sessao, loop residente e operacao local com uma fronteira que hoje e centrada em ingestao e supervisao.
- fronteira que justifica um repositório separado: ciclo operacional proprio, runtime state proprio e dependencia autenticada com regras de retry independentes.

## 3. O que este projeto compartilha com o ecossistema?

- configuracao: usa config settings local e env vars seguindo o padrao dos outros workers.
- logging: usa logger estruturado em JSON com evento, modulo e severidade.
- runtime: materializa artefatos apenas em runtime e nao no worktree principal.
- contratos: manifesta entrada, saida e identificadores em docs contracts.
- autenticacao ou transporte: reaproveita transporte HTTP autenticado, mas isola a sessao deste worker.

## 4. O que este projeto NAO pode carregar?

- responsabilidades fora de escopo: expor API HTTP, manter dashboards e fazer ETL generico.
- integrações que pertencem a outro sistema: contratos clinicos e sincronizacao mestre com PACS central.
- dados que nao devem morar aqui: estudos clinicos integrais, dumps historicos e credenciais fora da sessao operacional.

## 5. Qual e o custo de manutencao esperado?

- host ou ambiente principal: host local de integracao com execucao residente controlada.
- dependencia externa mais fragil: portal autenticado com sessao expirada e HTML instavel.
- necessidade de restart: qualquer mudanca em loop, parser ou sessao exige restart do processo residente.
- necessidade de backup: apenas manifestos consolidados e logs estruturados relevantes para auditoria local.
- risco operacional: duplicar lotes ou perder reprocessamento se a sessao quebrar sem sinalizacao clara.

## 6. Condicao de saida

Este repositório so deveria existir se:

- houver fronteira de escopo defensavel
- houver contrato de entrada e saida identificavel
- houver operacao propria ou ciclo de evolucao independente
- o custo de mais um repo for menor que o custo de acoplamento
""",
        encoding="utf-8",
    )

    (repo / "docs" / "ARCHITECTURE.md").write_text(
        """# ARCHITECTURE

## 1. Objetivo

Executar consolidacao recorrente de manifestos remotos em um worker isolado.

## 2. Escopo

Inclui:

- consolidar manifestos remotos com sessao autenticada
- reprocessar lotes pendentes com retry controlado

Nao inclui:

- servico HTTP para consulta manual
- dashboards operacionais e ETL generico

## 3. Contexto do sistema

Entradas externas:

- portal autenticado do parceiro
- fila local de lotes pendentes

Saidas externas:

- manifesto consolidado em runtime outbox
- sinal operacional em logs estruturados

Dependencias criticas:

- portal autenticado do parceiro
- configuracao host local e runtime state

## 4. Modulos principais

### 4.1 Domain

- lote pendente
- manifesto consolidado
- politicas de idempotencia

### 4.2 Application

- coleta e consolidacao do lote
- politica de retry
- orquestracao do ciclo residente

### 4.3 Infrastructure

- cliente HTTP autenticado
- filesystem de runtime
- logger estruturado

### 4.4 Interfaces

- entrypoint de worker
- comando once
- comando interval

## 5. Fluxo principal

1. carregar configuracao local e sessao valida
2. coletar lotes pendentes do portal autenticado
3. consolidar dados em manifesto normalizado
4. materializar manifesto e emitir log estruturado

## 6. Contratos e invariantes

- entrada canonica: `lote pendente com identificador externo`
- saida canonica: `manifesto consolidado em JSON`
- identificador primario: `batch_id`
- invariantes:
  - um manifesto por lote consolidado
  - nenhum lote concluido volta para fila pendente

## 7. Persistencia

- armazenamento principal: `filesystem`
- localizacao do runtime state: `runtime/`
- estrategia de backup/retencao: `copiar manifestos fechados e reter logs locais por sete dias`
- politicas de migracao: `migracoes manuais e versionadas quando o schema do manifesto mudar`

## 8. Configuracao

- fonte de configuracao: `env`, `arquivo` e `CLI`
- arquivo versionado de exemplo: `config/settings.example.json`
- configuracao host-local ignorada: `config/settings.local.json`

## 9. Observabilidade

- logger central: `sim`
- formato de logs: `json`
- metricas minimas: `errors, throughput e latency`
- healthcheck ou smoke test: `python -m {slug}.main --once`

## 10. Riscos e tradeoffs

- risco tecnico principal: `quebra de sessao ou HTML divergente sem reautenticacao automatica`
- acoplamento consciente: `dependencia do portal autenticado e do schema atual do manifesto`
- parte ainda experimental: `refresh de sessao automatico`

## 11. Decisoes abertas

- promover fila local para backend duravel se o volume crescer
- formalizar schema publicado do manifesto antes de abrir integracao externa
""".replace("{slug}", slug),
        encoding="utf-8",
    )

    (repo / "docs" / "CONTRACTS.md").write_text(
        """# CONTRACTS

## 1. Objetivo

Registrar entradas, saidas, identificadores e assuncoes do worker.

## 2. Entradas canonicas

| Nome | Origem | Formato | Obrigatorio | Observacoes |
| --- | --- | --- | --- | --- |
| `batch_queue.json` | `runtime/inbox` | `file` | sim | `lista de lotes pendentes com batch_id externo` |
| `session.json` | `runtime/browser` | `json` | nao | `cookie persistido para evitar relogin a cada ciclo` |

## 3. Saidas canonicas

| Nome | Destino | Formato | Garantias |
| --- | --- | --- | --- |
| `manifest.json` | `runtime/outbox/<batch_id>/` | `file` | `um manifesto por lote concluido` |
| `worker.log` | `runtime/logs/` | `file` | `log estruturado de bootstrap e consolidacao` |

## 4. Identificadores e chaves

| Conceito | Campo canonico | Observacoes |
| --- | --- | --- |
| `lote remoto` | `batch_id` | `nao assumir equivalencia com study_uid ou job_id externo` |
| `manifesto local` | `manifest_id` | `derivado de batch_id e timestamp de consolidacao` |

## 5. Eventos ou etapas de pipeline

| Etapa | Entrada | Saida | Falhas esperadas |
| --- | --- | --- | --- |
| `coleta` | `batch_queue.json` | `payload bruto do portal` | `sessao expirada ou HTML inconsistente` |
| `consolidacao` | `payload bruto do portal` | `manifest.json` | `campo obrigatorio ausente ou lote duplicado` |

## 6. Assuncoes ainda nao validadas

- o portal continuara expondo os lotes pendentes no mesmo fluxo de navegacao
- o operador aceitara retencao local de manifestos por sete dias

## 7. Quebras de contrato

- `2026-04-21`: schema inicial do manifesto consolidado definido para uso interno
""",
        encoding="utf-8",
    )

    (repo / "docs" / "OPERATIONS.md").write_text(
        f"""# OPERATIONS

## 1. Objetivo

Executar, diagnosticar, reiniciar e recuperar o worker sem contexto implicito.

## 2. Ambientes

| Ambiente | Objetivo | Runtime | Observacoes |
| --- | --- | --- | --- |
| `local` | desenvolvimento | `python3.11` | `host unico do operador` |
| `homolog` | validacao | `python3.11` | `replay controlado de lotes sinteticos` |
| `prod` | operacao | `python3.11` | `execucao residente com logs locais` |

## 3. Como executar

### Boot local

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp config/settings.example.json config/settings.local.json
```

### Boot principal

```bash
python -m {slug}.main --interval 30
```

## 4. Configuracao operacional

- arquivo local: `config/settings.local.json`
- variaveis de ambiente criticas:
  - `{slug.upper()}_CONFIG_FILE`
  - `APP_ENV`
- path de runtime state: `runtime/`
- path de logs: `runtime/logs/`

## 5. Validacao minima

Depois de subir:

```bash
python -m {slug}.main --once
```

Conferir:

- processo principal em execucao
- logs sem erro de bootstrap
- dependencia externa acessivel
- persistencia funcionando

## 6. Logs e diagnostico

- logger principal: `{slug}.infrastructure.logging`
- formato dos logs: `json`
- onde ler logs:
  - `runtime/logs/worker.log`
- sinais de falha comuns:
  - sessao expirada ou cookie ausente
  - lote preso em retry acima do limite previsto

## 7. Restart policy

Ao mudar:

- `domain/` ou `application/`: `restart total do processo residente`
- `infrastructure/`: `restart total e verificacao de sessao`
- `interfaces/`: `restart total do processo residente`
- `config/`: `restart total apos validar arquivo local`
- `docs/` apenas: `nenhum restart`

## 8. Persistencia, backup e limpeza

- armazenamento principal: `filesystem local ou banco definido pelo projeto`
- backup: `copiar runtime/outbox e runtime/logs para area local de retencao`
- retencao: `sete dias para logs e manifestos concluidos`
- limpeza segura: `remover apenas lotes concluidos ja copiados para retencao`

Nunca remova:

- `runtime/browser/session.json` enquanto houver execucao ativa
- `runtime/outbox` sem confirmar backup local

## 9. Incidentes

Checklist minimo:

1. confirmar configuracao carregada
2. confirmar dependencia externa
3. confirmar permissao path de runtime
4. confirmar logs e ultimo erro estruturado
5. confirmar se houve mudanca recente de contrato

## 10. Mudancas que exigem update deste documento

- novo entrypoint
- nova dependencia operacional
- novo path de runtime
- nova regra de restart
- nova rotina de backup ou limpeza
""",
        encoding="utf-8",
    )

    (repo / "config" / "doctor.json").write_text(
        json.dumps(
            {
                "version": 1,
                "ignored_warnings": [],
                "token_alias_groups": [],
            },
            indent=2,
            ensure_ascii=True,
        )
        + "\n",
        encoding="utf-8",
    )


class StarterRegressionTests(unittest.TestCase):
    def test_version_flags(self) -> None:
        scaffold_version = run_cmd([sys.executable, str(SCAFFOLDER), "--version"])
        self.assertIn(KIT_VERSION, scaffold_version.stdout)

        wrapper_version = run_cmd([sys.executable, str(NEWPROJ), "--version"])
        self.assertEqual(wrapper_version.stdout.strip(), f"newproj {KIT_VERSION}")

    def test_install_script_creates_wrapper_link(self) -> None:
        with tempfile.TemporaryDirectory(prefix="starter-install-") as tmp:
            target_bin = Path(tmp) / "bin"
            result = run_cmd(["bash", str(INSTALL_SCRIPT), str(target_bin)])
            self.assertTrue((target_bin / "newproj").exists())
            self.assertIn(KIT_VERSION, result.stdout)
            wrapper_version = run_cmd([str(target_bin / "newproj"), "--version"])
            self.assertEqual(wrapper_version.stdout.strip(), f"newproj {KIT_VERSION}")

    def test_doctor_strict_audit_and_wrapper_flow(self) -> None:
        with tempfile.TemporaryDirectory(prefix="starter-flow-") as tmp:
            repo = Path(tmp) / "FlowRepo"
            run_cmd(
                [
                    sys.executable,
                    str(SCAFFOLDER),
                    str(repo),
                    "--preset",
                    "worker",
                    "--enforce-gate",
                ]
            )

            self.assertTrue((repo / "config" / "doctor.json").exists())
            self.assertTrue((repo / "scripts" / "project_doctor.py").exists())
            self.assertTrue((repo / ".githooks" / "pre-commit").exists())
            self.assertTrue((repo / ".github" / "workflows" / "ci.yml").exists())
            self.assertTrue((repo / "flowrepo" / "main.py").exists())
            self.assertTrue((repo / "requirements.txt").exists())
            self.assertFalse((repo / "pyproject.toml").exists())
            self.assertFalse((repo / "src").exists())

            ci_workflow = (repo / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
            readme_text = (repo / "README.md").read_text(encoding="utf-8")
            self.assertIn("python -m pytest -q", ci_workflow)
            self.assertIn("python3 scripts/check_project_gate.py", ci_workflow)
            self.assertIn("[![CI](", readme_text)
            self.assertIn("![Python]", readme_text)

            logging_config = json.loads((repo / "config" / "logging.example.json").read_text(encoding="utf-8"))
            required_fields = logging_config["formatters"]["json"]["required_fields"]
            self.assertEqual(required_fields, ["ts", "lvl", "svc", "mod", "evt", "msg"])

            write_valid_docs(repo, "FlowRepo", "flowrepo")

            run_cmd([sys.executable, str(repo / "scripts" / "check_project_gate.py")], cwd=repo)

            doctor_warning = run_cmd([sys.executable, str(repo / "scripts" / "project_doctor.py")], cwd=repo)
            self.assertIn("[objective_mismatch]", doctor_warning.stdout)

            strict_failure = run_cmd(
                [sys.executable, str(repo / "scripts" / "project_doctor.py"), "--strict"],
                cwd=repo,
                expected=1,
            )
            self.assertIn("[objective_mismatch]", strict_failure.stderr)

            (repo / "config" / "doctor.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "ignored_warnings": [],
                        "token_alias_groups": [["daemon", "worker"]],
                    },
                    indent=2,
                    ensure_ascii=True,
                )
                + "\n",
                encoding="utf-8",
            )

            run_cmd([sys.executable, str(repo / "scripts" / "project_doctor.py"), "--strict"], cwd=repo)

            worker_run = run_cmd([sys.executable, "-m", "flowrepo.main", "--once"], cwd=repo, expected=1)
            log_payload = json.loads(worker_run.stdout.strip().splitlines()[-1])
            self.assertIn("ts", log_payload)
            self.assertEqual(log_payload["evt"], "worker_cycle")

            audit_ok = run_cmd(
                [sys.executable, str(repo / "scripts" / "project_doctor.py"), "--audit-config"],
                cwd=repo,
            )
            self.assertIn("Alias groups em uso:", audit_ok.stdout)

            (repo / "config" / "doctor.json").write_text(
                json.dumps(
                    {
                        "version": 1,
                        "ignored_warnings": [
                            {
                                "code": "objective_mismatch",
                                "reason": "README usa linguagem operacional e o gate usa linguagem de negocio.",
                            }
                        ],
                        "token_alias_groups": [["daemon", "worker"]],
                    },
                    indent=2,
                    ensure_ascii=True,
                )
                + "\n",
                encoding="utf-8",
            )

            audit_failure = run_cmd(
                [sys.executable, str(repo / "scripts" / "project_doctor.py"), "--audit-config"],
                cwd=repo,
                expected=1,
            )
            self.assertIn("Ignored warnings sem efeito atual:", audit_failure.stderr)

            wrapper_audit_failure = run_cmd(
                [sys.executable, str(NEWPROJ), "doctor", "--audit-config", str(repo)],
                expected=1,
            )
            self.assertIn("Ignored warnings sem efeito atual:", wrapper_audit_failure.stderr)

    def test_node_project_includes_ci_baseline(self) -> None:
        with tempfile.TemporaryDirectory(prefix="starter-node-") as tmp:
            repo = Path(tmp) / "NodeRepo"
            run_cmd(
                [
                    sys.executable,
                    str(SCAFFOLDER),
                    str(repo),
                    "--runtime",
                    "node",
                    "--enforce-gate",
                ]
            )

            workflow = (repo / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
            package_json = json.loads((repo / "package.json").read_text(encoding="utf-8"))
            readme_text = (repo / "README.md").read_text(encoding="utf-8")

            self.assertIn("npm install", workflow)
            self.assertIn("npm test", workflow)
            self.assertIn("python3 scripts/check_project_gate.py", workflow)
            self.assertEqual(package_json["scripts"]["test"], "node --test tests/*.test.mjs")
            self.assertIn("[![CI](", readme_text)
            self.assertIn("![Node]", readme_text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
