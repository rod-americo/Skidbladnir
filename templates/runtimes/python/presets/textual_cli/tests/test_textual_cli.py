
from {{PROJECT_SLUG}}.interfaces.tui.app import build_app
from {{PROJECT_SLUG}}.main import main


def test_doctor_command() -> None:
    assert main(["doctor"]) == 0


def test_build_app() -> None:
    app = build_app()
    assert app.__class__.__name__ == "DashboardApp"
