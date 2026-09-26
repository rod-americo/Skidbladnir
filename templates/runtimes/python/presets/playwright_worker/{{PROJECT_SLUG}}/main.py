
from __future__ import annotations

import sys
from pathlib import Path

from {{PROJECT_SLUG}}.application.worker import refresh_session, run_loop
from {{PROJECT_SLUG}}.infrastructure.config import Settings, load_settings
from {{PROJECT_SLUG}}.infrastructure.logging import build_logger
from {{PROJECT_SLUG}}.interfaces.cli.parser import build_parser


def _browser_storage_path(settings: Settings) -> Path:
    browser = settings.raw.get("browser", {})
    if isinstance(browser, dict):
        configured = browser.get("storage_path")
        if configured:
            return Path(str(configured))
    return Path("runtime/browser/session.json")


def _login_url(settings: Settings, cli_value: str) -> str:
    if cli_value:
        return cli_value
    browser = settings.raw.get("browser", {})
    if isinstance(browser, dict):
        return str(browser.get("login_url", "") or "")
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args([] if argv is None else argv)
    settings = load_settings()
    logger = build_logger(settings.app.name, settings.app.log_level)
    storage_path = _browser_storage_path(settings)
    login_url = _login_url(settings, args.login_url)

    if args.refresh_session:
        return refresh_session(
            logger,
            storage_path,
            dry_run=args.dry_run,
            show_browser=args.show_browser,
            login_url=login_url,
        )

    return run_loop(
        logger,
        args.interval,
        storage_path,
        once=args.once,
        dry_run=args.dry_run,
        show_browser=args.show_browser,
        login_url=login_url,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
