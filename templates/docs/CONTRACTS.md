# CONTRACTS

## 1. Objetivo

Registrar entradas, saídas, identificadores, eventos e assunções do sistema de forma explícita e auditável.

## 2. Entradas Canônicas

| Nome | Origem | Formato | Obrigatório | Observações |
| --- | --- | --- | --- | --- |
| `{{input_1}}` | `{{origem}}` | `{{json/csv/http/file}}` | sim | `{{observação}}` |
| `{{input_2}}` | `{{origem}}` | `{{json/csv/http/file}}` | não | `{{observação}}` |

## 3. Saídas Canônicas

| Nome | Destino | Formato | Garantias |
| --- | --- | --- | --- |
| `{{output_1}}` | `{{destino}}` | `{{json/file/db}}` | `{{garantia}}` |
| `{{output_2}}` | `{{destino}}` | `{{json/file/db}}` | `{{garantia}}` |

## 4. Identificadores e chaves

| Conceito | Campo canônico | Observações |
| --- | --- | --- |
| `{{entidade_1}}` | `{{field_1}}` | `{{não assumir equivalência com ...}}` |
| `{{entidade_2}}` | `{{field_2}}` | `{{observação}}` |

## 5. Eventos ou etapas de pipeline

| Etapa | Entrada | Saída | Falhas esperadas |
| --- | --- | --- | --- |
| `{{step_1}}` | `{{input}}` | `{{output}}` | `{{failures}}` |
| `{{step_2}}` | `{{input}}` | `{{output}}` | `{{failures}}` |

## 6. Assunções ainda não validadas

- {{assuncao_1}}
- {{assuncao_2}}

Marque explicitamente o que foi observado no ambiente real e o que ainda é apenas inferência.

## 7. Quebras de contrato

Registre aqui mudanças que exigem:

- migração de dados
- ajuste de integração
- restart operacional
- versão nova de cliente

Formato sugerido:

- `YYYY-MM-DD`: {{descricao_curta_da_quebra}}
