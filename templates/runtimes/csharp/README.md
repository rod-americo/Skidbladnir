# C# Runtime Template

Use `src/<Project>/` e `tests/<Project>.Tests/`, seguindo a convenção do ecossistema .NET.

Comandos:

```bash
dotnet restore <Project>.sln
dotnet build <Project>.sln
dotnet run --project src/<Project>/<Project>.csproj
dotnet test <Project>.sln
```

O manifesto deve usar `runtime.id` como `csharp`.
