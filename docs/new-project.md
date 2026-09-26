# Novo projeto

Use este fluxo ao iniciar um projeto com o protocolo Skidbladnir. O agente lê o kit e adapta seus templates; `newproj` é um bootstrap auxiliar. O clone pode estar em qualquer diretório informado pelo usuário.

## Descoberta e decisão

Leia `README.md`, `docs/runtimes.md`, `docs/deploy-manifest.md`, `docs/validation.md` e `templates/`. Determine objetivo, fronteira de responsabilidade, contratos, manutenção, bibliotecas obrigatórias, distribuição, operação e requisitos mensuráveis de escala.

Escolha linguagem/runtime pelas restrições e evidências. Nenhuma linguagem é default. Compare alternativas viáveis; a existência de scaffold não favorece uma delas. Registre no `PROJECT_GATE.md` restrições, alternativas, justificativa, riscos, mitigação, evidências e critérios de escala. Se ainda não houver requisito de escala, justifique isso e defina como identificar a necessidade, sem inventar uma meta. Use `docs/DECISIONS.md` para decisões e experimentos relevantes.

A CLI exige `--runtime` explícito. Consulte `newproj --list-presets` para as combinações disponíveis. Java e Rust têm preset `base`; presets especializados existentes são Python. Runtimes adicionais podem ser adaptados pelo protocolo e declarados no manifesto. `generic` só representa ausência de runtime dominante.

## Entregáveis

- `README.md`, `AGENTS.md`, `PROJECT_GATE.md` e `CHANGELOG.md`.
- `docs/ARCHITECTURE.md`, `docs/CONTRACTS.md`, `docs/OPERATIONS.md` e `docs/DECISIONS.md`.
- `docs/TASK_TEMPLATE.md`, para tarefas e passagens de contexto.
- `deploy/manifest.json`, `schema/deploy-manifest.schema.json` e exemplos de configuração.
- `config/doctor.json` e validadores comuns em `scripts/`.
- Código, testes de comportamento e CI conforme o runtime escolhido.
- `START_CHECKLIST.md` e `papers/` quando necessários.

`templates/` é a fonte de verdade dos arquivos gerados. Siga as convenções do ecossistema; crie somente fronteiras úteis e justifique quatro camadas se adotadas. Para projetos pequenos, um núcleo testável e um entrypoint podem bastar.

## Operação e colaboração

Todo projeto tem manifesto. Sem implantação configurada, use `deploy.target: none` com motivo. Testes de desenvolvimento e smoke local não substituem probe operacional. Só declare estado, logs, portas e variáveis que o código realmente usa. Workers precisam de supervisão e probe seguro antes da implantação.

Use o [protocolo de colaboração](agent-collaboration.md): uma tarefa por checkout isolado, escopo explícito, integrador para mudanças concorrentes, revisão independente e validação do resultado combinado. Integrações rotineiras podem ser autônomas com checks aprovados e permissões existentes. Fronteiras sensíveis e risco não esclarecido dependem de decisão humana.

## Verificação e conclusão

Preencha os documentos reais e execute:

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --deploy-strict
```

Execute também os checks do runtime publicados no [catálogo](runtime-catalog.md), o smoke local e o probe quando houver implantação. Teste contratos, falhas e compatibilidade conforme o risco; valide metas de escala com carga representativa.

Os controles documentais verificam estrutura e coerência superficial; revisão técnica avalia a decisão. O projeto só está validado quando os checks exigidos forem executados e aprovados. Registre limitações ou ferramentas ausentes como bloqueios, preservando separadamente os resultados estruturais já obtidos.
