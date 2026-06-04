# Deploy Manifest

O `deploy/manifest.json` é o contrato obrigatório de operação e deploy do Skidbladnir. Ele não executa deploy; ele declara como o projeto deve ser operado, validado, reiniciado, observado, recuperado e revertido.

## Por que JSON

O formato canônico inicial é JSON para permitir validação com Python stdlib, sem dependência de YAML. Projetos podem manter exemplos YAML adicionais, mas o arquivo obrigatório validado é `deploy/manifest.json`.

O schema formal vive em `schema/deploy-manifest.schema.json` no kit e também deve ser copiado para projetos alinhados. O script `scripts/check_deploy_manifest.py` continua sendo o validador operacional sem dependências externas.

## Campos obrigatórios

- `version`: versão do schema, atualmente `1`
- `project.name`: nome humano do projeto
- `project.slug`: identificador técnico
- `runtime.id`: runtime principal
- `runtime.version`: versão esperada do runtime
- `deploy.target`: `none`, `manual`, `local`, `systemd`, `container`, `compose`, `kubernetes` ou outro alvo justificado
- `deploy.reason`: justificativa do alvo escolhido
- `process.command`: comando principal quando `deploy.target` não for `none`
- `healthcheck.command` ou `healthcheck.http`: validação mínima operacional quando `deploy.target` não for `none`
- `ports`: lista de portas expostas, vazia quando não houver
- `environment.required`: variáveis obrigatórias
- `secrets.required`: segredos obrigatórios, sem valores reais
- `runtime_state.paths`: caminhos de estado mutável
- `logs.paths`: caminhos de logs
- `restart.policy`: regra de restart
- `backup.policy`: regra de backup ou declaração explícita de ausência de persistência relevante
- `rollback.strategy`: estratégia de rollback

## Exemplo mínimo

```json
{
  "version": 1,
  "project": {
    "name": "MeuWorker",
    "slug": "meu_worker"
  },
  "runtime": {
    "id": "python",
    "version": "3.11+"
  },
  "deploy": {
    "target": "local",
    "reason": "worker local operado em host dedicado"
  },
  "process": {
    "command": "python -m meu_worker --interval 30",
    "working_directory": ".",
    "user": "worker-user"
  },
  "healthcheck": {
    "command": "python -m meu_worker --once",
    "timeout_seconds": 30
  },
  "ports": [],
  "environment": {
    "required": ["MEU_WORKER_CONFIG_FILE"],
    "optional": ["APP_ENV"]
  },
  "secrets": {
    "required": []
  },
  "runtime_state": {
    "paths": ["runtime/"]
  },
  "logs": {
    "paths": ["runtime/logs/"]
  },
  "restart": {
    "policy": "restart total do processo residente quando codigo ou config mudar"
  },
  "backup": {
    "policy": "copiar runtime/outbox e logs relevantes antes de limpeza"
  },
  "rollback": {
    "strategy": "voltar ao ultimo commit validado e preservar config local"
  }
}
```

## Projetos sem deploy

Projetos sem processo ou deploy ainda devem declarar o manifesto:

```json
{
  "version": 1,
  "project": {
    "name": "MinhaBiblioteca",
    "slug": "minha_biblioteca"
  },
  "runtime": {
    "id": "go",
    "version": "1.22+"
  },
  "deploy": {
    "target": "none",
    "reason": "biblioteca sem processo residente ou artefato implantável neste repositório"
  },
  "process": {},
  "healthcheck": {},
  "ports": [],
  "environment": {
    "required": [],
    "optional": []
  },
  "secrets": {
    "required": []
  },
  "runtime_state": {
    "paths": []
  },
  "logs": {
    "paths": []
  },
  "restart": {
    "policy": "não aplicável"
  },
  "backup": {
    "policy": "não há estado persistente operacional"
  },
  "rollback": {
    "strategy": "reverter commit ou tag consumida pelo downstream"
  }
}
```

## Validação

Use:

```bash
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py --deploy-strict
```

O primeiro comando valida o schema mínimo. O segundo valida coerência entre manifesto e documentação operacional quando o projeto já possui doctor.
