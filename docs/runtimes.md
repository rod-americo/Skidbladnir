# Runtimes

Nenhuma linguagem é default. A disponibilidade de scaffold, a linguagem usada pelo kit e a familiaridade presumida do agente não favorecem uma alternativa. Python executa os validadores documentais; isso não determina a linguagem das aplicações.

## Como decidir

1. Registre as restrições: plataforma, bibliotecas e SDKs obrigatórios, suporte, distribuição, ambiente operacional, equipe responsável pela manutenção e contratos existentes.
2. Compare alternativas viáveis por facilidade de manutenção, verificabilidade, prevenção de regressões, dependências, operação e custo de transição. Tipagem, testes de contratos e ferramentas de diagnóstico contam; quantidade de código ou velocidade de geração por agente, isoladamente, não decidem.
3. Registre no gate a alternativa escolhida, as alternativas consideradas, justificativa, riscos, mitigação e evidências. Declare hipóteses ainda não verificadas e como serão testadas.
4. Defina escala com carga representativa e critérios: latência p95/p99, throughput, concorrência, memória, CPU, tempo de recuperação e custo, conforme o projeto. Informe volume, ambiente, método e limite aceitável. Não invente benchmarks ou metas para justificar preferência.
5. Preserve runtimes existentes adequados. Migração exige benefício concreto, comparação com a melhoria incremental, custo de transição, compatibilidade e estratégia de retorno.

Quando faltarem informações materiais, pergunte sobre manutenção, operação ou requisitos. Não substitua a análise por uma pergunta sobre linguagem favorita. Se as alternativas estiverem empatadas, explicite o empate e obtenha evidência com um experimento pequeno ou uma decisão registrada.

## Alternativas a considerar

| Ecossistema | Fatores que podem justificar a escolha | Custos e verificações |
| --- | --- | --- |
| Java/JVM | bibliotecas maduras, contratos tipados, suporte prolongado, serviços e integrações corporativas | medir inicialização, memória, GC e distribuição; evitar frameworks sem necessidade |
| Rust | controle de recursos, segurança de memória no código seguro, distribuição nativa | considerar custo de manutenção, compilação, interoperabilidade, dependências e experiência efetiva; medir antes de prometer ganhos |
| Go | binário distribuível, concorrência e operação simples | validar contratos, falhas, limites de recursos e bibliotecas do domínio |
| C#/.NET | bibliotecas, plataforma e integrações .NET | avaliar suporte, distribuição e comportamento na plataforma de destino |
| Swift | integração com plataformas Apple ou bibliotecas Swift existentes | verificar plataforma, CI e requisitos de distribuição |
| TypeScript/Node | browser, serviços e bibliotecas do ecossistema, contratos no build | manter modo estrito e validar dados externos em runtime |
| JavaScript/Node | sistema existente adequado ou integração que justifique JavaScript | compensar ausência de tipos estáticos com contratos e testes proporcionais ao risco |
| Python | bibliotecas de dados, automação, ciência e integrações apropriadas ao domínio | executar lint e tipos; medir limites de CPU, memória, concorrência e distribuição |

Esses fatores são possibilidades, não uma classificação de linguagens. Frameworks HTTP, runtimes assíncronos, filas e microsserviços só entram quando o projeto concreto precisar deles. Quatro camadas são uma opção justificada; siga o layout convencional de cada ecossistema e mantenha um núcleo testável.

## Suporte materializado

O [catálogo gerado](runtime-catalog.md) publica versões concretas, presets e comandos a partir de `templates/runtimes/catalog.json`. A CLI gera `python`, `node`, `ts`, `go`, `swift`, `csharp`, `java`, `rust` e `generic`. Java e Rust têm inicialmente apenas `base`. Os presets especializados existentes são Python e exigem `--runtime python` explícito, inclusive `fastapi-service`.

O protocolo admite outros runtimes: declare um identificador estável e a versão concreta no manifesto, adapte templates e provisione seus checks. `generic` é reservado a repositórios sem runtime dominante. `node` e `js` continuam aceitos em manifestos versão 1; a CLI mantém `node` como identificador de geração JavaScript.

## Reprodutibilidade

- Geração não usa rede. Bootstrap e checks de runtime podem baixar toolchains e dependências previamente fixadas.
- Python instala `requirements.txt` com versões transitivas e hashes; `requirements.in` registra dependências diretas. Execute Ruff, mypy e pytest. Use `.venv` na raiz e `python -m <slug>` como entrypoint público; launchers TUI/GUI dedicados podem ser finos em `tui/` e `gui/`.
- Node e TypeScript versionam `package-lock.json` e usam `npm ci`; TypeScript permanece estrito.
- Go fixa versão/toolchain e executa `go vet` e testes com detector de corrida. Sem dependências externas, não há `go.sum`; ao adicioná-las, versione-o.
- Swift segue Swift Package Manager e executa `swift test`. A CI provisiona imagem oficial com versão e digest fixos. Ao adicionar dependências, versione `Package.resolved` e exija resolução congelada.
- .NET fixa SDK em `global.json` e usa `packages.lock.json` com `dotnet restore --locked-mode`.
- Java usa Temurin 25 LTS, Maven Wrapper 3.9.16 com checksum, plugins/dependências fixos e JUnit Jupiter. `./mvnw -B verify` testa e empacota; o JAR executável inclui dependências. Maven não oferece aqui um lockfile transitivo equivalente ao Cargo: revisões de dependências continuam necessárias.
- Rust usa edição 2024, toolchain 1.98.1 e `Cargo.lock` versionado. Execute formatação, Clippy sem warnings, testes e build de release com `--locked`. Código próprio proíbe `unsafe`; isso não garante ausência de `unsafe` em dependências.

Fontes de versões e distribuição: [Python](https://www.python.org/downloads/), [Node](https://nodejs.org/en/about/previous-releases), [Go](https://go.dev/dl/), [Swift](https://www.swift.org/install/), [.NET](https://dotnet.microsoft.com/download/dotnet/10.0), [Temurin](https://adoptium.net/temurin/releases/), [Maven](https://maven.apache.org/download.cgi), [Rust](https://blog.rust-lang.org/).

## Atualização e validação

Uma atualização de toolchain exige revisão de suporte, atualização explícita do catálogo e dos lockfiles afetados, regeneração com `python3 sync_runtime_catalog.py`, execução da matriz e registro na release. Projetos gerados nunca resolvem silenciosamente a versão mais recente da toolchain.

A regressão estrutural funciona sem todas as toolchains. Cada job de runtime provisiona sua ferramenta e executa `python3 run_runtime_checks.py --runtime <id>`. Ferramenta ausente ou versão divergente é falha, nunca aprovação ou skip silencioso. Reporte bloqueios locais separadamente; só declare a matriz aprovada depois de executar todos os jobs exigidos.
