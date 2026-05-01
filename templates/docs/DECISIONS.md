# DECISIONS

Use este arquivo para registrar decisões arquiteturais de forma leve. O objetivo
não é burocracia; é evitar que o repositório mude de forma silenciosa.

## Como registrar

Cada decisão relevante deve incluir:

- data
- contexto
- decisao
- impacto
- tradeoff
- alternativa rejeitada

## Template

### YYYY-MM-DD - {{titulo_curto_da_decisao}}

**Contexto**

{{qual problema levou à decisão}}

**Decisão**

{{o que foi escolhido}}

**Impacto**

- {{impacto_1}}
- {{impacto_2}}

**Tradeoff**

- {{tradeoff_1}}
- {{tradeoff_2}}

**Alternativas rejeitadas**

- {{alternativa_1}}
- {{alternativa_2}}

---

## Exemplos de decisões que merecem registro

- mudar branch policy
- trocar formato de configuração
- trocar banco ou local de persistência
- introduzir fila, worker ou deploy remoto
- mover responsabilidade entre repositórios
- formalizar ou quebrar um contrato externo
