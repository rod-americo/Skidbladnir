
from __future__ import annotations

import sys

from {{PROJECT_SLUG}}.application.commands import doctor
from {{PROJECT_SLUG}}.interfaces.cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args([] if argv is None else argv)

    if args.command == "doctor":
        print(doctor())
        return 0

    if args.command == "tui":
        from {{PROJECT_SLUG}}.interfaces.tui.app import build_app

        build_app().run()
        return 0

    parser.error("comando nao suportado")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
