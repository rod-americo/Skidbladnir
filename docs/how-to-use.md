# Como usar

O uso principal é um agente lendo o clone do kit no caminho informado pelo usuário. Use os fluxos de [novo projeto](new-project.md) ou [projeto existente](existing-project.md) e a [política de runtime](runtimes.md). `newproj` é opcional e auxilia o bootstrap; não existe linguagem default.

## CLI

```bash
newproj --help
newproj --version
newproj --list-presets
newproj ./Servico --runtime java --preset base --enforce-gate
newproj ./Utilitario --runtime rust --preset base --enforce-gate
newproj ./Api --runtime python --preset fastapi-service --include-checklist
newproj ./Pesquisa --runtime go --include-papers
```

Toda geração exige `--runtime`, mesmo quando o preset é exclusivo de Python. Runtimes, versões concretas e comandos ficam no [catálogo](runtime-catalog.md). `--force` permite sobrescrever arquivos no destino: não use para atualizar um projeto existente sem revisão do diff. O kit não faz migrações automáticas de consumidores.

## Presets especializados

Os seguintes presets exigem `--runtime python` explícito: `fastapi` (alias `fastapi-service`), `cli`, `textual-cli`, `worker`, `playwright-worker`, `pipeline` e `dicom-pipeline`. Todos os runtimes da CLI oferecem `base`; Java e Rust inicialmente só oferecem esse preset. Presets não representam maturidade de produção.

O entrypoint Python é `python -m <slug>`; o preset Textual expõe `python -m tui`, um launcher fino para a implementação no pacote. Playwright inicia em dry-run; instalação do browser (`python -m playwright install chromium`), login e prova de sessão válida são adaptações explícitas posteriores. DICOM inclui somente uma amostra sintética; processamento de dados reais exige decisão e controles apropriados ao projeto.

## Ambiente e dependências

Siga os comandos exatos do README gerado e do catálogo. Python usa `.venv` na raiz, requisitos com hashes, Ruff, mypy e pytest. Node/TypeScript usam `npm ci`. Java usa `./mvnw -B verify`; Rust usa `--locked`; .NET usa restauração com lockfile. Geração é offline, bootstrap pode usar rede.

Exemplos de configuração são públicos; segredos, sessões, bancos, caches e outros estados locais não entram no Git. Swift e C# fornecem um exemplo de configuração para adaptação; seus baselines ainda não carregam esse arquivo. Registre somente entradas consumidas pelo código.

## Gate, operação e doctor

Preencha o gate com o problema real, fronteiras, escolha de runtime, alternativas, riscos, evidências e critérios mensuráveis de escala. O marcador do gate 2 amplia os campos exigidos; documentos antigos continuam reconhecidos com ou sem acentos. O gate verifica estrutura, não a qualidade da decisão.

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --strict
python3 scripts/project_doctor.py --deploy-strict
python3 scripts/project_doctor.py --audit-config
```

O doctor compara declarações em gate, README, arquitetura, contratos e operação. `--strict` transforma warnings de coerência textual em falhas; `--deploy-strict` também confronta processo e saúde declarados; `--audit-config` revisa exceções e aliases. O wrapper preserva `newproj doctor [opções] <diretório>`.

Para vocabulário equivalente, use `token_alias_groups` em `config/doctor.json`. Para uma divergência consciente, use `ignored_warnings` com código estável e motivo explícito. Não esconda desalinhamento real; audite exceções antigas com `--audit-config`.

Com `--enforce-gate`, são gerados hook local, step de CI e teste Python quando aplicável. Após `git init`, instale o hook com `bash scripts/install_git_hooks.sh`. O hook é um controle local complementar; revisão independente e CI continuam necessárias.

## Colaboração e evolução

Use `docs/TASK_TEMPLATE.md` e o [protocolo de colaboração](agent-collaboration.md). Isole tarefas concorrentes, delimite responsabilidades e designe integrador. O resultado combinado precisa de checks e revisão independente. Mudanças em fronteiras sensíveis ou risco não esclarecido dependem de decisão humana, respeitando decisões já concedidas no mesmo escopo.

Atualize documentação, manifesto e contratos junto do comportamento. Distinga testes, smoke e probe operacional. O estado inicial sem implantação é `deploy.target: none`; o preset HTTP configura um exemplo local, não uma publicação automática. Use o [guia de migração 2.0](migration-2.0.md) antes de adaptar comandos ou incorporar novos templates a projetos existentes.
