# Python Runtime Template

Use pacote direto em `/<slug>/` como padrão principal.

Comandos:

```bash
python3 -m venv .venv --prompt $(basename "$PWD")
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m <slug>
python -m pytest -q
```

O entrypoint público é `python -m <slug>`.

Quando TUI ou GUI forem aplicações dedicadas, prefira launchers top-level finos em `tui/__main__.py` e `gui/__main__.py`, executados com `python -m tui` e `python -m gui`. Esses launchers apenas delegam para a implementação em `<slug>/interfaces/`; não exponha novos comandos públicos como `python -m <slug>.tui` ou `python -m <slug>.gui`.
