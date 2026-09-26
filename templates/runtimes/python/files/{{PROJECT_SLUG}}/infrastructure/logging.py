
from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime


class JsonFormatter(logging.Formatter):
    def __init__(self, service_name: str) -> None:
        super().__init__()
        self.service_name = service_name

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(UTC).isoformat(),
            "lvl": record.levelname,
            "svc": self.service_name,
            "mod": record.name,
            "evt": getattr(record, "evt", "log"),
            "msg": record.getMessage(),
        }
        return json.dumps(payload, ensure_ascii=True)


def build_logger(service_name: str, level: str = "INFO") -> logging.Logger:
    logger = logging.getLogger(service_name)
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter(service_name))
    logger.addHandler(handler)
    logger.propagate = False
    return logger
