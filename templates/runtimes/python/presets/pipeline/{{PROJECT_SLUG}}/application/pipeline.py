
from __future__ import annotations

import json
from pathlib import Path

from .contracts import PipelineItem


def extract(item_id: str) -> PipelineItem:
    return PipelineItem(item_id=item_id, payload={"item_id": item_id, "status": "extracted"})


def transform(item: PipelineItem) -> PipelineItem:
    item.payload["status"] = "transformed"
    return item


def load(item: PipelineItem, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{item.item_id}.json"
    destination.write_text(json.dumps(item.payload, ensure_ascii=True, indent=2), encoding="utf-8")
    return destination


def run_pipeline(item_id: str, output_dir: Path) -> Path:
    item = extract(item_id)
    item = transform(item)
    return load(item, output_dir)
