
from __future__ import annotations

import json
import time
from pathlib import Path

from .contracts import BrowserCookie, SessionArtifacts


def save_session_artifacts(path: str | Path, artifacts: SessionArtifacts) -> Path:
    destination = Path(path).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(artifacts.to_dict(), ensure_ascii=True, indent=2) + "\n",
        encoding="utf-8",
    )
    return destination


def load_session_artifacts(path: str | Path) -> SessionArtifacts:
    source = Path(path).expanduser().resolve()
    payload = json.loads(source.read_text(encoding="utf-8"))
    return SessionArtifacts.from_dict(payload)


def build_placeholder_session(base_url: str = "") -> SessionArtifacts:
    return SessionArtifacts(
        cookies=[
            BrowserCookie(
                name="session",
                value="placeholder",
                domain="example.invalid",
                path="/",
            )
        ],
        created_at_epoch=time.time(),
        base_url=base_url,
        notes="TODO: substituir bootstrap placeholder por login real",
    )
