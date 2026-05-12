# Posicionamento do Projeto

## Nome

`Skidbladnir`

## Tese

`Skidbladnir` é um kit para criar projetos novos e recuperar repositórios já em funcionamento com uma baseline mínima de arquitetura, documentação, governança e operação.

Ele existe para reduzir o padrão recorrente de repositórios que:

- nascem sem fronteira clara
- crescem sem contratos explícitos
- acumulam operação implícita
- dependem demais de contexto mental do autor

## O que o projeto faz

- gera projetos novos com estrutura base, docs e validações
- endurece a criação com `PROJECT_GATE.md`
- verifica coerência estrutural com `project_doctor.py`
- oferece prompts e artefatos para retrofit de repositórios legados

## O que o projeto não é

- framework universal de arquitetura
- template genérico para qualquer stack sem adaptação
- plataforma de deploy
- substituto de revisão técnica, design de sistema ou disciplina de equipe

## Público-alvo

- engenheiros aplicados
- autores de sistemas operacionais internos
- mantenedores de automações, workers, pipelines e integrações
- pessoas que precisam criar ou recuperar repositórios sem cair em caos documental e estrutural

## Proposta de valor

O valor do projeto não está apenas no scaffolder. Ele está no conjunto:

- criação de projeto com fronteira explícita
- documentação-base coerente
- gate de existência do repositório
- doctor para detectar desalinhamento estrutural
- prompts para recuperação de bases legadas
- presets práticos para stacks operacionais reais

## Diferencial

`Skidbladnir` não tenta transformar todo projeto em framework. Ele trabalha com uma ideia mais pragmática: tornar explícitas as decisões mínimas que evitam retrabalho, ambiguidade e degradação operacional conforme o repositório cresce.
