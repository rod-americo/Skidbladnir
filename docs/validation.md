# Validação

## Controles documentais e operacionais estáticos

```bash
python3 scripts/check_project_gate.py
python3 scripts/check_deploy_manifest.py
python3 scripts/project_doctor.py
python3 scripts/project_doctor.py --strict
python3 scripts/project_doctor.py --deploy-strict
python3 scripts/project_doctor.py --audit-config
```

O gate reconhece rótulos com ou sem acentos, normaliza espaços e rejeita respostas vazias, pendentes ou excessivamente curtas. O marcador `<!-- skidbladnir:gate:2 -->` exige também riscos/mitigações, evidências e critérios de escala. Documentos antigos sem esse marcador continuam aceitos pelas regras anteriores, incluindo seus rótulos sem acentos.

O doctor preserva comandos ao extrair o campo de validação do AGENTS e compara o runtime com o manifesto; `js` e `node` são equivalentes nessa comparação. `--deploy-strict` compara o comando principal e a declaração de saúde operacional. Documentos antigos que colocavam o probe na validação mínima têm compatibilidade de leitura; a migração deve separar as funções.

Esses são controles estruturais e de coerência declarada. Contagem de palavras, similaridade textual e presença de campos não comprovam qualidade da decisão, segurança, correção, cobertura ou escalabilidade. Overrides do doctor devem ser justificados e auditados; não use exceções para esconder divergências reais.

A validação do manifesto não executa comandos, não acessa URLs e não comprova saúde. Um HTTP vazio ou sem URL válida falha. `deploy.target: none` é válido para projetos sem implantação configurada.

## Testes, smoke e probe

Testes de desenvolvimento exercitam comportamento, contratos, falhas e compatibilidade conforme o risco. Smoke local exercita uma execução curta e conhecida. Saúde operacional observa o serviço ou processo em execução sem produzir efeitos de negócio. `pytest`, `npm test`, `cargo test` e comandos de processamento como `--once` não são probes por si só.

Requisitos de escala precisam de métricas, carga, ambiente, método e limites verificáveis. Não conclua capacidade produtiva a partir de scaffold, microbenchmark isolado ou nome da linguagem. Testes de carga e resiliência serão adaptados ao projeto concreto.

Os comandos por runtime são publicados no [catálogo gerado](runtime-catalog.md). Python executa Ruff, mypy e pytest; TypeScript compila em modo estrito; Swift tem testes reais; Java executa JUnit e JAR; Rust executa formatação, Clippy sem warnings, testes com lockfile e release. Instalações congeladas usam hashes Python, `npm ci`, Cargo `--locked` e .NET `--locked-mode`.

## Matriz do kit

Na raiz do kit, a regressão estrutural não exige toolchains das aplicações nem rede:

```bash
python3 run_regression_suite.py
python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj
python3 sync_runtime_catalog.py --check
```

Depois de provisionar cada versão concreta do catálogo:

```bash
python3 run_runtime_checks.py --runtime python
python3 run_runtime_checks.py --runtime node
python3 run_runtime_checks.py --runtime ts
python3 run_runtime_checks.py --runtime go
python3 run_runtime_checks.py --runtime swift
python3 run_runtime_checks.py --runtime csharp
python3 run_runtime_checks.py --runtime java
python3 run_runtime_checks.py --runtime rust
```

O runner gera projetos temporários e executa seus checks reais. Python percorre todos os presets; `--preset <nome>` restringe somente uma investigação local. O gate é preenchido com texto sintético exclusivamente na fixture temporária para exercitar a integração dos checks, sem simular aprovação arquitetural de um projeto real. A matriz verifica instalações, testes, builds, smoke, probe HTTP real e rejeição de divergências em npm/Cargo e de hashes inválidos em Python.

Cada job de CI provisiona explicitamente a toolchain; Swift usa imagem oficial fixada por versão e digest. Actions são fixadas por SHA, com `contents: read` e sem persistir credenciais do checkout. `generic` tem apenas verificações estruturais, pois não declara runtime dominante.

Ferramenta ausente ou versão divergente é falha no runner, não aprovação ou skip. Registre resultados estruturais, matriz de runtime, limitações locais e execução da CI separadamente. Só declare a matriz aprovada quando todos os checks exigidos tiverem passado. A integração exige revisão independente e validação do commit combinado conforme o [protocolo](agent-collaboration.md).
