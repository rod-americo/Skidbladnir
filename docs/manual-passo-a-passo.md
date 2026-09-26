# Manual passo a passo

## 1. Ler o kit

Informe ao agente o caminho real do clone e o objetivo. Comece pelo README, fluxo de projeto novo ou existente, política de runtimes, colaboração e validação. O kit não exige uma localização fixa no computador nem execução manual da CLI pelo usuário.

## 2. Decidir antes de gerar

Registre escopo, manutenção, contratos, bibliotecas, distribuição, operação e critérios mensuráveis de escala. Compare linguagens viáveis e documente restrições, riscos, mitigação e evidências. Nenhuma linguagem é default e nenhum scaffold tem preferência. Preserve um runtime existente adequado; avalie migrações separadamente.

## 3. Preparar tarefa e bootstrap

Designe responsabilidade por arquivos/módulos e crie uma branch com worktree ou checkout isolado para cada tarefa independente. Para trabalho concorrente, registre integrador e dependências. Use `docs/TASK_TEMPLATE.md` como modelo de contexto durável.

Após a [instalação](../INSTALL.md), uma geração pode ser:

```bash
newproj --list-presets
newproj ./Servico --runtime java --preset base --enforce-gate
```

Substitua runtime e preset pela decisão registrada. Rust e Java inicialmente têm `base`; os presets especializados existentes exigem `--runtime python` explícito. Ajuda, versão e doctor não exigem a opção. Nenhum download ocorre na geração.

## 4. Preencher os documentos reais

Preencha `PROJECT_GATE.md`, README, arquitetura, contratos, operação e decisões. Remova exemplos e seções sem função. Quatro camadas são opcionais e precisam de justificativa; siga convenções do ecossistema.

Os exemplos do kit não demonstram prontidão de produção. Registre comandos que existem e campos que o código consome. Não use dados reais ou sensíveis como fixtures. Projetos de pesquisa podem incluir `papers/` com hipótese, método, métricas e avaliação.

## 5. Declarar operação

Preencha `deploy/manifest.json` versão 1. Sem implantação configurada, use `deploy.target: none` e motivo explícito. O preset HTTP declara porta 8000 e `/health`; reveja ambos se mudar host/porta. Workers precisam de probe seguro e supervisão antes da implantação.

Separe teste, smoke e saúde operacional. Declare apenas estado e destinos de logs realmente usados. Logs do baseline vão para stdout; um diretório ignorado não significa persistência ou arquivo de log existente.

## 6. Instalar e validar

Siga os comandos do README gerado e do [catálogo](runtime-catalog.md). Toolchains e dependências estão fixadas; downloads ocorrem no bootstrap. Python usa `.venv`, hashes, Ruff e mypy; Node usa `npm ci`; Cargo e .NET usam lockfiles; Java usa Maven Wrapper.

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --deploy-strict
```

Execute também os checks de desenvolvimento e smoke do runtime. Prove a saúde do processo quando houver implantação. Ausência de ferramenta deve ser registrada como bloqueio; não declare sucesso de uma verificação não executada.

## 7. Resolver divergências documentais

O doctor faz comparações estruturais e textuais. Corrija divergências reais no código ou documentação. Para termos equivalentes, registre `token_alias_groups`; para exceções conscientes, use `ignored_warnings` com código e motivo. Execute `python3 scripts/project_doctor.py --audit-config` para identificar overrides sem efeito.

`--strict` transforma warnings textuais em falhas. Nenhum modo prova qualidade semântica da arquitetura ou substitui revisão humana/técnica.

## 8. Revisar e integrar

Revise diff e arquivos gerados, execute os checks exigidos e obtenha revisão independente. O integrador valida novamente o resultado combinado. Integração rotineira pode ser autônoma com permissões existentes e checks aprovados; decisões humanas são obrigatórias nas fronteiras sensíveis descritas no [protocolo de colaboração](agent-collaboration.md).

Registre commits, resultados, riscos, bloqueios e próximo passo na passagem de contexto. Não habilite automerge remoto nem altere proteções para contornar uma dependência.

## 9. Evoluir consumidores

Atualizar o kit não regenera consumidores. Leia o [guia 2.0](migration-2.0.md) e incorpore mudanças por diffs revisados. Preserve runtime e comportamento existentes quando adequados; adapte contratos, docs, CI e manifesto na mesma mudança lógica.
