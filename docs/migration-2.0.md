# Migração para 2.0.0

A mudança incompatível é a exigência de runtime explícito na CLI. Nenhuma linguagem é default. O kit não regenera projetos consumidores nem migra aplicações automaticamente.

## Comandos antigos

| Uso anterior | Uso 2.0 após decisão técnica |
| --- | --- |
| `newproj ./Projeto` | `newproj ./Projeto --runtime <id>` |
| `newproj ./Api --preset fastapi-service` | `newproj ./Api --runtime python --preset fastapi-service` |
| `python3 scaffold_project.py ./Projeto` | `python3 scaffold_project.py ./Projeto --runtime <id>` |

Escolha um ID publicado por `--list-presets`; `<id>` é um marcador, não um argumento literal. A ausência de runtime falha antes de criar diretórios/arquivos. Java e Rust começam com preset `base`; combinações não suportadas falham com orientação. Ajuda, versão, listagem e doctor permanecem disponíveis sem runtime.

## Manifestos e documentos existentes

A versão do manifesto continua sendo 1 e os identificadores anteriores, incluindo `node` e `js`, permanecem válidos. Runtimes adicionais podem ter ID explícito estável e versão concreta; `generic` continua reservado à ausência de runtime dominante.

Declare `healthcheck.http.url` válida quando usar HTTP. Objetos HTTP vazios e declarações operacionais incompletas deixam de passar. Baselines sem implantação agora usam `deploy.target: none`, motivo explícito e nenhum probe inventado. Workers sem probe seguro ficam pendentes de adaptação. Declare somente paths de estado e logs efetivamente usados.

Separe testes de desenvolvimento, smoke e saúde operacional em `docs/OPERATIONS.md`. Um teste ou processamento `--once` não comprova saúde de processo residente. O doctor aceita a organização antiga para leitura, mas os novos templates usam seção própria para saúde.

Rótulos com ou sem acentos e variações de espaços são reconhecidos. O doctor agora extrai de fato o comando de validação em `AGENTS.md` e confronta o runtime do gate com o manifesto, podendo revelar divergências antes ignoradas.

O gate novo tem marcador `<!-- skidbladnir:gate:2 -->` e exige riscos/mitigações, evidências e critérios de escala. Documentos antigos sem marcador continuam reconhecidos pelas regras anteriores. Ao adotar o gate 2, preencha esses campos com decisões reais; texto suficientemente longo não prova qualidade técnica.

## Dependências e toolchains

Os novos scaffolds usam linhas suportadas e versões concretas publicadas no [catálogo](runtime-catalog.md). Isso não é uma ordem de atualizar toolchains de consumidores sem análise. Compare suporte, bibliotecas, contratos e custo de migração antes de incorporar mudanças.

Versione os novos lockfiles aplicáveis e use os comandos congelados: Python com hashes, `npm ci`, Cargo `--locked` e .NET `--locked-mode`. Python passa a executar Ruff e mypy; Swift passa a executar testes; Java usa Maven Wrapper e JUnit; Rust fixa edição, toolchain e proíbe `unsafe` próprio.

Não copie lockfiles sobre aplicações com dependências diferentes. Atualize-os com a ferramenta do ecossistema em uma mudança revisável e repita os checks. Geração continua offline; bootstrap e verificações podem usar rede.

## Colaboração e adoção incremental

Substitua a antiga recomendação de trabalho solo direto em `main` por tarefa independente em branch/worktree ou checkout isolado, com responsabilidade explícita, integrador e contexto durável. Integração rotineira exige checks, revisão independente e permissões existentes; fronteiras sensíveis e risco não esclarecido exigem decisão humana.

Adote `docs/TASK_TEMPLATE.md`, atualize o AGENTS respeitando regras locais e valide o resultado combinado. O kit não altera permissões remotas nem habilita automerge.

Revise cada mudança de consumidor, execute seus testes e controles documentais e registre o que ainda depende de validação no ambiente real. Evite `--force` como mecanismo de atualização: ele sobrescreve arquivos e não faz merge nem migração semântica.
