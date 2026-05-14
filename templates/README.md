# {{PROJECT_NAME}}

{{README_BADGES}}

Breve descrição em 1-2 linhas:

- qual problema este repositório resolve
- para quem ele existe
- qual o limite do seu escopo

## Por Que Este Projeto Existe

- {{motivacao_1}}
- {{motivacao_2}}
- {{motivacao_3}}

## O Que Este Repositório É

- {{uma biblioteca, serviço, pipeline, automação, produto interno, etc.}}
- {{a capacidade principal}}
- {{o contexto operacional ou de negócio}}

## O Que Este Repositório Não É

- {{escopo que parece próximo, mas pertence a outro sistema}}
- {{atalhos que você quer proibir desde o início}}
- {{integrações ou comportamentos que não devem nascer aqui}}

## Estado atual

- fase: `{{PROJECT_PHASE}}`
- runtime principal: `{{PRIMARY_RUNTIME}}`
- entrypoints principais:
  - `{{entrypoint_1}}`
  - `{{entrypoint_2}}`
- dependência externa crítica:
  - `{{API / host / banco / fila / worker / PACS / browser / etc}}`

## Baseline arquitetural

Padrão recomendado para projetos novos:

```text
{{PROJECT_NAME}}/
├── README.md
├── AGENTS.md
├── PROJECT_GATE.md
├── CHANGELOG.md
├── .github/
│   └── workflows/
│       └── ci.yml            # baseline de CI para push e pull_request
├── requirements.txt / package.json
├── config/
│   ├── doctor.json
│   ├── settings.example.json
│   └── logging.example.json
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CONTRACTS.md
│   ├── OPERATIONS.md
│   └── DECISIONS.md
{{OPTIONAL_RESEARCH_STRUCTURE}}├── {{PROJECT_SLUG}}/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   ├── interfaces/
│   └── main.py
├── tests/
└── runtime/                  # ignorado no git
```

Regras:

- preserve a separação `domain / application / infrastructure / interfaces`
- mantenha a raiz enxuta e intencional
- use `{{PROJECT_SLUG}}/` na raiz como padrão principal
- use `src/` só quando isolamento de packaging for requisito consciente
- `runtime/`, bancos locais, dumps, sessões e caches não devem ser versionados

## Quick start

### 1. Clonar

```bash
git clone {{REPO_URL}}
cd {{PROJECT_NAME}}
```

### 2. Preparar ambiente

```bash
{{SETUP_COMMANDS}}
```

### 3. Configurar

```bash
cp config/settings.example.json config/settings.local.json
{{OPTIONAL_ENV_SETUP}}
```

### 4. Rodar

```bash
{{RUN_COMMAND}}
```

## Configuração

Princípios:

- segredos e configuração host-local não entram no git
- sempre versione um exemplo: `.env.example`, `settings.example.json`, `config/*.example.json`
- defaults de execução devem ficar centralizados, não espalhados
- deixe claro o que é obrigatório, opcional e ambiente-específico

Tabela mínima:

| Entrada | Tipo | Obrigatório | Origem | Exemplo |
| --- | --- | --- | --- | --- |
| `{{ENV_OR_SETTING_1}}` | `env | arquivo | cli` | sim | `{{host | local | CI}}` | `{{valor_exemplo}}` |
| `{{ENV_OR_SETTING_2}}` | `env | arquivo | cli` | não | `{{host | local | CI}}` | `{{valor_exemplo}}` |

## Contratos e fronteiras

Antes de crescer o projeto, responda:

- qual é a entrada canônica?
- qual é a saída canônica?
- o que é inferido e o que é garantido?
- quais contratos dependem de validação no ambiente real?
- o que pertence a este repositório e o que deve ser delegado?

Registre isso em `docs/CONTRACTS.md` e `docs/ARCHITECTURE.md`.

## Persistência e runtime

- estado persistente deve ficar fora do worktree quando possível
- se precisar ficar localmente, use `runtime/` e ignore tudo no git
- logs operacionais devem ser estruturados e parseáveis
- `print()` não deve ser o mecanismo principal de log operacional
- bancos locais, filas e artefatos derivados precisam de localização clara em `docs/OPERATIONS.md`

## Validação

Checklist mínimo antes de commitar:

- `python3 scripts/check_project_gate.py` executado, se o gate estiver em enforcement
- `python3 scripts/project_doctor.py` executado quando README/docs/contratos já estiverem preenchidos
- testes relevantes executados
- lint ou checagem sintática executada
- `README.md` atualizado se comportamento mudou
- `docs/ARCHITECTURE.md` atualizado se fronteira mudou
- `docs/CONTRACTS.md` atualizado se entrada/saída mudou
- `docs/OPERATIONS.md` atualizado se deploy, restart ou runtime mudou

## Documentação do repositório

- `AGENTS.md`: regras de colaboração para agentes e autores
- `PROJECT_GATE.md`: justificativa de existência e fronteira do repositório
- `scripts/check_project_gate.py`: valida se o gate foi realmente preenchido e se as respostas têm densidade mínima
- `scripts/project_doctor.py`: valida coerência mínima entre gate, README, arquitetura, contratos e operação
- `scripts/project_doctor.py --strict`: transforma warnings semânticos em erro bloqueante
- `scripts/project_doctor.py --audit-config`: audita overrides e aliases de `config/doctor.json`
- `.github/workflows/ci.yml`: baseline de CI alinhada ao runtime e ao preset gerados pelo kit
- `config/doctor.json`: política versionada do doctor para aliases de vocabulário e exceções justificadas
- `docs/ARCHITECTURE.md`: desenho do sistema e fronteiras
- `docs/CONTRACTS.md`: entradas, saídas, invariantes e integrações
- `docs/OPERATIONS.md`: execução, logs, restart, backup e incidentes
- `docs/DECISIONS.md`: decisões arquiteturais com contexto e tradeoff
- `CHANGELOG.md`: histórico mínimo de versão e mudanças relevantes
{{OPTIONAL_RESEARCH_DOCS}}

## Regras operacionais

- commits em `en-US`, preferencialmente `type(scope): summary`
- documentação humana em `pt-BR`, salvo repositórios editoriais ou públicos que exijam outro idioma
- identificadores técnicos em `en-US`
- uma mudança lógica por commit
- se o repositório nascer com gate enforced, instale `.githooks/` com `bash scripts/install_git_hooks.sh`
- não inventar endpoints, campos, contratos ou fluxos sem marcar isso como inferência
- quando houver mudança que exija restart, deixar isso explícito no diff, no `AGENTS.md` e em `docs/OPERATIONS.md`

## Riscos e limites atuais

- risco principal: `{{risco_tecnico_principal}}`
- dependência mais frágil: `{{dependencia_mais_fragil}}`
- maior dívida técnica conhecida: `{{divida_tecnica_principal}}`

## Evolução do Projeto

### Consolidado

- [x] {{consolidado_1}}
- [x] {{consolidado_2}}
- [x] {{consolidado_3}}

### Em andamento

- [ ] {{em_andamento_1}}
- [ ] {{em_andamento_2}}

### Planejado

- [ ] {{passo_1}}
- [ ] {{passo_2}}
- [ ] {{passo_3}}
