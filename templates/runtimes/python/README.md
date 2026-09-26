# Python

Use pacote na raiz e `python -m <slug>`; `.venv` fica na raiz. Os presets especializados são opt-in e exigem `--runtime python`. Código comum está em `files/`, extensões em `presets/` e requisitos congelados em `requirements/`. Execute Ruff, mypy e pytest. Quatro camadas são opcionais; launchers TUI/GUI dedicados podem ser finos em `tui/` e `gui/`.

Versões e comandos exatos estão no [catálogo](../catalog.json) e na [documentação gerada](../../../docs/runtime-catalog.md). A existência deste scaffold não favorece a escolha da linguagem. O baseline usa `deploy.target: none`, salvo preset com operação HTTP local explícita.
