
from {{PROJECT_SLUG}}.interfaces.tui.app import build_app


def main() -> int:
    build_app().run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
