
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Executa pipeline DICOM local")
    parser.add_argument("--inbox", default="runtime/inbox", help="diretorio de entrada")
    parser.add_argument("--outbox", default="runtime/outbox", help="diretorio de saida")
    parser.add_argument("--sample", action="store_true", help="gera um DICOM de exemplo antes de processar")
    return parser
