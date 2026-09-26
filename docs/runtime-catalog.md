# Catálogo de runtimes

Gerado por `python3 sync_runtime_catalog.py`. Edite `templates/runtimes/catalog.json` e regenere; os checks de CI detectam divergência.

Versões concretas da release; consulta em 2026-09-26. Python 3.14.6 executa os validadores estruturais em todos os jobs, sem determinar a linguagem da aplicação.

| ID | Linguagem | Toolchain | Presets |
| --- | --- | --- | --- |
| `python` | Python | 3.14.6 | base, fastapi, cli, textual-cli, worker, playwright-worker, pipeline, dicom-pipeline |
| `node` | JavaScript | 24.21.0 | base |
| `ts` | TypeScript | 24.21.0 | base |
| `go` | Go | 1.27.1 | base |
| `swift` | Swift | 6.4.0 | base |
| `csharp` | C# | 10.0.401 | base |
| `java` | Java | 25.0.4.1+1 | base |
| `rust` | Rust | 1.98.1 | base |
| `generic` | sem runtime dominante | not-applicable | base |

`node` gera JavaScript; `ts` gera TypeScript sobre Node. `js` continua válido como identificador legado no manifesto. `generic` representa ausência de runtime dominante, não uma escolha automática.

## Comandos por runtime

Os marcadores `{slug}`, `{module}`, `{dist}` e `{sources}` são substituídos na geração. O Java usa Maven 3.9.16 pelo wrapper versionado. O Rust fixa edição 2024.

### Python (`python`)

Bootstrap:

```bash
python3 -m venv .venv --prompt $(basename "$PWD")
source .venv/bin/activate
python -m pip install --require-hashes -r requirements.txt
```

Checks de desenvolvimento:

```bash
python -m ruff check {sources} tests && python -m mypy {sources} && python -m pytest -q
python -m compileall -q {sources} scripts tests
```

Smoke local:

```bash
python -m {slug} --help
```

### Node (`node`)

Bootstrap:

```bash
npm ci
```

Checks de desenvolvimento:

```bash
npm test
node --check {slug}/main.mjs
```

Smoke local:

```bash
npm start
```

### TypeScript (`ts`)

Bootstrap:

```bash
npm ci
```

Checks de desenvolvimento:

```bash
npm test
npm run build
```

Smoke local:

```bash
npm start
```

### Go (`go`)

Bootstrap:

```bash
go mod download
```

Checks de desenvolvimento:

```bash
go vet ./... && go test -race ./...
go build -o bin/{slug} ./cmd/{slug}
```

Smoke local:

```bash
go run ./cmd/{slug}
```

### Swift (`swift`)

Bootstrap:

```bash
swift package resolve
```

Checks de desenvolvimento:

```bash
swift test
swift build
```

Smoke local:

```bash
swift run {module}
```

### .NET (`csharp`)

Bootstrap:

```bash
dotnet restore {module}.sln --locked-mode
```

Checks de desenvolvimento:

```bash
dotnet test {module}.sln --no-restore
dotnet build {module}.sln --no-restore
```

Smoke local:

```bash
dotnet run --no-restore --project src/{module}/{module}.csproj
```

### Java (`java`)

Bootstrap:

```bash
./mvnw -B verify
```

Checks de desenvolvimento:

```bash
./mvnw -B verify
./mvnw -B package
```

Smoke local:

```bash
java -jar target/{dist}-0.1.0.jar
```

### Rust (`rust`)

Bootstrap:

```bash
cargo build --locked
```

Checks de desenvolvimento:

```bash
cargo fmt --all -- --check && cargo clippy --locked --all-targets -- -D warnings && cargo test --locked
cargo build --locked --release
```

Smoke local:

```bash
cargo run --locked
```
