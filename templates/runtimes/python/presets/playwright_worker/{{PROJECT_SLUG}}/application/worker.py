
from __future__ import annotations

import logging
import time
from pathlib import Path

from .contracts import BrowserCookie, SessionArtifacts
from .session import build_placeholder_session, save_session_artifacts


def refresh_session(
    logger: logging.Logger,
    storage_path: Path,
    *,
    dry_run: bool = False,
    show_browser: bool = False,
    login_url: str = "",
) -> int:
    if dry_run:
        artifacts = build_placeholder_session(login_url)
        save_session_artifacts(storage_path, artifacts)
        logger.info("sessao de browser simulada", extra={"evt": "browser_session_dry_run"})
        return 1

    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "playwright nao esta instalado; rode `python -m playwright install chromium`"
        ) from exc

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=not show_browser)
        context = browser.new_context()
        page = context.new_page()
        if login_url:
            page.goto(login_url, wait_until="domcontentloaded", timeout=30000)
        cookies = [
            BrowserCookie.from_playwright_dict(item)
            for item in context.cookies()
        ]
        browser.close()

    artifacts = SessionArtifacts(
        cookies=cookies,
        created_at_epoch=time.time(),
        base_url=login_url,
        notes="TODO: inserir login real e validacao de sessao",
    )
    save_session_artifacts(storage_path, artifacts)
    logger.info("sessao de browser atualizada", extra={"evt": "browser_session_refreshed"})
    return 1


def run_once(
    logger: logging.Logger,
    storage_path: Path,
    *,
    dry_run: bool = False,
    show_browser: bool = False,
    login_url: str = "",
) -> int:
    return refresh_session(
        logger,
        storage_path,
        dry_run=dry_run,
        show_browser=show_browser,
        login_url=login_url,
    )


def run_loop(
    logger: logging.Logger,
    interval_seconds: int,
    storage_path: Path,
    *,
    once: bool = False,
    dry_run: bool = False,
    show_browser: bool = False,
    login_url: str = "",
) -> int:
    processed = run_once(
        logger,
        storage_path,
        dry_run=dry_run,
        show_browser=show_browser,
        login_url=login_url,
    )
    if once:
        return processed

    while True:
        time.sleep(interval_seconds)
        run_once(
            logger,
            storage_path,
            dry_run=dry_run,
            show_browser=show_browser,
            login_url=login_url,
        )
