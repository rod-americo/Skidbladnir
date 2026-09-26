
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


@dataclass
class AppSettings:
    name: str
    env: str
    log_level: str


@dataclass
class Settings:
    app: AppSettings
    config_path: Path
    raw: dict[str, object]


def _candidate_paths() -> list[Path]:
    env_path = os.getenv("{{ENV_PREFIX}}_CONFIG_FILE")
    paths: list[Path] = []
    if env_path:
        paths.append(Path(env_path))
    paths.append(Path("config/settings.local.json"))
    paths.append(Path("config/settings.example.json"))
    return paths


def load_settings() -> Settings:
    for path in _candidate_paths():
        if not path.exists():
            continue

        data = json.loads(path.read_text(encoding="utf-8"))
        app_data = data.get("app", {})
        return Settings(
            app=AppSettings(
                name=str(app_data.get("name", {{PROJECT_NAME_LITERAL}})),
                env=str(app_data.get("env", "dev")),
                log_level=str(app_data.get("log_level", "INFO")),
            ),
            config_path=path,
            raw=data,
        )

    return Settings(
        app=AppSettings(
            name={{PROJECT_NAME_LITERAL}},
            env="dev",
            log_level="INFO",
        ),
        config_path=Path("config/settings.example.json"),
        raw={},
    )
