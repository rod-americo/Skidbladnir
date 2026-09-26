# Skidbladnir

Protocolo e kit de templates para agentes iniciarem ou evoluírem repositórios com escopo explícito, escolha fundamentada de runtime, contratos verificáveis e operação documentada. O kit mantém o protocolo, os templates públicos, o scaffolder auxiliar, `newproj` e suas validações.

Skidbladnir era o navio capaz de se desdobrar sem perder a portabilidade. O projeto segue essa ideia: uma base pequena que se adapta ao problema, sem se tornar framework de aplicação ou plataforma de orquestração de agentes.

## Escolha técnica sem linguagem default

A escolha considera manutenção, prevenção de regressões, verificabilidade, bibliotecas, suporte, distribuição, operação e requisitos medidos de recursos e concorrência. Java, Rust, Go, C#, Swift, TypeScript, JavaScript e Python são alternativas, sem preferência pela linguagem usada para implementar o kit. A disponibilidade de scaffold não determina a decisão.

Registre no gate restrições, alternativas viáveis, justificativa, riscos e evidências. Preserve runtimes existentes adequados; migrações exigem benefício concreto e consideração do custo de transição. Quatro camadas são uma opção justificada; os layouts seguem as convenções de cada ecossistema.

Consulte a [política de escolha](docs/runtimes.md) e o [catálogo de versões, presets e comandos](docs/runtime-catalog.md). Outros runtimes podem ser adaptados pelo protocolo e declarados no manifesto. `generic` é reservado a projetos sem runtime dominante.

## Uso principal por agente

Informe o caminho real do clone e o objetivo. Use [novo projeto](prompts/novo-projeto.md) ou [projeto existente](prompts/projeto-existente.md). O agente lê o protocolo, adapta os templates ao sistema real, registra decisões e executa os checks exigidos.

- [Novo projeto](docs/new-project.md): descoberta, gate, templates e primeira validação.
- [Projeto existente](docs/existing-project.md): adoção incremental preservando comportamento e contratos.
- [Colaboração entre agentes](docs/agent-collaboration.md): tarefas isoladas, responsabilidade, revisão e integração.
- [Validação](docs/validation.md): controles estruturais, testes e matriz por runtime.
- [Manifesto operacional](docs/deploy-manifest.md): contrato versão 1, implantação, probes e estado real.

## Bootstrap auxiliar

Após a [instalação](INSTALL.md), consulte as combinações e escolha explicitamente o runtime:

```bash
newproj --list-presets
newproj ./Servico --runtime java --preset base --enforce-gate
newproj ./Ferramenta --runtime rust --preset base --enforce-gate
newproj ./Api --runtime python --preset fastapi-service --enforce-gate
```

Esses são exemplos após decisão técnica, não recomendações universais. Toda geração exige `--runtime`, inclusive presets específicos de Python. A ausência falha antes de criar arquivos. Ajuda, versão, listagem de presets e `newproj doctor` continuam disponíveis. A geração não requer rede; bootstrap e checks baixam dependências fixadas quando necessário.

A versão 2.0.0 altera a CLI de forma incompatível. Leia o [guia de migração](docs/migration-2.0.md). Projetos consumidores não são regenerados automaticamente.

## Colaboração e autonomia

Uma tarefa independente usa branch com worktree ou checkout isolado e responsabilidade explícita por arquivos ou módulos. `docs/TASK_TEMPLATE.md` acompanha projetos gerados para objetivo, critérios de aceite, referência de base, alterações, validações, bloqueios e passagem de contexto.

Um integrador coordena mudanças concorrentes e valida o resultado combinado. Integrações rotineiras podem ser autônomas com checks aprovados, revisão por agente ou pessoa diferente do autor e permissões existentes. Integridade de dados, migrações, dados sensíveis, autenticação/permissões, produção, contratos incompatíveis, enfraquecimento de controles e risco não esclarecido exigem decisão humana. O kit não cria orquestrador nem habilita automerge remoto.

## Operação e qualidade

Todo projeto tem `deploy/manifest.json`. Baselines sem implantação usam `deploy.target: none`. O preset HTTP declara porta e probe real; workers dependem de adaptação antes de implantar. Testes de desenvolvimento, smoke local e saúde operacional são verificações distintas. O validador estático não executa comandos declarados no manifesto.

Os validadores documentais são escritos com a biblioteca padrão de Python e verificam preenchimento, estrutura e coerência declarada. Eles não provam correção, segurança, escalabilidade ou qualidade da decisão arquitetural.

No kit:

```bash
python3 run_regression_suite.py
python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj
python3 sync_runtime_catalog.py --check
python3 run_runtime_checks.py --runtime java
```

A CI separa regressão estrutural de jobs para cada runtime. Cada job provisiona a toolchain fixada e testa projetos temporários; Python inclui todos os presets. Ausência de ferramenta ou versão divergente falha a validação de runtime. O catálogo alimenta geração, documentação e CI, com instalações congeladas onde suportadas, permissões mínimas e actions fixadas por SHA.

## Estrutura do kit

- `templates/`: fonte de verdade dos arquivos gerados, incluindo código, validadores e workflows.
- `templates/runtimes/catalog.json`: versões, comandos, suporte e presets.
- `scaffold_project.py` e `bin/newproj`: bootstrap auxiliar.
- `docs/` e `prompts/`: protocolo público e artefatos operacionais.
- `tests/`, `run_regression_suite.py` e `run_runtime_checks.py`: prevenção de regressões.
- `sync_runtime_catalog.py`: gera a tabela de suporte e a CI do kit.

O README da raiz descreve o produto; o README dos projetos gerados está em `templates/common/README.md`. Consulte também [uso detalhado](docs/how-to-use.md), [manual](docs/manual-passo-a-passo.md), [changelog](CHANGELOG.md) e [licença](LICENSE).
