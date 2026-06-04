# Skidbladnir

[![CI](https://github.com/rod-americo/Skidbladnir/actions/workflows/ci.yml/badge.svg)](https://github.com/rod-americo/Skidbladnir/actions/workflows/ci.yml) ![License](https://img.shields.io/github/license/rod-americo/Skidbladnir) ![Protocol](https://img.shields.io/badge/protocol-agent--first-2f6f4e) ![Runtimes](https://img.shields.io/badge/runtimes-6-blue) ![Deploy Manifest](https://img.shields.io/badge/deploy%20manifest-required-orange)

Protocolo documental e operacional para agentes iniciarem ou alinharem repositórios com fronteira explícita, runtime declarado, contratos auditáveis, operação real e manifesto obrigatório de deploy.

## Por que Skidbladnir

`Skidbladnir` era o navio forjado para ser compacto, transportável e capaz de se desdobrar em contexto real. Essa é a proposta do kit: carregar uma baseline pequena de estrutura, documentação e validação que pode ser aplicada por um agente em projetos novos ou existentes sem transformar o repositório em framework.

## O que este projeto é

- um protocolo para agentes e humanos estruturarem repositórios
- uma coleção de templates, prompts, regras e scripts prontos
- uma baseline multiruntime para Python, JavaScript, TypeScript, Go, Swift e C#
- uma forma de exigir contratos, operação e manifesto de deploy sem automatizar deploy
- um caminho de retrofit para repositórios vivos sem reescrita cosmética

## O que este projeto não é

- uma ferramenta de deploy
- um framework universal de aplicação
- um gerador que substitui leitura do repositório real
- uma garantia de maturidade sem código, operação e validação correspondentes
- uma obrigação de usar CLI para gerar projetos

## Uso principal

O uso principal é por prompt para um agente que tenha acesso ao repositório `~/Skidbladnir`.

Iniciar projeto:

```text
Vou iniciar um projeto com o escopo: <escopo>.
Use ~/Skidbladnir como protocolo base.
Crie a estrutura, manifesto de deploy e validações aplicáveis.
```

Ajustar projeto:

```text
Quero alinhar este repositório ao protocolo em ~/Skidbladnir.
Leia o projeto atual antes de alterar arquivos.
Adapte estrutura, manifesto de deploy e validações sem reescrita cosmética.
```

O agente deve ler os documentos do kit, escolher o runtime, copiar e adaptar os templates, criar ou revisar o manifesto de deploy e rodar as validações possíveis.

## Fluxos oficiais

- [Novo Projeto](docs/new-project.md)
- [Projeto Existente](docs/existing-project.md)
- [Runtimes](docs/runtimes.md)
- [Deploy Manifest](docs/deploy-manifest.md)
- [Validação](docs/validation.md)
- [Prompt Novo Projeto](prompts/novo-projeto.md)
- [Prompt Projeto Existente](prompts/projeto-existente.md)

## Componentes principais

- `templates/common/`: fonte de verdade dos documentos comuns
- `templates/runtimes/`: orientação por runtime
- `templates/scripts/`: scripts de validação copiados para projetos alinhados
- `templates/deploy/`: manifesto operacional copiável
- `schema/`: schema versionado do manifesto de deploy
- `docs/`: protocolo de uso, runtimes, validação e manifesto
- `prompts/`: prompts prontos para agentes
- `scaffold_project.py`: scaffolder auxiliar para bootstrap rápido e regressão
- `bin/newproj`: wrapper de compatibilidade para o scaffolder
- `run_regression_suite.py`: regressão do kit
- `tests/test_starter_regression.py`: suíte principal de regressão

## Manifesto obrigatório

Projetos alinhados ao Skidbladnir devem possuir `deploy/manifest.json`. O manifesto declara comando principal, healthcheck, runtime, portas, environment, secrets esperados, runtime state, logs, restart, backup e rollback.

Se o projeto não tiver deploy, o manifesto continua obrigatório com `deploy.target` igual a `none` e justificativa explícita.

## Runtimes

O protocolo cobre:

- Python
- JavaScript
- TypeScript
- Go
- Swift
- C#
- Genérico, quando não houver runtime dominante

A CLI atual materializa Python, Node, TypeScript, Go, Swift e C#. Os templates e o protocolo continuam sendo o caminho preferencial para adaptação contextual por agentes.

## Validação comum

Projetos alinhados devem, quando os scripts existirem, suportar:

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --deploy-strict
```

Além disso, cada runtime mantém sua validação própria: `python -m pytest -q`, `npm test`, `go test ./...`, `swift build && swift run <Module>` ou `dotnet test`.

## CLI auxiliar

O wrapper continua disponível para bootstrap rápido:

```bash
bash ~/Skidbladnir/install_newproj.sh ~/bin
newproj ~/MeuWorker --preset worker --include-checklist --enforce-gate
```

Esse caminho é auxiliar. Para uso real por agentes, especialmente em projetos existentes, prefira os prompts e o protocolo documental.

## Estrutura deste repositório

```text
Skidbladnir/
├── README.md
├── AGENTS.md
├── INSTALL.md
├── ROADMAP.md
├── docs/
├── prompts/
├── schema/
├── templates/
├── bin/
├── tests/
├── scaffold_project.py
└── run_regression_suite.py
```

## Quando usar

Use quando um projeto precisa nascer ou ser recuperado com fronteira clara, operação explícita, contratos documentados, runtime declarado e manifesto de deploy auditável.

## Quando não usar

Não use quando o projeto é descartável, quando o problema correto é não criar um repositório novo, ou quando a equipe precisa de uma plataforma completa de deploy em vez de um protocolo de governança leve.

## Instalação

Consulte [INSTALL.md](INSTALL.md).

## Roadmap

Consulte [ROADMAP.md](ROADMAP.md).

## Licença

MIT. Consulte [LICENSE](LICENSE).
