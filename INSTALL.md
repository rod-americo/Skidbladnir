# Instalação

O protocolo pode ser usado diretamente por um agente com acesso ao clone. Este guia instala o wrapper auxiliar `newproj`; não instala toolchains de aplicações nem altera configurações remotas.

## Clone e validação

Clone o repositório em um diretório de sua escolha e execute os comandos a partir da raiz do clone. O kit e os validadores usam Python 3.10 ou superior; a release é verificada com a versão concreta publicada no [catálogo](docs/runtime-catalog.md). Essa ferramenta não determina a linguagem dos projetos gerados.

```bash
python3 scaffold_project.py --version
python3 run_regression_suite.py
python3 -m py_compile scaffold_project.py run_regression_suite.py bin/newproj
```

A regressão acima é estrutural e não equivale à matriz completa de runtimes. Consulte [validação](docs/validation.md).

## Wrapper

```bash
bash install_newproj.sh "$HOME/bin"
export PATH="$HOME/bin:$PATH"
newproj --version
newproj --list-presets
```

O instalador cria ou atualiza o link para `bin/newproj` dentro deste clone. O destino pode ser outro diretório já presente no PATH. Para persistir o PATH, ajuste a configuração do seu shell conforme sua preferência; o script não exige localização fixa do kit.

## Geração

```bash
newproj ./Servico --runtime java --preset base --enforce-gate
newproj ./Ferramenta --runtime rust --preset base --enforce-gate
newproj ./Api --runtime python --preset fastapi-service
```

Escolha o runtime pelo [protocolo](docs/runtimes.md). `--runtime` é obrigatório e não tem default; presets Python também exigem a opção. A geração não baixa dependências. Siga o README gerado para bootstrap, checks e smoke com versões fixadas.

## Atualização do kit

Atualize seu clone pelo fluxo de Git adotado, leia o [guia de migração](docs/migration-2.0.md) e o [changelog](CHANGELOG.md), execute a regressão e reinstale o link caso o clone tenha mudado de lugar. Consumidores existentes não são regenerados; incorpore mudanças por revisão incremental de arquivos e contratos.

Para verificar runtimes, provisione cada toolchain do catálogo e execute `python3 run_runtime_checks.py --runtime <id>`. Ferramenta ausente ou versão divergente é falha. A CI do kit faz isso em jobs separados, incluindo todos os presets Python.

## Doctor

```bash
newproj doctor ./Projeto
newproj doctor --strict ./Projeto
newproj doctor --deploy-strict ./Projeto
newproj doctor --audit-config ./Projeto
```

Esses comandos usam os scripts presentes no projeto consumidor. Atualizar o kit não atualiza automaticamente o doctor de consumidores antigos.
