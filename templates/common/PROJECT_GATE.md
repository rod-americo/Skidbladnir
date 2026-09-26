# PROJECT GATE

<!-- skidbladnir:gate:2 -->

Preencha este arquivo antes de consolidar um novo repositório.

Respostas vagas como `a definir`, `não sei`, `talvez`, `N/A` ou frases curtas demais fazem o gate falhar quando o repositório nasce com enforcement ativo.

## 1. Por que este projeto existe?

- problema real:
- usuário ou operador alvo:
- resultado esperado:

## 2. Por que isto NÃO deveria ser um módulo?

- repositório candidato que poderia absorver isso:
- por que esse acoplamento seria inadequado:
- fronteira que justifica um repositório separado:

## 3. O que este projeto compartilha com o ecossistema?

- configuração:
- logging:
- runtime:
- contratos:
- autenticação ou transporte:

Se a resposta for "quase tudo", provavelmente isso ainda não deveria nascer como repositório.

## 4. O que este projeto NÃO pode carregar?

- responsabilidades fora de escopo:
- integrações que pertencem a outro sistema:
- dados que não devem morar aqui:

## 5. Qual É O Custo De Manutenção Esperado?

- host ou ambiente principal:
- dependência externa mais frágil:
- necessidade de restart:
- necessidade de backup:
- risco operacional:

## 6. Por que este runtime foi escolhido?

Compare alternativas viáveis por manutenção, prevenção de regressões, verificabilidade, bibliotecas, suporte, distribuição e operação. Nenhuma linguagem é default; a disponibilidade de scaffold não é critério de preferência. Preserve um runtime existente adequado e contabilize custo e risco de qualquer migração. Registre hipóteses e como serão verificadas; “escalável” sem medida não é evidência.

- restrições determinantes do runtime:
- runtime escolhido: `{{RUNTIME_ID}}`
- alternativa principal considerada:
- justificativa operacional:
- riscos e mitigações do runtime:
- evidências para a escolha:
- critérios mensuráveis de escala:

## 7. Condição de saída

Este repositório só deveria existir se:

- houver fronteira de escopo defensável
- houver contrato de entrada e saída identificável
- houver operação própria ou ciclo de evolução independente
- o custo de mais um repo for menor que o custo de acoplamento
