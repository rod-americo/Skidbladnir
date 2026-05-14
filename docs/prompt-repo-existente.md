# Prompt Para Recuperar Repositório Existente

Use este prompt quando o repositório já existe, já roda, mas ainda não adotou o padrão de governança, documentação e validação do starter kit.

Antes de rodar:

- substitua apenas `<REPO_PATH>` pelo caminho absoluto do repositório
- opcionalmente, ajuste uma ou duas linhas de contexto se o domínio for muito específico
- não reduza o prompt a uma lista curta; o valor aqui está justamente em forçar leitura, fronteira, honestidade e baseline operacional

---

```text
Você está trabalhando no repositório <REPO_PATH>.

Objetivo: Elevar este repositório existente ao nível estrutural, documental e operacional do kit Skidbladnir, sem descaracterizar o sistema real que já existe e sem fingir maturidade que o código ainda não sustenta.

Contexto:
- Este não é um projeto novo; ele já existe, já possui código e pode ter usuários, runtime, integrações e worktree suja.
- O trabalho aqui é de recuperação estrutural, não de reescrita cosmética.
- O repositório deve sair desta rodada mais governado, mais legível, mais auditável e mais defensável tecnicamente.

Restrições:
- Trabalhe apenas em <REPO_PATH>.
- Preserve o que o repositório já é; não o reinterprete como outro tipo de sistema.
- Não reverta alterações do usuário no worktree.
- Não invente readiness operacional.
- Não faça refactor massivo de diretórios só para parecer limpo.
- Preserve raiz limpa; se houver espaço para organizar melhor a estrutura, prefira o módulo ou app principal em `/<slug>/` em vez de `src/<slug>`, salvo quando `src/` já for requisito consciente do repositório.
- Não crie contratos, testes ou docs que contradigam o comportamento real do código.
- Documentação humana em pt-BR.
- Identificadores técnicos em en-US.
- Parágrafos Markdown em linha única, sem hard-wrap manual em 80 colunas.

Fonte de verdade para baseline:
- `<SKIDBLADNIR_PATH>/templates/README.md`
- `<SKIDBLADNIR_PATH>/templates/AGENTS.md`
- `<SKIDBLADNIR_PATH>/templates/PROJECT_GATE.md`
- `<SKIDBLADNIR_PATH>/templates/START_CHECKLIST.md`
- `<SKIDBLADNIR_PATH>/templates/docs/ARCHITECTURE.md`
- `<SKIDBLADNIR_PATH>/templates/docs/CONTRACTS.md`
- `<SKIDBLADNIR_PATH>/templates/docs/OPERATIONS.md`
- `<SKIDBLADNIR_PATH>/templates/docs/DECISIONS.md`
- scripts e policy de gate/doctor do starter

Tarefa principal: Fazer uma rodada completa de recuperação estrutural do repositório, adotando a baseline do starter kit de forma adaptada ao sistema real, sem maquiagem e sem overengineering.

Fase 0: descoberta obrigatória Antes de editar qualquer arquivo, faça uma leitura real do repositório e responda implicitamente por meio das mudanças:

1. O que este repositório é hoje?
2. O que ele não é?
3. Qual o entrypoint principal?
4. Onde está a orquestração central?
5. Quais são os contratos canonicamente relevantes?
6. Onde o runtime local ou remoto realmente vive?
7. Quais são os hotspots?
8. O que está operacional, o que está parcial e o que é placeholder?

A descoberta mínima deve cobrir:
- README e docs existentes
- entrypoints principais
- módulo central de orquestração
- modelos e contratos
- runtime/config/logging
- testes existentes, se houver
- scripts operacionais/smokes existentes, se houver
- git status, apenas para não destruir trabalho local

Entregáveis obrigatórios:

1. Revisar ou criar README.md
- Deixar claro o que o repositório é e o que não é.
- Registrar entrypoints reais.
- Explicitar fronteira do domínio.
- Explicitar maturidade real dos componentes principais.
- Trocar linguagem genérica por escopo defensável.

2. Revisar ou criar AGENTS.md
- Ordem mínima de leitura.
- Regras de camada.
- Regras de documentação.
- Validação mínima.
- Hotspots conhecidos.
- Restrições para não piorar a arquitetura.

3. Adicionar ou revisar a baseline documental do starter
- PROJECT_GATE.md
- CHANGELOG.md
- START_CHECKLIST.md
- docs/ARCHITECTURE.md
- docs/CONTRACTS.md
- docs/OPERATIONS.md
- docs/DECISIONS.md

4. Adicionar ou revisar a baseline operacional do starter
- config/doctor.json ou governance/doctor.json, conforme fizer sentido para o repo
- scripts/check_project_gate.py
- scripts/project_doctor.py
- se fizer sentido, .githooks/pre-commit
- se fizer sentido, scripts/install_git_hooks.sh

5. Integrar docs existentes em vez de duplicar
- Se o repositório já tiver docs úteis, absorva o que presta.
- Não duplique runbook em dois lugares sem motivo.
- Se houver docs de módulos, providers ou integrações, conecte-os com a nova baseline estrutural.

6. Materializar a arquitetura real do sistema
- Composition root, se existir.
- Fluxo principal.
- Camadas reais ou módulos reais.
- Layout real do código, preservando raiz limpa e evitando espalhar produção na top-level fora do módulo principal.
- Contratos centrais.
- Runtime state, persistência, logs e paths operacionais.
- Hotspots e dívidas técnicas conhecidas.

7. Materializar a operação real
- setup real
- run real
- test real
- smoke real
- restart real
- troubleshooting real
- dependências externas reais

8. Preparar o repositório para evolução segura
- Ajustar .gitignore se necessário para runtime mutável.
- Criar diretórios mínimos coerentes apenas se fizerem falta de verdade.
- Adicionar validação automatizada mínima honesta.
- Se o repo não tiver teste útil, não finja cobertura: documente isso.

O que eu espero de cada documento:

- README.md: identidade, escopo, não-escopo, comandos reais e visão geral curta
- AGENTS.md: protocolo de colaboração, leitura, validação e guardrails
- PROJECT_GATE.md: por que este repo existe, por que não deveria ser apenas módulo e quais fronteiras impedem escopo infinito
- ARCHITECTURE.md: mapa real do sistema, fluxo principal, hotspots e fronteiras
- CONTRACTS.md: modelos, entradas, saídas, invariantes, identificadores e integrações
- OPERATIONS.md: boot, env, runtime, logs, restart, troubleshooting, smoke e operação crítica
- DECISIONS.md: decisões já tomadas, tradeoffs e alternativas rejeitadas
- START_CHECKLIST.md: o que já está feito, o que ainda falta e o que não deve acontecer na próxima rodada

Pontos críticos:
- Não tratar repositório existente como projeto greenfield.
- Não esconder hotspots atuais.
- Não transformar docs em wishful thinking.
- Não abrir frentes que não são caminho crítico agora.
- Não empurrar toda a complexidade para AGENTS.md.
- Não declarar "escalável", "produto" ou "pronto" sem lastro no código e na operação.

Decisões de adaptação que você deve tomar com critério:
- Se o repositório deve manter o layout atual ou convergir para `/<slug>/` como módulo ou app principal
- Se o repo usa `config/doctor.json` ou `governance/doctor.json`
- Se vale ligar gate enforcement agora ou apenas preparar a base
- Se o repo comporta hook local sem atrapalhar a rotina
- Se existe espaço para teste novo ou se a rodada deve focar em documentação e guardrails

Validação mínima obrigatória:
- checagem sintática dos scripts Python novos, se houver
- scripts/check_project_gate.py passando, se existir
- scripts/project_doctor.py passando, ou explicação precisa do bloqueio
- scripts/project_doctor.py --audit-config passando, ou explicação precisa do bloqueio
- testes existentes executados quando forem relevantes e viáveis
- smoke real quando a mudança tocar operação crítica e houver comando para isso
- revisão de consistência entre README, AGENTS, ARCHITECTURE, CONTRACTS, OPERATIONS, DECISIONS e START_CHECKLIST

Formato esperado da resposta final:
- resumo curto do que foi mudado
- arquivos criados e alterados
- validações executadas
- pendências reais
- avaliação honesta do que ainda continua fraco no repositório mesmo depois desta rodada

Trabalhe de forma autônoma até deixar o repositório claramente mais próximo do padrão do starter, sem maquiar limitações reais e sem destruir a história local do projeto.
```

---

## Quando usar este prompt

Use para repositórios que:

- já existem e já rodam
- nasceram antes do scaffold
- acumulam valor real, mas ainda sem fronteira/documentação/guardrails
- precisam de recuperação estrutural sem reescrita total

## Quando não usar

- projeto greenfield: use o scaffolder normal
- repositório descartável ou experimental de curtíssima vida
- caso em que o problema real seja "este repo não deveria existir"

## Regra prática

Se o repositório estiver vivo, com runtime, usuários ou integrações reais, a primeira rodada deve endurecer governança, docs, contratos e operação. Não comece por refactor cosmético.
