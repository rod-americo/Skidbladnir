
from __future__ import annotations

import argparse

from {{PROJECT_SLUG}}.infrastructure.config import load_settings
from {{PROJECT_SLUG}}.infrastructure.logging import build_logger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Entrypoint principal do projeto")
    parser.parse_args([] if argv is None else argv)
    settings = load_settings()
    logger = build_logger(settings.app.name, settings.app.log_level)
    logger.info("servico inicializado", extra={"evt": "startup"})
    return 0
