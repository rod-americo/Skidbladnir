# Prompt Novo Projeto

```text
Vou criar um projeto com o escopo abaixo e quero iniciá-lo já com a estrutura proposta pelo projeto em ~/Skidbladnir.

Escopo:
<DESCREVA_O_ESCOPO>

Instruções:
- Leia ~/Skidbladnir/README.md.
- Leia ~/Skidbladnir/docs/new-project.md.
- Leia ~/Skidbladnir/docs/runtimes.md.
- Leia ~/Skidbladnir/docs/deploy-manifest.md.
- Use ~/Skidbladnir/templates como fonte de verdade.
- Crie o projeto com documentação humana em pt-BR e identificadores técnicos em en-US.
- Escolha autonomamente o runtime entre python, node, ts, go, swift, csharp ou generic a partir de plataforma, SDKs obrigatórios, ambiente de deploy, formato de distribuição, interoperabilidade e requisitos mensuráveis.
- Não pergunte qual linguagem eu prefiro quando essas restrições forem suficientes; pergunte apenas pelo contexto material ausente.
- Preserve Python como default quando nenhuma restrição determinar outra escolha.
- Registre no PROJECT_GATE as restrições determinantes, o runtime escolhido, a principal alternativa considerada e a justificativa operacional.
- Em Python, mantenha `python -m <slug>` para o domínio e prefira launchers finos `python -m tui` ou `python -m gui` quando essas interfaces forem aplicações dedicadas.
- Crie README, AGENTS, PROJECT_GATE, docs estruturais, deploy/manifest.json e scripts de validação aplicáveis.
- Não declare deploy, teste, contrato ou maturidade que o projeto ainda não sustenta.
- Rode as validações possíveis e explique bloqueios com precisão.
```
