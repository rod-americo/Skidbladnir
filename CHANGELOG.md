# CHANGELOG

## [2.0.0] — 2026-09-26

### Breaking

- geração exige `--runtime` explícito, inclusive presets Python; ausência falha antes de criar arquivos. Ajuda, versão, listagem e doctor são preservados.
- nenhuma linguagem é default; escolha exige restrições, alternativas, riscos e evidências. Consumidores não são regenerados automaticamente; consulte `docs/migration-2.0.md`.

### Added

- scaffolds Java com Temurin 25, Maven Wrapper, JUnit e JAR executável; Rust com edição 2024, toolchain fixa, lockfile, Clippy e núcleo testável sem `unsafe` próprio.
- protocolo de tarefas isoladas, integrador, revisão independente, validação combinada e decisão humana em fronteiras sensíveis; template de tarefa e passagem de contexto.
- catálogo central de versões, presets e comandos, documentação/CI derivadas e matriz real por runtime.
- Ruff e mypy nos projetos Python, testes Swift, instalações congeladas, permissões mínimas e actions por SHA.

### Fixed

- campos acentuados do gate, normalização de espaços, extração do comando no doctor e coerência de runtime declarado.
- HTTP exige URL válida; validadores não executam comandos operacionais. Manifestos versão 1 e IDs anteriores continuam aceitos.
- baselines sem implantação usam `deploy.target: none`; testes, smoke e probes ficam separados; estado/logs refletem o código.
- código dos presets Python passa a viver em templates, com tipos e lint verificados; arquitetura em quatro camadas deixa de ser obrigatória.
- CI do kit e dos projetos Java usa o seletor SemVer do Adoptium para provisionar a release exata, preservando a versão Java original no manifesto e nos checks.

### Validation

- matriz local: Python 3.14.6 (oito presets), Node/TypeScript 24.21.0, Go 1.27.1, Swift 6.4.0, .NET SDK 10.0.401, Temurin 25.0.4.1+1/Maven 3.9.16 e Rust 1.98.1.
- regressão estrutural, checks sintáticos, builds, testes, smoke, probe HTTP real e rejeição de divergências de lockfile/hashes. A execução remota da CI exige publicação separada; não é inferida desses resultados locais.

## [1.0.0] — histórico anterior

### Changed
- promoção do projeto para `Skidbladnir`
- separação entre `README` público e templates gerados
- adoção de `templates/` como fonte de verdade do scaffolder
- wrapper `newproj` movido para `bin/` dentro do repositório
- preferência por launchers Python top-level `python -m tui` e `python -m gui` para interfaces dedicadas; o preset `textual-cli` agora gera `tui/__main__.py`
- escolha autônoma do runtime por restrições técnicas e operacionais, com Python como default e justificativa obrigatória no `PROJECT_GATE.md`

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
