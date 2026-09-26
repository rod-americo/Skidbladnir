
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Executa pipeline em etapas")
    parser.add_argument("--item-id", default="demo-001", help="identificador do item")
    parser.add_argument("--once", action="store_true", help="mantido para compatibilidade operacional")
    return parser
