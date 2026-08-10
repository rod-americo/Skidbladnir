# Validação

Este documento define a validação mínima esperada para projetos alinhados ao Skidbladnir.

## Validação comum

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --strict
python3 scripts/project_doctor.py --deploy-strict
python3 scripts/project_doctor.py --audit-config
```

Use `--strict` quando os docs principais já estiverem preenchidos. Use `--deploy-strict` quando `docs/OPERATIONS.md` e `deploy/manifest.json` precisarem estar coerentes. Use `--audit-config` quando houver aliases ou warnings ignorados em `config/doctor.json`.

## Validação por runtime

| Runtime | Sintaxe/build | Teste |
| --- | --- | --- |
| Python | `python -m compileall -q <slug> scripts tests` | `python -m pytest -q` |
| JavaScript | `node --check <arquivo>` quando aplicável | `npm test` |
| TypeScript | `npm run build` | `npm test` |
| Go | `go test ./...` | `go test ./...` |
| Swift | `swift build` | `swift build && swift run <Module>` |
| C# | `dotnet build <Project>.sln` | `dotnet test <Project>.sln` |

## Regra de honestidade

Se a toolchain não existir localmente, não invente validação. Registre o comando esperado e informe que ele não foi executado por ausência de ambiente.

## Critério mínimo antes de concluir uma rodada

- `git diff` revisado
- scripts comuns executados ou bloqueio explicado
- teste do runtime executado ou bloqueio explicado
- manifesto de deploy coerente com operação real
- `PROJECT_GATE.md` registra restrições, runtime escolhido, alternativa considerada e justificativa operacional
- docs atualizados junto com qualquer mudança de comando, contrato, restart, runtime state, log, backup ou rollback
