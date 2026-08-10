# Prompt Projeto Existente

```text
Alinhe o projeto atual à estrutura proposta pelo projeto em ~/Skidbladnir.

Instruções:
- Leia o repositório atual antes de editar qualquer arquivo.
- Leia ~/Skidbladnir/README.md.
- Leia ~/Skidbladnir/docs/existing-project.md.
- Leia ~/Skidbladnir/docs/runtimes.md.
- Leia ~/Skidbladnir/docs/deploy-manifest.md.
- Preserve o comportamento real do projeto.
- Preserve o runtime existente, salvo incompatibilidade concreta com plataforma, SDK, operação ou requisito mensurável; preferência de linguagem não justifica migração.
- Preserve entrypoints existentes; se criar uma TUI ou GUI Python dedicada, prefira um launcher fino `python -m tui` ou `python -m gui` a um novo comando público aninhado em `<slug>`.
- Não faça refactor cosmético de diretórios.
- Adote README, AGENTS, PROJECT_GATE, docs estruturais, deploy/manifest.json e scripts de validação de forma compatível com o sistema real.
- Se o projeto não tiver deploy, declare deploy.target como none e justifique.
- Se o deploy for manual, declare deploy.target como manual e descreva smoke, rollback e restart reais.
- Rode validações possíveis e explique bloqueios com precisão.
- Termine com resumo de mudanças, validações executadas, pendências e fragilidades que continuam reais.
```
