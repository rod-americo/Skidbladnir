
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Worker residente")
    parser.add_argument("--once", action="store_true", help="executa um ciclo e sai")
    parser.add_argument("--interval", type=int, default=30, help="intervalo entre ciclos")
    return parser
