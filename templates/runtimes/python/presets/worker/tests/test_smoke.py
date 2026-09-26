
from {{PROJECT_SLUG}}.main import main


def test_smoke_once() -> None:
    assert main(["--once"]) == 1
