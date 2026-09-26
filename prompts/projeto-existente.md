# Prompt Projeto Existente

```text
Alinhe o projeto atual à estrutura proposta pelo projeto em <SKIDBLADNIR_PATH>.

Instruções:
- Leia o repositório atual antes de editar qualquer arquivo.
- Leia <SKIDBLADNIR_PATH>/README.md.
- Leia <SKIDBLADNIR_PATH>/docs/existing-project.md.
- Leia <SKIDBLADNIR_PATH>/docs/runtimes.md.
- Leia <SKIDBLADNIR_PATH>/docs/deploy-manifest.md e <SKIDBLADNIR_PATH>/docs/agent-collaboration.md.
- Isole cada tarefa independente em branch/worktree ou checkout próprio, delimite arquivos/módulos e registre contexto em docs/TASK_TEMPLATE.md.
- Designe integrador; integração rotineira exige checks, revisão independente e permissões existentes. Valide novamente o resultado combinado.
- Integridade de dados, migrações, dados sensíveis, autenticação/permissões, produção, contratos incompatíveis, enfraquecimento dos controles e risco não esclarecido exigem decisão humana. Não habilite automerge remoto.
- Preserve o comportamento real do projeto. Nenhuma linguagem é default; migrações exigem benefício concreto e consideração do custo de transição.
- Preserve o runtime existente, salvo incompatibilidade concreta com plataforma, SDK, operação ou requisito mensurável; preferência de linguagem não justifica migração.
- Preserve entrypoints existentes; se criar uma TUI ou GUI Python dedicada, prefira um launcher fino `python -m tui` ou `python -m gui` a um novo comando público aninhado em `<slug>`.
- Não faça refactor cosmético de diretórios.
- Adote README, AGENTS, PROJECT_GATE, docs estruturais, deploy/manifest.json e scripts de validação de forma compatível com o sistema real.
- Se o projeto não tiver deploy, declare deploy.target como none e justifique.
- Se o deploy for manual, declare deploy.target como manual e descreva smoke, rollback e restart reais.
- Execute os checks exigidos; ferramenta ausente é bloqueio, não aprovação. Separe validação documental, testes, smoke e saúde operacional.
- Termine com resumo de mudanças, validações executadas, pendências e fragilidades que continuam reais.
```
