# AGENTS.md

Este arquivo define regras de colaboração para agentes e autores neste repositório. Ele vale para a raiz inteira, salvo quando um subdiretório tiver um `AGENTS.md` mais específico.

## 1. Ordem mínima de leitura

Antes de fazer mudanças significativas, leia nesta ordem:

1. `README.md`
2. `docs/ARCHITECTURE.md`
3. `docs/CONTRACTS.md`
4. `docs/OPERATIONS.md`
5. `docs/DECISIONS.md`

Se qualquer um desses arquivos ainda não existir, trate isso como débito estrutural e não como permissão para improvisar arquitetura.

## 2. Política de idioma

- Documentação para humanos: `pt-BR`
- Identificadores técnicos: `en-US`
- Mensagens de commit: `en-US`
- Parágrafos em Markdown ficam em linha única; não aplicar hard-wrap manual em 80 colunas

Inclui:

- `README.md`, `docs/`, runbooks, notas operacionais e comentários de contexto
- nomes de módulos, funções, classes, arquivos e variáveis novas
- assuntos de commit no formato `type(scope): summary`

Convenção de nomes:

- código Python, pacotes, módulos, funções, variáveis, tabelas, colunas e identificadores técnicos: `snake_case`
- documentos Markdown, diretórios de documentação/papers, wrappers shell e arquivos de configuração humana: `kebab-case`
- nomes tradicionais da raiz podem permanecer em maiúsculas ou underscore quando forem convenção explícita, como `README.md`, `AGENTS.md`, `CHANGELOG.md` e `PROJECT_GATE.md`

Exceção:

- preserve contratos externos, nomes de campos, env vars e schemas impostos por terceiros
- quando algo for inferido ou adaptado, documente isso explicitamente

## 3. Limite de escopo

Ao iniciar qualquer tarefa, responda primeiro:

- isto pertence a este repositório?
- isto deveria ser uma extensão de um módulo existente, e não um subsistema novo?
- quais módulos e contratos esta mudança afeta?
- existe algum comportamento semelhante que deveria ser extraído em vez de duplicado?

Não use este repositório para:

- empilhar capacidades fora do escopo declarado no `README.md`
- esconder lógica de domínio em scripts soltos
- introduzir comportamento de produção em arquivos experimentais sem promover a estrutura correspondente

## 4. Baseline de arquitetura

Dimensione a arquitetura ao projeto e siga convenções do ecossistema. Um núcleo testável e um entrypoint podem bastar. As quatro responsabilidades abaixo são uma opção, cuja adoção deve ser justificada:

- `domain/`: regras e modelos centrais do problema
- `application/`: casos de uso e orquestração
- `infrastructure/`: IO, banco, API, fila, filesystem, adapters
- `interfaces/`: CLI, API, TUI, GUI, workers, entrypoints externos

Regras:

- não coloque código de produção solto na raiz
- mantenha a raiz enxuta
- preserve imports e dependências na direção da arquitetura
- use `python -m <slug>` como entrypoint público do domínio em projetos Python
- para TUI e GUI dedicadas, prefira launchers top-level finos em `tui/` e `gui/`, executados com `python -m tui` e `python -m gui`, que delegam para `<slug>/interfaces/`; não coloque regra de negócio nesses launchers
- não acople interface diretamente a detalhes de infraestrutura quando houver uma camada de aplicação prevista

Escolha de runtime:

- em repositório existente, preserve o runtime salvo incompatibilidade concreta
- em projeto novo, escolha autonomamente por plataforma, SDK, deploy, distribuição, interoperabilidade e requisitos mensuráveis
- não peça preferência de linguagem quando as restrições forem suficientes
- nenhuma linguagem é default; compare manutenção, prevenção de regressões, verificabilidade, bibliotecas, suporte, distribuição e requisitos medidos de recursos e concorrência
- disponibilidade de scaffold não é critério de preferência; migrações exigem benefício concreto e custo de transição explícito
- registre restrições, alternativas viáveis, justificativa, riscos, mitigação e evidências no `PROJECT_GATE.md`; decisões e experimentos relevantes ficam em `docs/DECISIONS.md`

## 5. Configuração, runtime e logs

- não versione segredos, sessões, dumps, bancos locais, caches ou runtime state
- sempre versione exemplos de configuração
- centralize defaults e parsing de configuração
- ambientes Python ficam em `.venv` na raiz do projeto, criados com `python3 -m venv .venv --prompt $(basename "$PWD")`
- prefira estado host-local fora do worktree; se não for possível, use `runtime/` ignorado no git

Logging:

- logs operacionais devem ser estruturados e parseáveis
- prefira JSON em uma linha ou formato estrito equivalente
- campos mínimos recomendados: `ts`, `lvl`, `svc`, `mod`, `evt`, `msg`
- não use `print()` como mecanismo principal de log operacional
- sempre que possível, use um logger central

## 6. Política de commit e branch

Use uma branch com worktree ou checkout isolado por tarefa independente. Registre objetivo, escopo, responsabilidade por arquivos/módulos, critérios de aceite e commit de referência em `docs/TASK_TEMPLATE.md`. Autores concorrentes não compartilham checkout; coordene sobreposições e contratos compartilhados antes de editar.

Designe um integrador por conjunto de mudanças concorrentes. Ele organiza dependências e valida novamente o resultado combinado. O autor entrega commits pequenos, alterações, resultados de validação, bloqueios e próximo passo; contexto durável deve permitir continuidade sem memória da conversa.

A integração rotineira pode ser autônoma somente com checks exigidos aprovados, revisão independente por outro agente ou pessoa diferente do autor, permissões já configuradas e validação do commit combinado. Registre as revisões exatas avaliadas. Mudanças após os checks ou resolução de conflitos exigem nova validação e revisão do resultado afetado. Não habilite automerge nem altere proteções remotas para contornar uma dependência.

Decisão humana é obrigatória para integridade de dados, migrações, dados sensíveis, autenticação/permissões, produção, contratos incompatíveis ou enfraquecimento de controles. Risco não esclarecido também depende de decisão humana. Apresente impacto, alternativas, evidências e retorno; decisões já concedidas continuam válidas dentro do escopo aprovado. Avance nas partes independentes enquanto uma decisão estiver pendente.

Mensagem de commit:

- idioma: `en-US`
- modo: imperativo
- formato preferencial: `type(scope): summary`
- limite recomendado: 72 caracteres no assunto

Tipos comuns:

- `feat`
- `fix`
- `refactor`
- `docs`
- `test`
- `chore`
- `perf`

Respeite as permissões de push e integração já concedidas ao projeto; trabalho local e criação de commits não autorizam publicação remota por si só.

## 7. Validação obrigatória

Antes de concluir:

- executar os checks exigidos e testes proporcionais de contratos, falhas e compatibilidade
- medir requisitos de escala com carga, ambiente e critérios verificáveis
- separar testes de desenvolvimento, smoke local e saúde operacional; documentação aprovada não comprova comportamento
- revisar `git diff` e `git status`
- confirmar que não há artefatos temporarios sendo versionados
- deixar claro o que foi validado e o que não foi; ferramenta ausente é bloqueio, não aprovação
- validar `deploy/manifest.json` com `python3 scripts/check_deploy_manifest.py` quando houver mudança operacional

Se a mudança afetar execução:

- declarar se exige restart total, parcial ou nenhum restart
- atualizar `docs/OPERATIONS.md` quando a rotina operacional mudar
- atualizar `deploy/manifest.json` quando comando, healthcheck, porta, runtime state, logs, backup, rollback ou restart mudar

## 8. Documentação obrigatória

Atualize junto com o código quando necessário:

- `README.md`: objetivo, escopo, quick start, entrypoints, estado atual
- `docs/ARCHITECTURE.md`: fronteiras, módulos, dependências, runtime
- `docs/CONTRACTS.md`: entradas, saídas, eventos, schemas, invariantes
- `docs/OPERATIONS.md`: execução, logs, restart, incidentes, backup
- `docs/DECISIONS.md`: decisões que alteram a forma como o sistema cresce
- `deploy/manifest.json`: processo, healthcheck, runtime state, logs, restart, backup e rollback

Se a mudança não couber em nenhum desses arquivos, provavelmente ela ainda não foi enquadrada estruturalmente.

Quando o `project_doctor.py` acusar falso positivo semântico:

- registre a exceção em `config/doctor.json`
- use código de warning estável e motivo explícito
- prefira `token_alias_groups` quando o problema for vocabulário equivalente
- prefira `ignored_warnings` quando a divergência for consciente e específica
- não use a configuração para esconder desalinhamento real de escopo
- rode `python3 scripts/project_doctor.py --audit-config` ao revisar overrides antigos

## 9. Regras de segurança técnica

- não inventar endpoints, campos, schemas ou fluxos sem marcar como inferido
- não assumir equivalência entre identificadores diferentes
- não sobrescrever persistência local sem intenção explícita
- não misturar dados reais, sensíveis ou confidenciais com fixtures de exemplo
- não apagar comportamento ou estrutura existente sem justificar o motivo

## 10. Fragilidades clássicas a evitar

- criar um novo repositório para algo que deveria ser módulo
- crescer por script antes de definir contrato
- documentar muito e abstrair pouco
- duplicar config, logger, session, transport ou runtime paths
- deixar comportamento operacional fora de `docs/OPERATIONS.md`

## 11. Extensões específicas do repositório

Preencha este bloco ao iniciar um projeto real:

- domínio crítico: `{{DOMINIO_CRITICO}}`
- dependência externa crítica: `{{DEPENDENCIA_EXTERNA}}`
- dados sensíveis: `{{TIPO_DE_DADO_SENSIVEL}}`
- host principal: `{{HOST_PRINCIPAL}}`
- comando de validação mínima: `{{VALIDACAO_MINIMA}}`
- regra de restart: `{{RESTART_POLICY}}`
- gate check local: `python3 scripts/check_project_gate.py`
- deploy manifest check: `python3 scripts/check_deploy_manifest.py`
- doctor estrutural: `python3 scripts/project_doctor.py`
- doctor estrito: `python3 scripts/project_doctor.py --strict`
- doctor deploy strict: `python3 scripts/project_doctor.py --deploy-strict`
- doctor audit: `python3 scripts/project_doctor.py --audit-config`
- policy do doctor: `config/doctor.json`
