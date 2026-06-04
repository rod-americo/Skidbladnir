# Roadmap Inicial

## Princípio

O roadmap de `Skidbladnir` deve privilegiar clareza de protocolo, utilidade operacional para agentes e estabilidade do kit antes de adicionar volume de features.

## v1.0.x

Objetivo:

fechar a publicação inicial com tese clara, protocolo para agentes, instalação auxiliar simples e baseline confiável.

Frentes:

- publicar o projeto com nome, posicionamento e README público coerentes
- consolidar o uso principal por agentes lendo `~/Skidbladnir`
- manter a suíte de regressão do scaffolder estável
- consolidar templates e scripts comuns como fonte de verdade
- manter o fluxo de retrofit como caminho oficial para repositórios legados
- tornar `deploy/manifest.json` obrigatório nos projetos alinhados
- manter Python, Node, TypeScript, Go, Swift e C# como scaffolds auxiliares executáveis
- documentar claramente quando usar e quando não usar o kit

## v1.1

Objetivo:

melhorar ergonomia e previsibilidade do uso por agentes.

Frentes:

- prompts mais curtos para uso recorrente
- exemplos de saída reais por preset
- documentação pública com árvores por runtime
- modo mais simples para escolher presets
- melhoria do fluxo de atualização do `newproj` como compatibilidade auxiliar

## v1.2

Objetivo:

endurecer a recuperação de repositórios existentes.

Frentes:

- versão curta do prompt para agentes mais rápidos
- regras mais claras para adoção gradual de gate e doctor em bases legadas
- baseline de retrofit por classe de projeto: API, worker, pipeline, desktop
- exemplos reais de before/after em recuperação estrutural
- validação mais rica de `deploy/manifest.json` em repositórios legados

## v1.3

Objetivo:

expandir a camada de governança sem virar framework excessivo.

Frentes:

- regras opcionais por stack em `doctor.json`
- presets de documentação por domínio
- auditoria mais rica de inconsistências entre docs e operação
- convenções opcionais para changelog e releases
- aprofundar presets específicos por runtime sem transformar o kit em framework

## v2.0

Objetivo:

extrair uma camada comum realmente reutilizável sem destruir o caráter leve do kit.

Frentes:

- biblioteca core opcional para validação de gate, doctor e deploy manifest
- integração mais forte entre protocolo, scaffolder auxiliar e componentes compartilháveis
- estratégia de evolução sem acoplamento forçado entre repositórios

## O que evitar no roadmap

- transformar o projeto em framework universal
- adicionar dezenas de presets fracos só para parecer completo
- automatizar demais antes de consolidar a tese
- esconder tradeoffs reais atrás de marketing técnico
