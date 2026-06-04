# CHANGELOG

## [Unreleased]

### Changed
- promoção do projeto para `Skidbladnir`
- separação entre `README` público e templates gerados
- adoção de `templates/` como fonte de verdade do scaffolder
- wrapper `newproj` movido para `bin/` dentro do repositório

### Added
- `ROADMAP.md`
- `LICENSE`
- `docs/posicionamento.md`
- `docs/release-checklist.md`
- protocolo para agentes em `docs/new-project.md` e `docs/existing-project.md`
- matriz multilinguagem em `docs/runtimes.md`
- especificação obrigatória de `deploy/manifest.json`
- validação de manifesto com `scripts/check_deploy_manifest.py` nos projetos gerados
- prompts prontos em `prompts/`
- schema formal em `schema/deploy-manifest.schema.json`
- scaffold auxiliar real para projetos Go
- scaffolds auxiliares reais para TypeScript, Swift e C#
- templates comuns reorganizados em `templates/common/`

### Fixed
- normalização de headings no `project_doctor.py` gerado para aceitar acentos e diferenças de capitalização
- fences Markdown inválidas em `INSTALL.md`

### Changed
- scripts gerados passaram a vir de `templates/scripts/`, reduzindo duplicação dentro do scaffolder
