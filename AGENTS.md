# AGENTS.md

## Ordem mínima de leitura

1. `README.md`
2. `docs/new-project.md`
3. `docs/existing-project.md`
4. `docs/runtimes.md`
5. `docs/deploy-manifest.md`
6. `docs/validation.md`
7. `INSTALL.md`
8. `docs/how-to-use.md`
9. `docs/manual-passo-a-passo.md`
10. `docs/prompt-repo-existente.md`
11. `templates/`

## Escopo deste repositório

- manter o protocolo para agentes, o scaffolder auxiliar, o wrapper `newproj` e os templates públicos
- tratar `templates/` como fonte de verdade dos arquivos gerados
- manter coerência entre produto público, prompts, documentação, instalação, regressão e templates

## Regras

- documentação humana em `pt-BR`
- identificadores técnicos em `en-US`
- parágrafos em Markdown ficam em linha única; não aplicar hard-wrap manual em 80 colunas
- ambientes Python ficam em `.venv` na raiz do projeto, criados com `python3 -m venv .venv --prompt $(basename "$PWD")`
- entrypoint público de projeto Python gerado é `python -m <slug>`; não documentar `python -m <slug>.main` como caminho primário
- mudanças em geração exigem revisão de `templates/`
- mudanças em `scaffold_project.py`, `bin/newproj` ou `install_newproj.sh` exigem regressão
- mudanças em protocolo exigem revisão de `README.md`, `docs/`, `prompts/` e `templates/`
- não reintroduzir caminhos locais implícitos como requisito estrutural do kit

## Validação mínima

- `python3 run_regression_suite.py`
- `python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj`
- revisar `git diff`

## Fronteiras importantes

- `README.md` da raiz é documento de produto, não template
- templates de projetos gerados vivem em `templates/`
- `docs/prompt-repo-existente.md` é artefato operacional do kit, não template de repo
- `newproj` é compatibilidade e bootstrap auxiliar; o uso principal do kit é por agente lendo o protocolo
