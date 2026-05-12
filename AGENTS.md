# AGENTS.md

## Ordem mínima de leitura

1. `README.md`
2. `INSTALL.md`
3. `docs/how-to-use.md`
4. `docs/manual-passo-a-passo.md`
5. `docs/prompt-repo-existente.md`
6. `templates/`

## Escopo deste repositório

- manter o scaffolder, o wrapper `newproj` e os templates públicos
- tratar `templates/` como fonte de verdade dos arquivos gerados
- manter coerência entre produto público, instalação, regressão e templates

## Regras

- documentação humana em `pt-BR`
- identificadores técnicos em `en-US`
- parágrafos em Markdown ficam em linha única; não aplicar hard-wrap manual em 80 colunas
- mudanças em geração exigem revisão de `templates/`
- mudanças em `scaffold_project.py`, `bin/newproj` ou `install_newproj.sh` exigem regressão
- não reintroduzir caminhos locais implícitos como requisito estrutural do kit

## Validação mínima

- `python3 run_regression_suite.py`
- `python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj`
- revisar `git diff`

## Fronteiras importantes

- `README.md` da raiz é documento de produto, não template
- templates de projetos gerados vivem em `templates/`
- `docs/prompt-repo-existente.md` é artefato operacional do kit, não template de repo
