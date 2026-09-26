# Prompt Novo Projeto

```text
Vou criar um projeto com o escopo abaixo e quero iniciá-lo já com a estrutura proposta pelo projeto em <SKIDBLADNIR_PATH>.

Escopo:
<DESCREVA_O_ESCOPO>

Instruções:
- Leia <SKIDBLADNIR_PATH>/README.md.
- Leia <SKIDBLADNIR_PATH>/docs/new-project.md.
- Leia <SKIDBLADNIR_PATH>/docs/runtimes.md.
- Leia <SKIDBLADNIR_PATH>/docs/deploy-manifest.md e <SKIDBLADNIR_PATH>/docs/agent-collaboration.md.
- Isole cada tarefa independente em branch/worktree ou checkout próprio, delimite arquivos/módulos e registre contexto em docs/TASK_TEMPLATE.md.
- Designe integrador; integração rotineira exige checks, revisão independente e permissões existentes. Valide novamente o resultado combinado.
- Integridade de dados, migrações, dados sensíveis, autenticação/permissões, produção, contratos incompatíveis, enfraquecimento dos controles e risco não esclarecido exigem decisão humana. Não habilite automerge remoto.
- Use <SKIDBLADNIR_PATH>/templates como fonte de verdade.
- Crie o projeto com documentação humana em pt-BR e identificadores técnicos em en-US.
- Escolha autonomamente o runtime por plataforma, SDKs obrigatórios, ambiente de deploy, distribuição, interoperabilidade e requisitos mensuráveis. Considere java, rust, go, csharp, swift, ts, node, python ou outro runtime justificado; use generic somente quando não houver runtime dominante.
- Não pergunte qual linguagem eu prefiro quando essas restrições forem suficientes; pergunte apenas pelo contexto material ausente.
- Nenhuma linguagem é default. Compare manutenção, prevenção de regressões, verificabilidade, bibliotecas, suporte, distribuição e requisitos medidos de escala; a existência de scaffold não favorece a escolha.
- Se usar a CLI, passe --runtime explicitamente, inclusive em presets Python.
- Registre no PROJECT_GATE as restrições determinantes, o runtime escolhido, alternativas viáveis, justificativa operacional, riscos, mitigação, evidências e critérios mensuráveis de escala.
- Em Python, mantenha `python -m <slug>` para o domínio e prefira launchers finos `python -m tui` ou `python -m gui` quando essas interfaces forem aplicações dedicadas.
- Crie README, AGENTS, PROJECT_GATE, docs estruturais, deploy/manifest.json e scripts de validação aplicáveis.
- Não declare deploy, teste, contrato ou maturidade que o projeto ainda não sustenta.
- Execute os checks exigidos; ferramenta ausente é bloqueio, não aprovação. Separe validação documental, testes, smoke e saúde operacional.
```
