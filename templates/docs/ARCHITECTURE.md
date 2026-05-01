# ARCHITECTURE

## 1. Objetivo

Descreva o problema técnico que este sistema resolve e a função dele dentro do
ecossistema.

## 2. Escopo

Inclui:

- {{responsabilidade_1}}
- {{responsabilidade_2}}

Não inclui:

- {{fora_do_escopo_1}}
- {{fora_do_escopo_2}}

## 3. Contexto do sistema

Entradas externas:

- {{API / fila / arquivo / PACS / webhook / operador}}

Saídas externas:

- {{banco / evento / arquivo / API / dashboard / integração}}

Dependências críticas:

- {{dependencia_1}}
- {{dependencia_2}}

## 4. Módulos Principais

### 4.1 Domain

- entidades e regras centrais
- invariantes do problema
- nomes e conceitos canônicos

### 4.2 Application

- casos de uso
- coordenação de fluxo
- políticas de orquestração

### 4.3 Infrastructure

- persistência
- transport
- APIs externas
- filesystem
- filas e workers

### 4.4 Interfaces

- CLI
- HTTP API
- TUI/GUI
- cron/worker

## 5. Fluxo principal

Descreva o fluxo end-to-end em passos numerados:

1. {{entrada}}
2. {{validação / transformação}}
3. {{persistência / orquestração}}
4. {{saída}}

## 6. Contratos e invariantes

- entrada canônica: `{{entrada_canonica}}`
- saída canônica: `{{saida_canonica}}`
- identificador primário: `{{id_primario}}`
- invariantes:
  - {{invariante_1}}
  - {{invariante_2}}

Se houver contratos externos pouco confiáveis, documente o que é garantido e o
que ainda depende de validação real.

## 7. Persistência

- armazenamento principal: `{{sqlite / postgres / filesystem / none}}`
- localização do runtime state: `{{path}}`
- estratégia de backup/retenção: `{{estratégia}}`
- políticas de migração: `{{como_migrar}}`

## 8. Configuração

- fonte de configuração: `env`, `arquivo`, `CLI` ou combinação
- arquivo versionado de exemplo: `{{arquivo_exemplo}}`
- configuração host-local ignorada: `{{arquivo_local}}`

## 9. Observabilidade

- logger central: `{{sim/não}}`
- formato de logs: `{{json / key-value / outro parseável}}`
- métricas mínimas: `{{fila, latency, throughput, errors, etc}}`
- healthcheck ou smoke test: `{{comando ou endpoint}}`

## 10. Riscos e tradeoffs

- risco técnico principal: `{{risco_1}}`
- acoplamento consciente: `{{acoplamento_1}}`
- parte ainda experimental: `{{parte_experimental}}`

## 11. Decisões abertas

- {{decisao_aberta_1}}
- {{decisao_aberta_2}}
