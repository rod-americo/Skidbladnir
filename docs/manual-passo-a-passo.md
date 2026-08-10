# Manual Passo A Passo

## 0. Quando usar este kit

Use este kit quando um projeto novo:

- realmente merece repositório próprio
- precisa nascer com fronteira, contratos e operação explícitos
- não deve crescer por script solto

Se a resposta correta for "isso é um módulo de outro sistema", não gere repo novo.

## 1. Escolher o modo de uso

O uso principal do Skidbladnir é por agente lendo o protocolo em `~/Skidbladnir`.

Use:

- `docs/new-project.md` para projeto novo
- `docs/existing-project.md` para projeto existente
- `docs/runtimes.md` para escolher runtime
- `docs/deploy-manifest.md` para preencher `deploy/manifest.json`
- `docs/validation.md` para validar a rodada

O comando `newproj` continua existindo como bootstrap auxiliar para Python, Node, TypeScript, Go, Swift e C#.

## 2. Preparar o comando global auxiliar

Instale ou atualize o wrapper:

```bash
bash ~/Skidbladnir/install_newproj.sh ~/bin
source ~/.zshrc
newproj --version
```

Se o binário já estiver em `~/Scripts/bin` e esse diretório já estiver no `PATH`, a instalação pode ser mantida como está.

## 3. Escolher o preset certo

Antes do preset, deixe o agente escolher o runtime pelas restrições reais de plataforma, SDK, deploy, distribuição, interoperabilidade e desempenho mensurável. Não pergunte por preferência de linguagem; sem fator decisivo, use Python. Registre a justificativa no `PROJECT_GATE.md`.

Regra prática:

- `fastapi-service`: API HTTP pequena, repo-owned
- `textual-cli`: cockpit local com TUI
- `playwright-worker`: browser automation com sessão
- `dicom-pipeline`: ingestão e materialização DICOM
- `worker`: loop residente simples
- `cli`: comando local com interface de shell
- `pipeline`: fluxo em etapas orientado a item

Se estiver em dúvida entre dois presets, escolha o mais simples e endureça depois.

## 4. Gerar o projeto com o scaffolder auxiliar

Exemplo:

```bash
newproj ~/Projetos/MeuWorker --preset worker --include-checklist --enforce-gate
```

O que isso cria:

- docs básicos do repositório
- camadas `domain / application / infrastructure / interfaces`
- pacote ou app principal em `/<slug>/`, preservando a raiz limpa
- `PROJECT_GATE.md`
- `deploy/manifest.json`
- `config/doctor.json`
- `scripts/check_project_gate.py`
- `scripts/check_deploy_manifest.py`
- `scripts/project_doctor.py`
- hook local se o gate estiver enforced

## 5. Ler antes de codar

Entre no projeto gerado e leia, nesta ordem:

1. `README.md`
2. `AGENTS.md`
3. `PROJECT_GATE.md`
4. `docs/ARCHITECTURE.md`
5. `docs/CONTRACTS.md`
6. `docs/OPERATIONS.md`
7. `deploy/manifest.json`

Não escreva código de produção antes disso.

## 6. Preencher o gate

Primeiro responda o `PROJECT_GATE.md`.

Objetivo do gate:

- justificar por que o repo existe
- provar por que não deveria ser só um módulo
- delimitar o que não pertence aqui
- explicitar custo operacional
- justificar o runtime pelas restrições do sistema, pela alternativa principal considerada e pelo custo operacional

Valide:

```bash
python3 scripts/check_project_gate.py
```

Se falhar:

- remova respostas vagas
- troque frases curtas por justificativas defensáveis
- elimine `TODO`, `preencher`, `talvez`, `não sei`

## 7. Preencher o manifesto de deploy

Revise `deploy/manifest.json` antes do primeiro push relevante.

O manifesto deve declarar:

- comando principal
- healthcheck
- runtime e versão
- portas expostas
- env vars e secrets esperados
- runtime state e logs
- restart, backup e rollback

Valide:

```bash
python3 scripts/check_deploy_manifest.py
```

Se o projeto não tiver deploy, use `deploy.target` como `none` e explique em `deploy.reason`.

## 8. Inicializar git e hooks

Se gerou com `--enforce-gate`:

```bash
git init
bash scripts/install_git_hooks.sh
```

Isso faz o pre-commit barrar commits com gate ruim.

## 9. Ajustar os docs estruturais

Preencha o mínimo viável destes arquivos:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/OPERATIONS.md`
- `AGENTS.md`
- `deploy/manifest.json`

Regras:

- `README.md`: o que o repo é, o que não é, como roda
- `ARCHITECTURE.md`: escopo, fluxo e módulos
- `CONTRACTS.md`: entradas, saídas, identificadores e quebras
- `OPERATIONS.md`: boot, validação, restart, logs e backup
- `AGENTS.md`: política local de colaboração e validação mínima
- `deploy/manifest.json`: processo, healthcheck, runtime state, logs, restart, backup e rollback

## 10. Rodar o doctor

Quando os docs já estiverem reais:

```bash
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --strict
python3 scripts/project_doctor.py --deploy-strict
python3 scripts/project_doctor.py --audit-config
```

Interpretação:

- `doctor`: valida baseline e mostra warnings semânticos
- `strict`: trata warnings semânticos como erro
- `deploy-strict`: valida coerência entre `docs/OPERATIONS.md` e `deploy/manifest.json`
- `audit-config`: audita `config/doctor.json`

## 11. Corrigir warnings semânticos do jeito certo

Se o doctor disser que os documentos usam vocábulos diferentes:

- prefira `token_alias_groups` em `config/doctor.json`
- use `ignored_warnings` só para divergência realmente consciente

Exemplo:

```json
{
  "version": 1,
  "ignored_warnings": [],
  "token_alias_groups": [
    ["worker", "daemon"],
    ["api", "serviço"]
  ]
}
```

Depois rode:

```bash
python3 scripts/project_doctor.py --audit-config
```

Se o audit acusar `ignored_warnings` sem efeito atual, remova o lixo.

## 12. Fazer o bootstrap da stack

Exemplos comuns:

```bash
python3 -m venv .venv --prompt $(basename "$PWD")
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Para `playwright-worker`:

```bash
python -m playwright install chromium
```

Para `node`:

```bash
npm install
```

## 13. Rodar a validação mínima do projeto

Use o comando registrado no `AGENTS.md` e no `docs/OPERATIONS.md`.

Exemplos:

- worker: `python -m <slug> --once`
- cli: `python -m <slug> doctor`
- TUI dedicada: `python -m tui`
- GUI dedicada: `python -m gui`
- fastapi-service: `python -m pytest -q`
- dicom-pipeline: `python -m <slug> --sample`

## 14. Fazer o primeiro commit relevante

Antes de commitar:

1. `python3 scripts/check_project_gate.py`
2. `python3 scripts/check_deploy_manifest.py`
3. `python3 scripts/project_doctor.py`
4. `python3 scripts/project_doctor.py --deploy-strict`
5. validação mínima da stack
6. revisar `git diff`

Se o projeto nasceu com runtime suportado pelo kit, revise também o baseline de CI em `.github/workflows/ci.yml` antes do primeiro push.

Se a mudança afeta operação:

- declare restart
- atualize `docs/OPERATIONS.md`
- atualize `deploy/manifest.json`

## 15. Rotina de crescimento

A cada mudança estrutural:

- atualize `README.md` se o comportamento visível mudou
- atualize `ARCHITECTURE.md` se a fronteira mudou
- atualize `CONTRACTS.md` se entrada ou saída mudou
- atualize `OPERATIONS.md` se boot, restart, logs ou backup mudou
- atualize `deploy/manifest.json` se comando, healthcheck, env, secret, porta, runtime, logs, backup ou rollback mudou
- rode `project_doctor.py --audit-config` quando mexer em `config/doctor.json`

## 16. Atualizar o próprio kit

Quando mexer no scaffolder:

```bash
python3 ~/Skidbladnir/run_regression_suite.py
newproj --version
```

Só considere a alteração pronta se a regressão passar.

## 17. Erros Clássicos A Evitar

- criar repo novo quando era módulo
- deixar `README.md` genérico por semanas
- esconder regra de negócio em script solto
- usar `ignored_warnings` para silenciar desalinhamento real
- esquecer restart policy
- omitir manifesto de deploy porque o deploy ainda é manual
- crescer sem `CONTRACTS.md` minimamente confiável
