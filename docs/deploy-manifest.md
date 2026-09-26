# Manifesto operacional

Todo projeto alinhado ao kit possui `deploy/manifest.json`, mesmo quando ainda não tem implantação. O formato JSON versão 1 é validado com Python stdlib e preserva a estrutura e os identificadores anteriores, incluindo `node` e `js`. A versão 2.0 do kit não altera a versão do manifesto.

## Campos e significado

- `project.name` e `project.slug`: identidade do projeto.
- `runtime.id` e `runtime.version`: identificador estável e versão concreta. Outros runtimes são permitidos; `generic` só significa ausência de runtime dominante.
- `deploy.target` e `deploy.reason`: destino real ou `none`, com justificativa.
- `process`: comando principal, diretório e usuário quando aplicáveis. Sem processo, pode ser vazio.
- `healthcheck.command` ou `healthcheck.http.url`: probe operacional quando houver implantação. HTTP precisa de URL HTTP(S) válida, com host e sem credenciais; objeto HTTP vazio é inválido.
- `ports`, `environment`, `secrets`: portas e nomes de entradas realmente usadas; nunca valores secretos.
- `runtime_state.paths` e `logs.paths`: destinos efetivamente usados. Stdout não é um arquivo; nesse caso `logs.paths` é vazio e OPERATIONS descreve o coletor quando existir.
- `restart.policy`, `backup.policy` e `rollback.strategy`: procedimentos reais ou explicação da ausência de serviço/estado.

## Baseline sem implantação

O baseline abaixo declara um comando local finito; não inventa serviço, healthcheck, estado persistente ou destino de log:

```json
{
  "version": 1,
  "project": {
    "name": "Ferramenta",
    "slug": "ferramenta"
  },
  "runtime": {
    "id": "rust",
    "version": "1.98.1"
  },
  "deploy": {
    "target": "none",
    "reason": "baseline sem implantação configurada; comando local documentado"
  },
  "process": {
    "command": "cargo run --locked",
    "working_directory": "."
  },
  "healthcheck": {},
  "ports": [],
  "environment": {
    "required": [],
    "optional": [
      "FERRAMENTA_CONFIG_FILE"
    ]
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
    "policy": "não há serviço supervisionado no baseline"
  },
  "backup": {
    "policy": "não há estado persistente criado pelo baseline"
  },
  "rollback": {
    "strategy": "restaurar artefato validado anterior e preservar configuração e dados locais"
  }
}
```

## Serviço HTTP local

O preset FastAPI configura um exemplo local com porta 8000 e probe real. Host e porta podem ser alterados por CLI/ambiente; atualize manifesto e OPERATIONS juntos. Antes de qualquer produção, revise a implantação, permissões, dados e estratégia de retorno.

```json
{
  "version": 1,
  "project": {
    "name": "Api",
    "slug": "api"
  },
  "runtime": {
    "id": "python",
    "version": "3.14.6"
  },
  "deploy": {
    "target": "local",
    "reason": "serviço HTTP local de exemplo; reveja o contrato antes de implantar"
  },
  "process": {
    "command": "python -m api",
    "working_directory": "."
  },
  "healthcheck": {
    "http": {
      "url": "http://127.0.0.1:8000/health"
    },
    "timeout_seconds": 5
  },
  "ports": [
    8000
  ],
  "environment": {
    "required": [],
    "optional": [
      "API_CONFIG_FILE",
      "SERVER_HOST",
      "SERVER_PORT"
    ]
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
    "policy": "reiniciar processo após alteração de código ou configuração"
  },
  "backup": {
    "policy": "não há estado persistente criado pelo baseline"
  },
  "rollback": {
    "strategy": "restaurar artefato validado anterior e preservar configuração e dados locais"
  }
}
```

## Workers e projetos existentes

Workers gerados não possuem probe seguro nem supervisão configurada e usam `deploy.target: none`, com adaptação pendente. `--once` pode processar dados e não comprova saúde de outro processo; testes de desenvolvimento também não são probes. Defina readiness/liveness ou uma verificação sem efeito de negócio apropriada ao worker real.

Em projeto existente, descreva operação observada. Use `manual` apenas se há implantação manual real, com processo e probe adequados. Não declare systemd, container, Kubernetes, portas, backup ou arquivos de logs que o código não utiliza. Ausência de implantação é `none`; não omita o manifesto.

## Validação e limites

```bash
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py --deploy-strict
```

O primeiro comando valida schema e regras operacionais de preenchimento. O doctor compara declarações com a documentação. Nenhum deles executa comandos do manifesto, acessa URLs ou comprova saúde. Testes, smoke e verificação operacional devem ser executados separadamente em contexto autorizado.

A especificação formal fica em `schema/deploy-manifest.schema.json`. O template inicial sem implantação fica em `templates/deploy/manifest.json` e é usado pelo scaffolder; presets acrescentam somente as capacidades que materializam.
