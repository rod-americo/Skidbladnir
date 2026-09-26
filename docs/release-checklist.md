# Checklist de release

## Conteúdo e compatibilidade

- [ ] Conferir VERSION, changelog, guia de migração e comportamento da CLI.
- [ ] Revisar README, docs, prompts e templates no mesmo escopo.
- [ ] Confirmar que geração funciona sem rede e que comandos administrativos permanecem disponíveis.
- [ ] Confirmar compatibilidade de manifestos versão 1 e IDs legados.
- [ ] Revisar decisões de runtime sem linguagem default, operação real e protocolo de colaboração.

## Validação

- [ ] Executar `python3 run_regression_suite.py`.
- [ ] Executar `python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj`.
- [ ] Executar `python3 sync_runtime_catalog.py --check`.
- [ ] Provisionar cada toolchain do catálogo e aprovar todos os runtimes com `run_runtime_checks.py`, incluindo todos os presets Python.
- [ ] Confirmar testes, build, smoke, probe HTTP e rejeição de divergências de lockfile/hashes.
- [ ] Registrar versões concretas validadas e separar bloqueios locais de execução remota da CI.
- [ ] Revisar diff, revisão independente aplicável e resultado combinado.

## Publicação separada

- [ ] Obter autorização para push/publicação quando não existir previamente.
- [ ] Confirmar resultados da CI remota na revisão publicada.
- [ ] Criar tag/release pelo fluxo aprovado do projeto.

Este checklist é um modelo de trabalho, não uma declaração automática de aprovação. Não habilita automerge nem modifica permissões remotas.
