# Projeto Existente

Use este fluxo quando um agente receber um pedido como: "Alinhe o projeto atual à estrutura proposta pelo projeto em `<SKIDBLADNIR_PATH>`."

## Objetivo

Elevar um repositório vivo ao padrão Skidbladnir sem fingir maturidade, sem reescrever estrutura por estética e sem substituir comportamento real por documentação aspiracional.

## Regra central

Projeto existente não é greenfield. Primeiro leia o sistema real, depois adapte a baseline do kit.

## Descoberta obrigatória

Antes de editar:

- leia `README.md`, docs existentes e arquivos de configuração
- identifique entrypoints reais
- preserve entrypoints compatíveis; ao criar uma TUI ou GUI Python dedicada, prefira `python -m tui` ou `python -m gui` como launcher público fino em vez de `python -m <slug>.tui`
- identifique runtime principal e toolchain
- preserve o runtime existente, salvo incompatibilidade concreta com plataforma, SDK, operação ou requisitos mensuráveis; preferência de linguagem não justifica migração
- identifique composição ou orquestração central
- identifique contratos canônicos, schemas, modelos, payloads e integrações
- identifique runtime state, logs, cache, banco local, secrets e configuração host-local
- identifique testes, smokes, scripts operacionais e CI existentes
- rode `git status --short`

## Adoção mínima

Crie ou revise:

- `README.md`
- `AGENTS.md`
- `PROJECT_GATE.md`
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/OPERATIONS.md`
- `docs/DECISIONS.md`
- `docs/TASK_TEMPLATE.md` ou registro equivalente de tarefas e passagens de contexto
- `deploy/manifest.json`
- `schema/deploy-manifest.schema.json`
- `config/doctor.json` ou localização equivalente justificada
- scripts de validação que não contrariem o runtime real

## Manifesto em repositório existente

O manifesto deve refletir a operação atual, mesmo que ela seja parcial. Se o deploy ainda for manual, use `deploy.target: "manual"`. Se o projeto for biblioteca sem processo, use `deploy.target: "none"` e explique em `deploy.reason`. Não declare systemd, container ou Kubernetes se o repositório ainda não usa isso.

## O que não fazer

- não reorganizar diretórios só para parecer limpo
- não criar deploy fictício
- não declarar teste ou cobertura que não existe
- não esconder hotspots em linguagem genérica
- não remover docs úteis já existentes sem absorver o conteúdo
- não empurrar toda a governança para `AGENTS.md`
- não trocar linguagem por preferência; nenhuma linguagem é default e uma migração exige benefício concreto, custo de transição e estratégia de retorno

## Validação

Rode o que for viável e honesto:

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --deploy-strict
python3 scripts/project_doctor.py --audit-config
```

Depois rode os testes existentes do repositório. Se uma validação não for viável por dependência externa, toolchain ausente ou ambiente indisponível, registre isso na resposta final com precisão.

## Critério de pronto

A rodada está pronta quando o repositório passa a ter fronteira, operação, contratos e manifesto explícitos, sem contrariar o comportamento real. Dívidas remanescentes devem aparecer como dívidas, não como se já estivessem resolvidas.

## Colaboração e riscos

Siga `docs/agent-collaboration.md`: tarefa independente por branch/worktree ou checkout isolado, responsabilidade por arquivos/módulos e integrador para mudanças concorrentes. Integração rotineira requer checks aprovados, revisão independente e permissões existentes, com nova validação do resultado combinado. Fronteiras sensíveis e risco não esclarecido exigem decisão humana; decisões já concedidas continuam válidas dentro do escopo aprovado.

Siga convenções do runtime e dimensione a arquitetura ao problema. Quatro camadas não são obrigatórias. Registre critérios de contratos, falhas, compatibilidade e escala conforme risco. Validação documental é estrutural; ferramenta ausente ou ambiente indisponível não pode ser contado como teste aprovado. Projetos consumidores não são regenerados automaticamente; consulte o guia de migração 2.0.
