
from __future__ import annotations

import sys
from pathlib import Path

from {{PROJECT_SLUG}}.application.pipeline import run_pipeline
from {{PROJECT_SLUG}}.interfaces.cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args([] if argv is None else argv)
    output = run_pipeline(args.item_id, Path("runtime/outbox"))
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
