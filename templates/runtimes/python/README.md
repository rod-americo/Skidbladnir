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
