# Projeto Existente

Use este fluxo quando um agente receber um pedido como: "Alinhe o projeto atual à estrutura proposta pelo projeto em `~/Skidbladnir`."

## Objetivo

Elevar um repositório vivo ao padrão Skidbladnir sem fingir maturidade, sem reescrever estrutura por estética e sem substituir comportamento real por documentação aspiracional.

## Regra central

Projeto existente não é greenfield. Primeiro leia o sistema real, depois adapte a baseline do kit.

## Descoberta obrigatória

Antes de editar:

- leia `README.md`, docs existentes e arquivos de configuração
- identifique entrypoints reais
- identifique runtime principal e toolchain
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
