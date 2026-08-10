# Novo Projeto

Use este fluxo quando um agente receber um pedido como: "Vou criar um projeto com o escopo XYZ e quero iniciá-lo já com a estrutura proposta pelo projeto em `~/Skidbladnir`."

## Objetivo

Criar um repositório novo com identidade, fronteira, runtime, contratos, operação e manifesto de deploy explícitos desde a primeira rodada, sem depender de execução manual de `newproj` pelo usuário.

## Ordem de leitura do kit

1. `README.md`
2. `docs/runtimes.md`
3. `docs/deploy-manifest.md`
4. `docs/validation.md`
5. `templates/`

## Descoberta mínima

Antes de criar arquivos, determine:

- escopo real do projeto
- restrições que determinam runtime: plataforma nativa, SDK ou biblioteca dominante, ambiente de deploy, necessidade de binário autônomo, interface, interoperabilidade e requisitos mensuráveis de desempenho, memória ou concorrência
- runtime principal escolhido autonomamente entre `python`, `node`, `ts`, `go`, `swift`, `csharp` ou `generic`
- tipo principal: `base`, `cli`, `worker`, `http-service` ou `pipeline`
- comando principal esperado
- interfaces dedicadas e seus launchers públicos; em Python, prefira `python -m tui` e `python -m gui` a módulos públicos aninhados como `python -m <slug>.tui`
- comando de validação mínima
- runtime state, logs e configuração host-local
- se haverá processo residente, serviço HTTP, job batch ou biblioteca sem deploy

## Escolha autônoma do runtime

Não pergunte ao usuário qual linguagem ele prefere quando as restrições do sistema forem suficientes para decidir. Pergunte apenas pelo contexto ausente que possa alterar materialmente arquitetura ou operação, como plataforma de execução, SDK obrigatório, formato do artefato, integração com ecossistema existente e metas mensuráveis de desempenho.

Use esta ordem de decisão:

1. adote o runtime imposto por plataforma, SDK, integração ou ambiente operacional
2. quando mais de um runtime atender igualmente, escolha o que reduzir dependências, build, distribuição e custo operacional
3. quando não houver fator decisivo, use Python
4. registre em `PROJECT_GATE.md` as restrições determinantes, o runtime escolhido, a principal alternativa considerada e a justificativa operacional
5. registre em `docs/DECISIONS.md` quando a escolha tiver tradeoff relevante ou contrariar o default

Não escolha linguagem por familiaridade presumida do usuário ou do agente. A superfície humana de revisão é comportamento, contratos, testes, operação, riscos e resultados; a implementação continua sujeita às validações do runtime escolhido.

## Entregáveis obrigatórios

- `README.md`
- `AGENTS.md`
- `PROJECT_GATE.md`
- `CHANGELOG.md`
- `START_CHECKLIST.md`, quando a adoção inicial ainda precisa de checklist explícito
- `docs/ARCHITECTURE.md`
- `docs/CONTRACTS.md`
- `docs/OPERATIONS.md`
- `docs/DECISIONS.md`
- `deploy/manifest.json`
- `schema/deploy-manifest.schema.json`
- `config/doctor.json`
- `config/settings.example.*`
- scripts de validação aplicáveis em `scripts/`
- baseline de teste mínima do runtime escolhido

## Uso dos templates

Copie e adapte os templates comuns de `templates/common/` como fonte de verdade editorial. Quando houver template específico de runtime, ele deve prevalecer apenas para arquivos de linguagem, layout de código, CI e comandos de bootstrap; a governança comum continua vindo dos templates comuns.

## Manifesto obrigatório

Todo projeto nasce com `deploy/manifest.json`. Quando o projeto não tiver deploy nem processo residente, declare `deploy.target` como `none` e explique o motivo em `deploy.reason`; não omita o manifesto.

## Validação esperada

Rode, quando os scripts existirem no projeto novo:

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --deploy-strict
```

Depois rode a validação do runtime escolhido, por exemplo `python -m pytest -q`, `npm test`, `go test ./...`, `swift build && swift run <Module>` ou `dotnet test <Project>.sln`.

## Critério de pronto

O projeto está pronto para a primeira rodada quando os documentos descrevem o escopo real, o gate justifica a escolha do runtime, o manifesto descreve como operar ou por que não há deploy, os scripts de validação passam ou têm bloqueio explicado, e o runtime escolhido possui ao menos um smoke test honesto.
