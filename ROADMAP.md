# Roadmap Inicial

## Princípio

O roadmap de `Skidbladnir` deve privilegiar clareza de produto, utilidade operacional e estabilidade do kit antes de adicionar volume de features.

## v1.0.x

Objetivo:

fechar a publicação inicial com tese clara, instalação simples e baseline confiável.

Frentes:

- publicar o projeto com nome, posicionamento e README público coerentes
- manter a suíte de regressão do scaffolder estável
- consolidar os presets principais já existentes
- manter o prompt de retrofit como caminho oficial para repositórios legados
- documentar claramente quando usar e quando não usar o kit

## v1.1

Objetivo:

melhorar ergonomia e previsibilidade do uso diário.

Frentes:

- comando de bootstrap mais direto para instalação local
- exemplos de saída reais por preset
- documentação pública com árvores de projeto gerado
- modo mais simples para escolher presets
- melhoria do fluxo de atualização do `newproj`

## v1.2

Objetivo:

endurecer a recuperação de repositórios existentes.

Frentes:

- versão curta do prompt para agentes mais rápidos
- regras mais claras para adoção gradual de gate e doctor em bases legadas
- baseline de retrofit por classe de projeto: API, worker, pipeline, desktop
- exemplos reais de before/after em recuperação estrutural

## v1.3

Objetivo:

expandir a camada de governança sem virar framework excessivo.

Frentes:

- regras opcionais por stack em `doctor.json`
- presets de documentação por domínio
- auditoria mais rica de inconsistências entre docs e operação
- convenções opcionais para changelog e releases

## v2.0

Objetivo:

extrair uma camada comum realmente reutilizável sem destruir o caráter leve do kit.

Frentes:

- biblioteca core opcional para config, logging e contratos
- integração mais forte entre scaffolder e componentes compartilháveis
- estratégia de evolução sem acoplamento forçado entre repositórios

## O que evitar no roadmap

- transformar o projeto em framework universal
- adicionar dezenas de presets fracos só para parecer completo
- automatizar demais antes de consolidar a tese
- esconder tradeoffs reais atrás de marketing técnico
