# Manual Passo A Passo

## 0. Quando usar este kit

Use este kit quando um projeto novo:

- realmente merece repositório próprio
- precisa nascer com fronteira, contratos e operação explícitos
- não deve crescer por script solto

Se a resposta correta for "isso é um módulo de outro sistema", não gere repo
novo.

## 1. Preparar o comando global

Instale ou atualize o wrapper:

```bash
bash ~/Skidbladnir/install_newproj.sh ~/bin
source ~/.zshrc
newproj --version
```

Se o binário já estiver em `~/Scripts/bin` e esse diretório já estiver no
`PATH`, a instalação pode ser mantida como está.

## 2. Escolher o preset certo

Regra prática:

- `fastapi-service`: API HTTP pequena, repo-owned
- `textual-cli`: cockpit local com TUI
- `playwright-worker`: browser automation com sessão
- `dicom-pipeline`: ingestão e materialização DICOM
- `worker`: loop residente simples
- `cli`: comando local com interface de shell
- `pipeline`: fluxo em etapas orientado a item

Se estiver em dúvida entre dois presets, escolha o mais simples e endureça
depois.

## 3. Gerar o projeto

Exemplo:

```bash
newproj ~/Projetos/MeuWorker --preset worker --include-checklist --enforce-gate
```

O que isso cria:

- docs básicos do repositório
- camadas `domain / application / infrastructure / interfaces`
- pacote ou app principal em `/<slug>/`, preservando a raiz limpa
- `PROJECT_GATE.md`
- `config/doctor.json`
- `scripts/check_project_gate.py`
- `scripts/project_doctor.py`
- hook local se o gate estiver enforced

## 4. Ler antes de codar

Entre no projeto gerado e leia, nesta ordem:

1. `README.md`
2. `AGENTS.md`
3. `PROJECT_GATE.md`
4. `docs/ARCHITECTURE.md`
5. `docs/CONTRACTS.md`
6. `docs/OPERATIONS.md`

Não escreva código de produção antes disso.

## 5. Preencher o gate

Primeiro responda o `PROJECT_GATE.md`.

Objetivo do gate:

- justificar por que o repo existe
- provar por que não deveria ser só um módulo
- delimitar o que não pertence aqui
- explicitar custo operacional

Valide:

```bash
python3 scripts/check_project_gate.py
```

Se falhar:

- remova respostas vagas
- troque frases curtas por justificativas defensáveis
- elimine `TODO`, `preencher`, `talvez`, `não sei`

## 6. Inicializar git e hooks

Se gerou com `--enforce-gate`:

```bash
git init
bash scripts/install_git_hooks.sh
```

Isso faz o pre-commit barrar commits com gate ruim.

## 7. Ajustar os docs estruturais

Preencha o mínimo viável destes arquivos:

- `README.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/OPERATIONS.md`
- `AGENTS.md`

Regras:

- `README.md`: o que o repo é, o que não é, como roda
- `ARCHITECTURE.md`: escopo, fluxo e módulos
- `CONTRACTS.md`: entradas, saídas, identificadores e quebras
- `OPERATIONS.md`: boot, validação, restart, logs e backup
- `AGENTS.md`: política local de colaboração e validação mínima

## 8. Rodar o doctor

Quando os docs já estiverem reais:

```bash
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --strict
python3 scripts/project_doctor.py --audit-config
```

Interpretação:

- `doctor`: valida baseline e mostra warnings semânticos
- `strict`: trata warnings semânticos como erro
- `audit-config`: audita `config/doctor.json`

## 9. Corrigir warnings semânticos do jeito certo

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

## 10. Fazer o bootstrap da stack

Exemplos comuns:

```bash
python3 -m venv .venv
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

## 11. Rodar a validação mínima do projeto

Use o comando registrado no `AGENTS.md` e no `docs/OPERATIONS.md`.

Exemplos:

- worker: `python -m <slug>.main --once`
- cli: `python -m <slug> doctor`
- fastapi-service: `python -m pytest -q`
- dicom-pipeline: `python -m <slug>.main --sample`

## 12. Fazer o primeiro commit relevante

Antes de commitar:

1. `python3 scripts/check_project_gate.py`
2. `python3 scripts/project_doctor.py`
3. validação mínima da stack
4. revisar `git diff`

Se o projeto nasceu com runtime suportado pelo kit, revise também o baseline de
CI em `.github/workflows/ci.yml` antes do primeiro push.

Se a mudança afeta operação:

- declare restart
- atualize `docs/OPERATIONS.md`

## 13. Rotina de crescimento

A cada mudança estrutural:

- atualize `README.md` se o comportamento visível mudou
- atualize `ARCHITECTURE.md` se a fronteira mudou
- atualize `CONTRACTS.md` se entrada ou saída mudou
- atualize `OPERATIONS.md` se boot, restart, logs ou backup mudou
- rode `project_doctor.py --audit-config` quando mexer em `config/doctor.json`

## 14. Atualizar o próprio kit

Quando mexer no scaffolder:

```bash
python3 ~/Skidbladnir/run_regression_suite.py
newproj --version
```

Só considere a alteração pronta se a regressão passar.

## 15. Erros Clássicos A Evitar

- criar repo novo quando era módulo
- deixar `README.md` genérico por semanas
- esconder regra de negócio em script solto
- usar `ignored_warnings` para silenciar desalinhamento real
- esquecer restart policy
- crescer sem `CONTRACTS.md` minimamente confiável
