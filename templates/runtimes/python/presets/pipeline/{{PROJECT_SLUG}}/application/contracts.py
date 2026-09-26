
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PipelineItem:
    item_id: str
    payload: dict
