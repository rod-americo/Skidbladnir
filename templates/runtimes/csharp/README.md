# C#/.NET

Use `src/<Project>/` e `tests/<Project>.Tests/`. SDK em `global.json`, lockfiles versionados e `dotnet restore --locked-mode` tornam o bootstrap explícito. Execute `dotnet test` após restore. O arquivo de configuração de exemplo ainda depende de adaptação para ser consumido.

Versões e comandos exatos estão no [catálogo](../catalog.json) e na [documentação gerada](../../../docs/runtime-catalog.md). A existência deste scaffold não favorece a escolha da linguagem. O baseline usa `deploy.target: none`, salvo preset com operação HTTP local explícita.
