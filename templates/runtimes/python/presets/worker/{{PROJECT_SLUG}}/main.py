
from __future__ import annotations

import sys

from {{PROJECT_SLUG}}.application.worker import run_loop
from {{PROJECT_SLUG}}.infrastructure.logging import build_logger
from {{PROJECT_SLUG}}.interfaces.cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args([] if argv is None else argv)
    logger = build_logger({{PROJECT_NAME_LITERAL}})
    return run_loop(logger, args.interval, once=args.once)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
