# Install

## Objetivo

Este documento instala ou atualiza o comando `newproj` para uso diário.

## 1. Confirmar a localização do kit

O instalador funciona a partir do clone local do repositório.

Exemplo desta máquina:

- `~/Skidbladnir`

Se o repositório estiver em outro lugar, ajuste apenas o caminho do comando.

## 2. Escolher o diretório de binários

Opções comuns:

- `~/bin`
- `~/Scripts/bin`

Se você já usa `~/Scripts/bin` no `PATH`, pode manter esse diretório. Se quiser um binário curto e isolado no shell, prefira `~/bin`.

## 3. Rodar o instalador

Exemplo usando `~/bin`:

```bash bash ~/Skidbladnir/install_newproj.sh ~/bin
```

Exemplo mantendo `~/Scripts/bin`:

```bash
bash ~/Skidbladnir/install_newproj.sh ~/Scripts/bin
```

O instalador:

- garante permissão de execução no wrapper
- cria ou atualiza o link `newproj`
- informa a versão do kit
- avisa se o diretório de binários não está no `PATH`

## 4. Garantir o PATH

Se o instalador avisar que o binário não está no `PATH`, adicione no `~/.zshrc`:

```bash export PATH="$HOME/bin:$PATH"
```

Ou, se preferir `~/Scripts/bin`:

```bash
export PATH="$HOME/Scripts/bin:$PATH"
```

Depois recarregue o shell:

```bash source ~/.zshrc
```

## 5. Verificar a instalação

```bash
newproj --version
newproj --list-presets
```

Resultado esperado:

- a versão do kit aparece sem erro
- a lista de presets é exibida

## 6. Rodar a regressão do kit

Antes de confiar no setup, rode:

```bash python3 ~/Skidbladnir/run_regression_suite.py
```

Isso valida:

- versionamento do kit
- instalação do wrapper
- geração de projeto com gate
- `doctor`, `strict` e `audit-config`
- forwarding de `newproj doctor`

## 7. Atualizar o kit no futuro

Sempre que mudar o scaffolder ou o wrapper:

1. rode a regressão
2. confirme `newproj --version`
3. reinstale o wrapper se mudar a localização do binário

Comandos:

```bash
python3 ~/Skidbladnir/run_regression_suite.py
bash ~/Skidbladnir/install_newproj.sh ~/bin
```
