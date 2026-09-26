
from __future__ import annotations

import sys
from pathlib import Path

from {{PROJECT_SLUG}}.application.pipeline import run_pipeline, write_sample_dicom
from {{PROJECT_SLUG}}.interfaces.cli.parser import build_parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args([] if argv is None else argv)
    inbox = Path(args.inbox)
    outbox = Path(args.outbox)

    if args.sample:
        write_sample_dicom(inbox)

    outputs = run_pipeline(inbox, outbox)
    for output in outputs:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
