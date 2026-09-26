
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass


@dataclass
class BrowserCookie:
    name: str
    value: str
    domain: str = ""
    path: str = "/"

    @classmethod
    def from_playwright_dict(cls, payload: Mapping[str, object]) -> BrowserCookie:
        return cls(
            name=str(payload.get("name", "")),
            value=str(payload.get("value", "")),
            domain=str(payload.get("domain", "")),
            path=str(payload.get("path", "/")),
        )

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass
class SessionArtifacts:
    cookies: list[BrowserCookie]
    created_at_epoch: float
    base_url: str = ""
    notes: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "cookies": [cookie.to_dict() for cookie in self.cookies],
            "created_at_epoch": self.created_at_epoch,
            "base_url": self.base_url,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, object]) -> SessionArtifacts:
        raw_cookies = payload.get("cookies", [])
        cookies = []
        if isinstance(raw_cookies, list):
            for item in raw_cookies:
                if isinstance(item, dict):
                    cookies.append(BrowserCookie.from_playwright_dict(item))
        created_at = payload.get("created_at_epoch", 0.0) or 0.0
        if not isinstance(created_at, (int, float, str)):
            raise ValueError("created_at_epoch must be a number")
        return cls(
            cookies=cookies,
            created_at_epoch=float(created_at),
            base_url=str(payload.get("base_url", "")),
            notes=str(payload.get("notes", "")),
        )
