
from __future__ import annotations

import logging
import time


def run_once(logger: logging.Logger) -> int:
    logger.info("ciclo executado", extra={"evt": "worker_cycle"})
    return 1


def run_loop(logger: logging.Logger, interval_seconds: int, *, once: bool = False) -> int:
    processed = run_once(logger)
    if once:
        return processed

    while True:
        time.sleep(interval_seconds)
        run_once(logger)
