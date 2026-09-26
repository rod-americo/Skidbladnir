
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Worker com sessao de browser")
    parser.add_argument("--once", action="store_true", help="executa um ciclo e sai")
    parser.add_argument("--interval", type=int, default=30, help="intervalo entre ciclos")
    parser.add_argument(
        "--refresh-session",
        action="store_true",
        help="faz apenas o bootstrap/refresh dos artefatos de sessao",
    )
    parser.add_argument("--dry-run", action="store_true", help="gera artefatos placeholder sem abrir browser")
    parser.add_argument("--show-browser", action="store_true", help="abre browser visivel no refresh real")
    parser.add_argument("--login-url", default="", help="URL inicial para bootstrap de sessao")
    return parser
