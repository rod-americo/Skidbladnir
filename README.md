# Skidbladnir

Kit pragmático para criar projetos novos e recuperar repositórios existentes com
fronteira explícita, documentação útil, governança mínima e operação
intencional.

## Por que Skidbladnir

`Skidbladnir` era o navio forjado pelos anões na mitologia nórdica: um artefato
de engenharia perfeita, construído com intenção e precisão desde a origem. Essa
ideia reflete a proposta deste repositório: ajudar projetos a nascerem
corretamente, com estrutura, fronteiras e operação explícitas desde o primeiro
dia.

O nome também carrega a noção de movimento sem atrito. Skidbladnir sempre
encontrava vento favorável, e aqui isso funciona como metáfora para boas
decisões iniciais que reduzem improviso, retrabalho e desgaste operacional ao
longo da vida do repositório.

Por fim, Skidbladnir podia ser dobrado, transportado e depois expandido para
cumprir sua função. Essa é a síntese conceitual do projeto: um artefato
compacto, reutilizável e portável, pronto para ser desdobrado em contexto real
sem perder coerência estrutural.

## O que este projeto faz

`Skidbladnir` combina três capacidades complementares:

- scaffolding para projetos novos
- governança mínima para evitar repositórios mal definidos
- retrofit estrutural para projetos que já existem e já estão em funcionamento

Na prática, ele oferece:

- `scaffold_project.py` para gerar projetos novos
- `bin/newproj` como wrapper de uso diário
- templates em `templates/` para `README`, `AGENTS`, `PROJECT_GATE`,
  `ARCHITECTURE`, `CONTRACTS`, `OPERATIONS` e `DECISIONS`
- `check_project_gate.py` para justificar a existência do repositório
- `project_doctor.py` para validar coerência documental e estrutural
- `docs/prompt-repo-existente.md` para recuperar repositórios legados

## Para quem ele existe

- engenheiros aplicados
- mantenedores de workers, integrações e pipelines
- autores de sistemas internos que precisam de operação explícita
- pessoas que já cansaram de repositórios que crescem sem fronteira

## O que ele não é

- um framework universal para qualquer tipo de software
- um template mágico que substitui design de sistema
- uma ferramenta de deploy
- uma garantia de boa arquitetura sem pensamento crítico

## Layout recomendado

O padrão principal do kit é:

- raiz limpa para `README`, `docs`, `config`, `tests`, `scripts` e `runtime`
- módulo ou app principal em `/<slug>/`
- `src/` apenas quando houver necessidade consciente de isolamento de packaging

## Quick start

Instalação do wrapper:

```bash
bash ~/Skidbladnir/install_newproj.sh ~/bin
source ~/.zshrc
newproj --version
```

Gerar um projeto novo:

```bash
newproj ~/MeuWorker --preset worker --include-checklist --enforce-gate
cd ~/MeuWorker
python3 scripts/check_project_gate.py
python3 scripts/project_doctor.py
```

Para repositórios existentes:

- use o prompt em `docs/prompt-repo-existente.md`
- adapte a baseline sem fingir maturidade que o código ainda não sustenta

## Componentes principais

- `scaffold_project.py`: gera novos projetos com baseline estrutural
- `bin/newproj`: wrapper de uso diário
- `templates/`: fonte de verdade dos arquivos gerados
- `install_newproj.sh`: instala ou atualiza o comando `newproj`
- `run_regression_suite.py`: regressão do kit
- `tests/test_starter_regression.py`: suíte principal de regressão

## Quando usar

Use `Skidbladnir` quando você quiser:

- criar um projeto novo com fronteiras explícitas
- evitar documentação implícita desde o começo
- recuperar um repositório vivo sem reescrevê-lo do zero
- estabelecer uma rotina mínima de validação e operação

## Quando não usar

Não use `Skidbladnir` quando:

- o projeto é descartável e de curtíssima vida
- o problema real é que o repositório nem deveria existir
- a equipe precisa de um framework prescritivo completo, e não de um baseline
  pragmático

## Estrutura deste repositório

```text
Skidbladnir/
├── README.md
├── AGENTS.md
├── INSTALL.md
├── ROADMAP.md
├── LICENSE
├── docs/
│   ├── how-to-use.md
│   ├── manual-passo-a-passo.md
│   ├── prompt-repo-existente.md
│   ├── posicionamento.md
│   └── release-checklist.md
├── templates/
├── bin/
├── tests/
└── scaffold_project.py
```

## Estado atual

- foco principal: projetos Python, Node e presets operacionais
- baseline madura para docs, gate e doctor
- suporte a retrofit de repositórios existentes
- espaço claro para evoluir presets, publicação e ergonomia

## Instalação

Consulte [INSTALL.md](INSTALL.md).

## Documentação adicional

- [How To Use](docs/how-to-use.md)
- [Manual Passo a Passo](docs/manual-passo-a-passo.md)
- [Prompt para Repositório Existente](docs/prompt-repo-existente.md)
- [Posicionamento](docs/posicionamento.md)
- [Checklist de Publicação](docs/release-checklist.md)

## Roadmap

Consulte [ROADMAP.md](ROADMAP.md).

## Licença

MIT. Consulte [LICENSE](LICENSE).
