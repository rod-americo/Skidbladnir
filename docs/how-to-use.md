# How To Use

Arquivos complementares do kit:

- `../INSTALL.md`: instalação e update do comando `newproj`
- `manual-passo-a-passo.md`: fluxo operacional completo do zero ao primeiro commit
- `prompt-repo-existente.md`: prompt genérico para recuperar repositórios já em funcionamento
- `../VERSION`: versão atual do kit
- `../run_regression_suite.py`: regressão automatizada do scaffolder

## Fluxo recomendado

1. Gere o projeto com `newproj` ou `scaffold_project.py`.
2. Revise `README.md` e `AGENTS.md` antes de escrever código de produção.
3. Ajuste `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md` e `docs/OPERATIONS.md`
   antes da primeira integração real.
4. Se usar `--include-checklist`, rode `START_CHECKLIST.md` antes do primeiro
   push relevante.

Para repositórios antigos que já existem e não nasceram com o scaffolder, use
`prompt-repo-existente.md` em vez de gerar um projeto novo.

## Layout recomendado

Padrão principal para projetos Python e Node deste kit:

- raiz limpa para `README`, `docs`, `config`, `tests`, `scripts` e `runtime`
- pacote ou app principal direto em `/<slug>/`
- entrypoints por `python -m <slug>...`, `python -m <slug>.main...` ou `node <slug>/main.mjs`

Exemplo:

```text
MeuProjeto/
├── README.md
├── docs/
├── config/
├── tests/
├── runtime/
└── meuprojeto/
```

Use `src/<slug>` só quando o repositório tiver uma necessidade explícita de
isolamento de packaging e isso estiver documentado.

Exemplos:

```bash
newproj --version
newproj ~/NovoProjeto --include-checklist
newproj ~/ApiNova --preset fastapi-service --include-checklist
newproj ~/PainelLocal --preset textual-cli --include-checklist
newproj ~/BrowserWorker --preset playwright-worker --include-checklist
newproj ~/DicomStage --preset dicom-pipeline --include-checklist
newproj ~/ProjetoCritico --preset fastapi-service --include-checklist --enforce-gate
newproj --list-presets
```

## Presets Python

Os presets não-base exigem `--runtime python` implicitamente. O scaffold já
preenche `README.md`, `AGENTS.md` e `docs/OPERATIONS.md` com um comando
principal coerente por preset.

Linha recomendada hoje:

- `fastapi-service`: serviços HTTP pequenos e repo-owned
- `textual-cli`: cockpit local e TUI operacional
- `playwright-worker`: browser automation, login e sessão persistida
- `dicom-pipeline`: staging DICOM, manifesto de estudo e materialização

Presets genéricos ainda existem e continuam úteis:

- `fastapi`
- `cli`
- `worker`
- `pipeline`

Comandos iniciais esperados:

- `fastapi` / `fastapi-service`
  - setup: `python -m pip install -r requirements.txt`
  - run: `python -m <slug>.main`
  - alternativa: `uvicorn <slug>.interfaces.http.app:create_app --factory --reload`
  - smoke test: `python -m pytest -q`
- `cli`
  - setup: `python -m pip install -r requirements.txt`
  - run: `python -m <slug> doctor`
  - smoke test: `python -m <slug> doctor`
- `textual-cli`
  - setup: `python -m pip install -r requirements.txt`
  - run: `python -m <slug> tui`
  - smoke test: `python -m <slug> doctor`
- `worker`
  - setup: `python -m pip install -r requirements.txt`
  - run: `python -m <slug>.main --once`
  - modo residente: `python -m <slug>.main --interval 30`
  - smoke test: `python -m <slug>.main --once`
- `playwright-worker`
  - setup: `python -m pip install -r requirements.txt`
  - bootstrap browser: `python -m playwright install chromium`
  - run inicial: `python -m <slug>.main --once --dry-run`
  - refresh real: `python -m <slug>.main --refresh-session`
  - smoke test: `python -m <slug>.main --once --dry-run`
- `pipeline`
  - setup: `python -m pip install -r requirements.txt`
  - run: `python -m <slug>.main --item-id demo-001`
  - smoke test: `python -m <slug>.main --item-id demo-001`
- `dicom-pipeline`
  - setup: `python -m pip install -r requirements.txt`
  - run inicial: `python -m <slug>.main --sample`
  - run real: `python -m <slug>.main --inbox runtime/inbox --outbox runtime/outbox`
  - smoke test: `python -m <slug>.main --sample`

Fragilidade conhecida:

- `fastapi` não é validado por import puro sem instalar dependências; isso é
  intencional. O baseline assume bootstrap do ambiente antes do primeiro run.
- `playwright-worker` sai com bootstrap de sessão e artefato placeholder, não
  com login real. O primeiro trabalho útil é substituir esse dry-run.
- `dicom-pipeline` sai com manifesto mínimo e sample DICOM sintético. Isso
  resolve baseline técnico, não contrato clínico final.
- `newproj` depende de `~/Scripts/bin` estar no `PATH`; se não estiver, use o
  caminho absoluto do binário ou rode `scaffold_project.py` diretamente.

## Versão e regressão do kit

Comandos úteis:

```bash
python3 scaffold_project.py --version
newproj --version
python3 run_regression_suite.py
```

Use a regressão sempre que mudar:

- `scaffold_project.py`
- `newproj`
- `install_newproj.sh`
- templates base de docs

Projetos Python e Node gerados pelo kit agora também saem com um baseline de
CI em `.github/workflows/ci.yml`.

O objetivo desse workflow é simples:

- instalar dependências
- rodar checagem sintática quando fizer sentido
- executar a suíte de testes do projeto
- validar `PROJECT_GATE.md` quando o projeto nascer com `--enforce-gate`

## Gate Enforced

Se você usar `--enforce-gate`, o projeto sai com:

- `scripts/check_project_gate.py`
- `.githooks/pre-commit`
- `scripts/install_git_hooks.sh`
- `tests/test_project_gate.py` para runtimes Python

Fluxo esperado:

1. gere o projeto com `--enforce-gate`
2. preencha `PROJECT_GATE.md`
3. rode `git init`
4. rode `bash scripts/install_git_hooks.sh`
5. confirme que `python3 scripts/check_project_gate.py` passa

O gate agora falha em 3 casos:

- campos obrigatórios vazios ou com `TODO/preencher`
- respostas vagas como `a definir`, `não sei`, `talvez`, `N/A`
- respostas curtas demais para justificar existência, fronteira e custo

## Project Doctor

Depois que `README.md`, `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md` e
`docs/OPERATIONS.md` estiverem realmente preenchidos, rode:

```bash
python3 scripts/project_doctor.py
newproj doctor .
newproj doctor --strict .
newproj doctor --audit-config .
```

O doctor valida:

- arquivos obrigatórios presentes
- placeholders e `TODO` remanescentes nos docs principais
- coerência entre `README.md` e `docs/OPERATIONS.md` no comando principal
- coerência entre `AGENTS.md` e `docs/OPERATIONS.md` na validação mínima
- preenchimento do `PROJECT_GATE.md`
- warnings com código estável para desalinhamento entre gate, README e arquitetura

Use `--strict` quando quiser tratar esses warnings como erro bloqueante.
Use `--audit-config` para auditar `config/doctor.json`, listar warnings
suprimidos, aliases em uso e exceções sem efeito atual.

Se aparecer falso positivo semântico, ajuste `config/doctor.json` em vez de
afrouxar o texto dos docs. O arquivo é versionado e aceita:

- `ignored_warnings`: exceções conscientes com `code` e `reason`
- `token_alias_groups`: grupos de termos equivalentes para o repositório

Regra prática:

- prefira `token_alias_groups` quando o problema for linguagem equivalente
- use `ignored_warnings` só quando a divergência for consciente e desejada
- rode `--audit-config` periodicamente para remover ignores velhos

Exemplo:

```json
{
  "version": 1,
  "ignored_warnings": [
    {
      "code": "scope_architecture_mismatch",
      "reason": "README descreve a capacidade de negócio e ARCHITECTURE descreve módulos técnicos."
    }
  ],
  "token_alias_groups": [
    ["worker", "daemon"],
    ["api", "serviço"]
  ]
}
```

## O que manter sempre

- escopo explícito
- limites do que NÃO pertence ao repositório
- branch policy
- commit policy
- localização de runtime state
- regra de restart
- validação mínima

## O que adaptar por repositório

- domínio crítico
- linguagem pública do projeto, se não for `pt-BR`
- dependência externa principal
- política de persistência
- comandos reais de setup, run e test
- o conteúdo de `PROJECT_GATE.md`

## O que não fazer

- apagar `AGENTS.md` e tentar compensar com contexto implícito
- deixar `README.md` genérico depois que o projeto ganhar forma
- criar novo repositório sem responder se isso deveria ser um módulo
- introduzir integração externa sem registrar contrato e operação
- editar manualmente dezenas de placeholders quando o scaffolder já consegue
  preencher o baseline por você
