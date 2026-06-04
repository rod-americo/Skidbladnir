# C# Runtime Template

Use `src/<Project>/` e `tests/<Project>.Tests/`, seguindo a convenção do ecossistema .NET.

Comandos:

```bash
dotnet restore
dotnet build
dotnet run --project src/<Project>
dotnet test
```

O manifesto deve usar `runtime.id` como `csharp`.
