
from {{PROJECT_SLUG}}.main import main


def test_doctor_command() -> None:
    assert main(["doctor"]) == 0
