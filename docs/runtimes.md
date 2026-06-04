# Runtimes

Este documento define a matriz multilinguagem do Skidbladnir para agentes. A CLI atual materializa Python, Node, TypeScript, Go, Swift e C#; agentes devem usar esta matriz como referência e adaptar os templates ao contexto real.

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

- Python usa `python -m <slug>` como entrypoint público primário.
- JavaScript e TypeScript usam `npm start` e `npm test` como comandos públicos.
- Go deve preferir `cmd/<slug>` quando houver binário e evitar esconder domínio em scripts soltos.
- Swift segue convenção de Swift Package Manager.
- C# segue convenção de solução/projetos com `src/` e `tests/`, porque essa é a convenção forte do ecossistema.
- `src/` não é proibido; ele só precisa ser consciente e documentado. Para Python novo, o padrão do kit continua sendo pacote direto na raiz.

## Toolchains ausentes

Agentes não devem falhar uma rodada estrutural apenas porque `go`, `swift` ou `dotnet` não estão instalados localmente. Nesse caso, devem gerar a baseline correta, não rodar a validação de runtime e registrar a limitação na resposta final.
