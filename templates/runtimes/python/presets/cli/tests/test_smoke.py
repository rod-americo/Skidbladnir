
from {{PROJECT_SLUG}}.main import main


def test_smoke_doctor() -> None:
    assert main(["doctor"]) == 0
