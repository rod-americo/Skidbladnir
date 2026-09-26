
from {{PROJECT_SLUG}}.main import main


def test_smoke_pipeline() -> None:
    assert main(["--item-id", "demo-001"]) == 0
