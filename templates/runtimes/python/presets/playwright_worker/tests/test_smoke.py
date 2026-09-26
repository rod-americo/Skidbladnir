
from {{PROJECT_SLUG}}.main import main


def test_smoke_dry_run(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["--once", "--dry-run"]) == 1
