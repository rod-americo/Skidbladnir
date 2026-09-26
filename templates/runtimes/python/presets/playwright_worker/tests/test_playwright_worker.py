
from {{PROJECT_SLUG}}.main import main


def test_worker_dry_run_creates_session_artifact(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["--once", "--dry-run"]) == 1
    assert (tmp_path / "runtime" / "browser" / "session.json").exists()
