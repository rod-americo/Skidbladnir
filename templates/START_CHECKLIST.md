# Start Checklist

Use este checklist antes do primeiro push de um projeto novo.

## 0. Decisão de existência

- este projeto realmente precisa ser um repositório novo?
- ele não deveria nascer como módulo de um repositório existente?
- o limite de escopo está claro no `README.md`?

## 1. Baseline mínima

- `README.md` criado e preenchido
- `AGENTS.md` criado e ajustado para o domínio
- `PROJECT_GATE.md` preenchido
- `CHANGELOG.md` criado
- `docs/ARCHITECTURE.md` criado
- `docs/CONTRACTS.md` criado
- `docs/OPERATIONS.md` criado
- `docs/DECISIONS.md` criado

## 2. Estrutura

- raiz enxuta e intencional
- camadas `domain / application / infrastructure / interfaces` visíveis
- `tests/` criado
- `config/` criado com exemplos versionados
- `runtime/` definido e ignorado no git, se aplicável

## 3. Configuração e runtime

- segredos não entram no git
- existe `settings.example.*` ou equivalente
- runtime state, bancos locais e sessões estão fora do versionamento
- caminho de logs definido
- entrypoint principal documentado

## 4. Contratos

- entrada canônica definida
- saída canônica definida
- identificadores principais definidos
- inferências e assunções marcadas
- limites com sistemas vizinhos documentados

## 5. Validação

- `python3 scripts/check_project_gate.py` passa sem pendências, respostas vagas ou respostas curtas demais, se o gate estiver em enforcement
- `python3 scripts/project_doctor.py` passa quando README e docs estruturais estiverem prontos
- `config/doctor.json` só foi alterado para exceção real, com motivo explícito
- `python3 scripts/project_doctor.py --audit-config` não acusa ignores velhos
- comando mínimo de teste definido
- comando mínimo de lint ou checagem sintática definido
- comportamento de restart documentado
- critério de smoke test definido

## 6. Disciplina de crescimento

- regra de branch definida
- regra de commit definida
- idioma da documentação definido
- política de logs definida
- política de update de docs definida
- `bash scripts/install_git_hooks.sh` executado após `git init`, se houver enforcement do gate

## 7. Perguntas obrigatórias

Se qualquer resposta for "não sei", o projeto ainda está nascendo sem baseline:

- onde mora a configuração?
- onde mora o estado persistente?
- o que pertence a este repositório?
- o que NÃO pertence a este repositório?
- qual arquivo explica a arquitetura?
- qual arquivo explica a operação?
- qual arquivo explica contratos?
