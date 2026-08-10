# Runtimes

Este documento define a matriz multilinguagem do Skidbladnir para agentes. A CLI atual materializa Python, Node, TypeScript, Go, Swift e C#; agentes devem usar esta matriz como referência e adaptar os templates ao contexto real.

## Política de escolha

A linguagem é uma decisão técnica e operacional do agente, não uma preferência que o usuário precise fornecer. Antes de escolher, determine plataforma, SDKs obrigatórios, ambiente de deploy, formato de distribuição, integrações existentes e requisitos mensuráveis de desempenho, memória ou concorrência.

Ordem de decisão:

1. Em repositório existente, preserve o runtime atual, salvo incompatibilidade concreta.
2. Em projeto novo, use o runtime imposto por plataforma, SDK, integração ou ambiente operacional.
3. Entre opções equivalentes, prefira a que reduza dependências, build, distribuição e custo operacional.
4. Sem fator decisivo, use Python.
5. Registre a decisão no `PROJECT_GATE.md`; use `docs/DECISIONS.md` quando houver tradeoff relevante ou desvio do default.

Não pergunte “qual linguagem você prefere?” quando as restrições já permitirem decidir. Se faltar contexto material, pergunte sobre o sistema: onde roda, qual SDK precisa usar, qual artefato deve entregar, com que ecossistema precisa interoperar e quais limites mensuráveis deve cumprir.

## Heurística por contexto

| Contexto dominante | Escolha inicial | Motivo |
| --- | --- | --- |
| Automação, dados, IA, integrações ou ausência de restrição dominante | Python | menor atrito para bootstrap e ecossistema amplo |
| Browser, frontend ou ecossistema Node com contrato tipado | TypeScript | integração direta com a plataforma e tipos no build |
| Base JavaScript existente sem benefício material de migração | JavaScript | preservação do sistema real e menor churn |
| Binário autônomo, serviço concorrente ou operação enxuta | Go | distribuição simples e runtime operacional pequeno |
| Aplicação ou integração nativa Apple | Swift | acesso direto à plataforma e toolchain nativa |
| Ecossistema .NET, Windows ou SDK corporativo dominante | C# | compatibilidade direta com plataforma e bibliotecas |
| Repositório sem runtime dominante | Genérico | evita inventar uma linguagem central inexistente |

Esta tabela orienta, mas não substitui evidência. Não use desempenho, escalabilidade ou portabilidade como justificativa abstrata sem requisito observável.

## Runtimes suportados pelo protocolo

| Runtime | Identificador | Layout recomendado | Setup | Run | Test |
| --- | --- | --- | --- | --- | --- |
| Python | `python` | pacote em `/<slug>/` | `python3 -m venv .venv --prompt $(basename "$PWD")` e `python -m pip install -r requirements.txt` | `python -m <slug>` | `python -m pytest -q` |
| JavaScript | `node` | app em `/<slug>/` com `.mjs` | `npm install` | `npm start` | `npm test` |
| TypeScript | `ts` | app em `src/` quando build/transpile exigir | `npm install` | `npm start` | `npm test` |
| Go | `go` | `cmd/<slug>/` para binário e pacote interno quando necessário | `go mod download` | `go run ./cmd/<slug>` | `go test ./...` |
| Swift | `swift` | `Sources/<Module>/` e `Sources/<Module>Core/` | `swift package resolve` | `swift run <Module>` | `swift build && swift run <Module>` |
| C# | `csharp` | `src/<Project>/` e `tests/<Project>.Tests/` | `dotnet restore <Project>.sln` | `dotnet run --project src/<Project>/<Project>.csproj` | `dotnet test <Project>.sln` |
| Genérico | `generic` | documentação, scripts e manifesto sem runtime dominante | definido pelo projeto | definido pelo projeto | definido pelo projeto |

## Presets comuns

- `base`: documentação, manifesto, configuração e smoke mínimo
- `cli`: comando local com interface explícita
- `worker`: processo residente, loop, retry, restart e runtime state
- `http-service`: serviço HTTP pequeno com healthcheck
- `pipeline`: fluxo em etapas com entrada, saída e materialização

## Regras por runtime

- Python usa `python -m <slug>` como entrypoint público primário do domínio.
- TUI e GUI Python dedicadas preferem launchers top-level `python -m tui` e `python -m gui`; os pacotes `tui/` e `gui/` devem ser adapters finos que delegam ao código em `<slug>/interfaces/`, não novos lugares para regra de negócio. Evite expor `python -m <slug>.tui` e `python -m <slug>.gui` como comandos públicos novos.
- JavaScript e TypeScript usam `npm start` e `npm test` como comandos públicos.
- Go deve preferir `cmd/<slug>` quando houver binário e evitar esconder domínio em scripts soltos.
- Swift segue convenção de Swift Package Manager.
- C# segue convenção de solução/projetos com `src/` e `tests/`, porque essa é a convenção forte do ecossistema.
- `src/` não é proibido; ele só precisa ser consciente e documentado. Para Python novo, o padrão do kit continua sendo pacote direto na raiz.

## Toolchains ausentes

Agentes não devem falhar uma rodada estrutural apenas porque `go`, `swift` ou `dotnet` não estão instalados localmente. Nesse caso, devem gerar a baseline correta, não rodar a validação de runtime e registrar a limitação na resposta final.
