
from {{PROJECT_SLUG}}.main import main


def test_worker_once() -> None:
    assert main(["--once"]) == 1
