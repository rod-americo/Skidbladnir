# OPERATIONS

## 1. Objetivo

Este documento deve permitir executar, diagnosticar, reiniciar e recuperar o sistema sem depender de contexto implícito.

## 2. Ambientes

| Ambiente | Objetivo | Runtime | Observações |
| --- | --- | --- | --- |
| `local` | desenvolvimento | `{{runtime}}` | `{{obs}}` |
| `homolog` | validação | `{{runtime}}` | `{{obs}}` |
| `prod` | operação | `{{runtime}}` | `{{obs}}` |

## 3. Como executar

### Boot local

```bash {{LOCAL_BOOT_COMMANDS}}
```

### Boot principal

```bash
{{PRIMARY_RUN_COMMAND}}
```

## 4. Configuração operacional

- arquivo local: `{{config_local}}`
- variáveis de ambiente críticas:
  - `{{ENV_1}}`
  - `{{ENV_2}}`
- path de runtime state: `{{runtime_path}}`
- path de logs: `{{logs_path}}`

## 5. Validação mínima

Depois de subir:

```bash {{SMOKE_TEST_COMMAND}}
```

Conferir:

- processo principal em execução
- logs sem erro de bootstrap
- dependência externa acessível
- persistência funcionando

## 6. Logs E Diagnóstico

- logger principal: `{{logger}}`
- formato dos logs: `{{json / key-value / outro}}`
- onde ler logs:
  - `{{arquivo_ou_journal}}`
- sinais de falha comuns:
  - {{falha_1}}
  - {{falha_2}}

## 7. Restart policy

Ao mudar:

- `domain/` ou `application/`: `{{restart_impact}}`
- `infrastructure/`: `{{restart_impact}}`
- `interfaces/`: `{{restart_impact}}`
- `config/`: `{{restart_impact}}`
- `docs/` apenas: `{{restart_impact}}`

## 8. Persistência, backup e limpeza

- armazenamento principal: `{{storage}}`
- backup: `{{como_e_onde}}`
- retenção: `{{política}}`
- limpeza segura: `{{o_que_pode_ser_removido}}`

Nunca remova:

- {{estado_critico_1}}
- {{estado_critico_2}}

## 9. Incidentes

Checklist mínimo:

1. confirmar configuração carregada
2. confirmar dependência externa
3. confirmar permissão/path de runtime
4. confirmar logs e último erro estruturado
5. confirmar se houve mudança recente de contrato

## 10. Mudanças que exigem update deste documento

- novo entrypoint
- nova dependência operacional
- novo path de runtime
- nova regra de restart
- nova rotina de backup ou limpeza
