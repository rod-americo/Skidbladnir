
from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="CLI com cockpit Textual")
    subparsers = parser.add_subparsers(dest="command", required=True)

    doctor = subparsers.add_parser("doctor", help="valida baseline minima")
    doctor.set_defaults(command="doctor")

    tui = subparsers.add_parser("tui", help="abre a interface textual")
    tui.set_defaults(command="tui")
    return parser
