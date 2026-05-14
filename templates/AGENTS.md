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
- esta mudança afeta domínio, aplicação, infraestrutura ou interface?
- existe algum comportamento semelhante que deveria ser extraído em vez de duplicado?

Não use este repositório para:

- empilhar capacidades fora do escopo declarado no `README.md`
- esconder lógica de domínio em scripts soltos
- introduzir comportamento de produção em arquivos experimentais sem promover a estrutura correspondente

## 4. Baseline de arquitetura

Prefira a seguinte separação:

- `domain/`: regras e modelos centrais do problema
- `application/`: casos de uso e orquestração
- `infrastructure/`: IO, banco, API, fila, filesystem, adapters
- `interfaces/`: CLI, API, TUI, GUI, workers, entrypoints externos

Regras:

- não coloque código de produção solto na raiz
- mantenha a raiz enxuta
- preserve imports e dependências na direção da arquitetura
- use `python -m <slug>` como entrypoint público em projetos Python; subcomandos como `gui`, `tui` e `doctor` vivem abaixo desse comando
- não acople interface diretamente a detalhes de infraestrutura quando houver uma camada de aplicação prevista

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

Workflow padrão para repositório solo:

- trabalhar diretamente em `main`
- não criar branches auxiliares sem necessidade explícita
- manter um commit por mudança lógica
- preferir commits curtos, intencionais e fáceis de reverter
- fazer push só depois de revisar diff, validação e impacto operacional

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

Se este repositório deixar de ser solo ou passar a exigir branches protegidas, atualize este arquivo e o `README.md` no mesmo commit.

## 7. Validação obrigatória

Antes de concluir:

- executar a validação mais relevante para os arquivos alterados
- revisar `git diff` e `git status`
- confirmar que não há artefatos temporarios sendo versionados
- deixar claro o que foi validado e o que não foi

Se a mudança afetar execução:

- declarar se exige restart total, parcial ou nenhum restart
- atualizar `docs/OPERATIONS.md` quando a rotina operacional mudar

## 8. Documentação obrigatória

Atualize junto com o código quando necessário:

- `README.md`: objetivo, escopo, quick start, entrypoints, estado atual
- `docs/ARCHITECTURE.md`: fronteiras, módulos, dependências, runtime
- `docs/CONTRACTS.md`: entradas, saídas, eventos, schemas, invariantes
- `docs/OPERATIONS.md`: execução, logs, restart, incidentes, backup
- `docs/DECISIONS.md`: decisões que alteram a forma como o sistema cresce

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
- doctor estrutural: `python3 scripts/project_doctor.py`
- doctor estrito: `python3 scripts/project_doctor.py --strict`
- doctor audit: `python3 scripts/project_doctor.py --audit-config`
- policy do doctor: `config/doctor.json`
